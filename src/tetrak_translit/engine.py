"""The transliteration engine: pure functions over a :class:`Scheme`.

Script to Latin walks each word letter by letter, longest unit first (so
a digraph is taken whole), rendering each through the scheme's table and
carrying the source's case across: a capital letter capitalises its
rendering, a word in capitals renders in capitals. Punctuation is the scheme's to
say: marks its standard maps are rendered where they stand or moved to
the end of the sentence, and the rest are left alone. Text outside the
scheme's script passes through untouched, so a mixed-script line -- an
Armenian title with a Latin author -- comes out with only the Armenian
changed.

Latin to script is offered only for the schemes whose tables are
one-to-one. The rest are lossy by construction -- ALA-LC's ``zh`` is
``ժ`` or ``զ``+``հ`` -- and guessing would be worse than refusing. For
*matching* across schemes, which needs no guessing, there is
:func:`tetrak_translit.fold`.

This module knows nothing about which scripts exist; it is given a scheme
and reads the script from it. That is what lets a script package's fold
use it without a circular import.
"""

from __future__ import annotations

import unicodedata
from itertools import pairwise

from .script import Scheme

#: Every apostrophe-like mark a reader might type for an aspiration or
#: ejective sign.
APOSTROPHES = "'’‘ʻʿʼˀ`´"


class NotReversibleError(ValueError):
    """Raised when asked to reverse a scheme whose table is lossy."""


def _units(word: str, scheme: Scheme) -> list[tuple[str, bool]]:
    """Split a word into (lowercase unit, was-capitalised) pairs.

    A mark set inside a digraph (Armenian's ``ո՞ւ``, the question mark on
    the stressed vowel) does not split it: the digraph is one unit and the
    mark follows it.
    """
    lowered = [character.lower() for character in word]
    capitals = [character.isupper() for character in word]
    digraphs = {key for key in scheme.digraphs if len(key) == 2}
    marks = scheme.script.marks

    units: list[tuple[str, bool]] = []
    index = 0
    while index < len(lowered):
        second = index + 1
        while second < len(lowered) and lowered[second] in marks:
            second += 1
        if second < len(lowered) and lowered[index] + lowered[second] in digraphs:
            units.append((lowered[index] + lowered[second], capitals[index]))
            units.extend((lowered[inside], False) for inside in range(index + 1, second))
            index = second + 1
        else:
            units.append((lowered[index], capitals[index]))
            index += 1
    return units


def _render_word(word: str, scheme: Scheme, variant: str | None) -> str:
    """Render one word: the script's letters, and any marks set inside it.

    Marks are rendered through the scheme's punctuation where they stand
    and are invisible to everything positional: the letter after ``՞`` is
    not word-initial, and a word in capitals is still in capitals.
    """
    units = _units(word, scheme)
    marks = scheme.script.marks
    letters = [index for index, (unit, _) in enumerate(units) if unit not in marks]
    all_capitals = len(letters) > 1 and all(units[index][1] for index in letters)
    following = {here: units[there][0] for here, there in pairwise(letters)}
    vowels = scheme.script.vowels
    rendered: list[str] = []
    previous: str | None = None
    adjoining: str | None = None
    for index, (unit, capital) in enumerate(units):
        if unit in marks:
            latin = scheme.punctuation.get(unit, unit)
            rendered.append(latin)
            if latin:
                adjoining = None
            continue
        latin = scheme.render(
            unit,
            initial=previous is None,
            final=index == letters[-1],
            after_vowel=previous is not None and previous[-1] in vowels,
            following=following.get(index),
            capital=capital,
            variant=variant,
        )
        if all_capitals:
            latin = latin.upper()
        elif capital:
            latin = latin[:1].upper() + latin[1:]
        if adjoining is not None and (adjoining, unit) in scheme.separate:
            rendered.append(scheme.separator)
        rendered.append(latin)
        previous = adjoining = unit
    return "".join(rendered)


def _before_trailing_space(out: list[str], marks: list[str]) -> list[str]:
    """Insert *marks* before any spaces or tabs at the end of *out*."""
    text = "".join(out)
    body = text.rstrip(" \t")
    return [body, "".join(marks), text[len(body) :]]


def render(text: str, scheme: Scheme, variant: str | None = None) -> str:
    """Render the scheme's script in *text* to Latin, leaving the rest alone.

    Args:
        text: Any string.
        scheme: The table to render through.
        variant: The variant of the script the text is in (Armenian's
            ``"classical"`` or ``"reformed"`` orthography), for a scheme
            with rules that depend on it; ``None`` applies none of them.
    """
    script = scheme.script
    text = script.expand(unicodedata.normalize("NFC", text))
    out: list[str] = []
    word: list[str] = []
    pending: list[str] = []

    def hold(mark: str) -> None:
        latin = scheme.sentence_final[mark]
        if latin not in pending:
            pending.append(latin)

    for character in text:
        if script.is_letter(character) or (word and character in script.marks):
            if character in scheme.sentence_final:
                hold(character)
            else:
                word.append(character)
            continue
        if word:
            out.append(_render_word("".join(word), scheme, variant))
            word = []
        if character in scheme.sentence_final:
            hold(character)
        elif character in scheme.sentence_end and pending:
            out.extend(pending)
            pending.clear()
        elif character in "\r\n" and pending:
            out = _before_trailing_space(out, pending)
            pending.clear()
            out.append(character)
        else:
            out.append(scheme.punctuation.get(character, character))
    if word:
        out.append(_render_word("".join(word), scheme, variant))
    if pending:
        out = _before_trailing_space(out, pending)
    return "".join(out)


# Each scheme's inverse, built once: a fold at query time reads every query
# back and must not sort the table each time. Keyed by id, with the scheme
# kept to check it is the same object, since a Scheme is not hashable.
_INVERSES: dict[str, tuple[Scheme, list[tuple[str, str]]]] = {}


def _inverse(scheme: Scheme) -> list[tuple[str, str]]:
    """Latin unit to script unit, longest Latin first, for a reversible table.

    The Latin is decomposed (NFD), as :func:`read` decomposes its input, so
    that a capital with no precomposed form -- ``J̌``, J and a combining
    caron, the capital of ``ǰ`` -- lowercases to the same characters as
    the table's letter.
    """
    cached = _INVERSES.get(scheme.id)
    if cached is not None and cached[0] is scheme:
        return cached[1]
    pairs = {
        unicodedata.normalize("NFD", latin.lower()): letter
        for letter, latin in scheme.letters.items()
    }
    for unit, latin in scheme.digraphs.items():
        pairs.setdefault(unicodedata.normalize("NFD", latin.lower()), unit)
    for mark, latin in scheme.punctuation.items():
        if latin:
            pairs.setdefault(unicodedata.normalize("NFD", latin.lower()), mark)
    inverse = sorted(pairs.items(), key=lambda item: -len(item[0]))
    _INVERSES[scheme.id] = (scheme, inverse)
    return inverse


def _normalise_marks(text: str, scheme: Scheme, mark: str) -> str:
    """*text* with the apostrophes people type for the table's *mark* made it.

    Only an apostrophe-like character directly after a letter the table
    marks is taken for the mark (``t'`` for ``tʻ``); one anywhere else is
    a quotation mark and is left alone, so ``‘Erewan’`` keeps its quotes.
    *text* is in NFD, as :func:`read` works.
    """
    bases = {
        unicodedata.normalize("NFD", latin[:-1].lower())
        for latin in scheme.letters.values()
        if latin[-1] in APOSTROPHES
    }
    longest = max(len(base) for base in bases)
    out: list[str] = []
    for index, character in enumerate(text):
        if character in APOSTROPHES:
            before = text[max(0, index - longest) : index].lower()
            if any(before.endswith(base) for base in bases):
                character = mark
        out.append(character)
    return "".join(out)


def read(text: str, scheme: Scheme) -> str:
    """Read Latin written in *scheme* back into its script.

    Raises:
        NotReversibleError: *scheme* is lossy and cannot be reversed.
    """
    if not scheme.reversible:
        raise NotReversibleError(
            f"{scheme.name} ({scheme.id}) is not reversible: more than one spelling can "
            f"produce the same Latin, so reading it back would be a guess. "
            f"To match names across schemes without reversing, use fold()."
        )
    aspiration = next(
        (latin[-1] for latin in scheme.letters.values() if latin[-1] in APOSTROPHES), None
    )
    text = unicodedata.normalize("NFD", text)
    if aspiration is not None:
        text = _normalise_marks(text, scheme, aspiration)

    inverse = _inverse(scheme)
    cased = scheme.script.cased
    out: list[str] = []
    index = 0
    separator = scheme.separator
    while index < len(text):
        if separator and text.startswith(separator, index):
            index += len(separator)
            continue
        for latin, unit in inverse:
            end = index + len(latin)
            candidate = text[index:end]
            # A match must end on a whole character: plain e is not the
            # start of an ē that the table does not have.
            if candidate.lower() == latin and not (
                end < len(text) and unicodedata.combining(text[end])
            ):
                if cased and candidate[0].isupper():
                    unit = unit[0].upper() + unit[1:]
                out.append(unit)
                index = end
                break
        else:
            out.append(text[index])
            index += 1
    return unicodedata.normalize("NFC", "".join(out))


__all__ = ["APOSTROPHES", "NotReversibleError", "read", "render"]
