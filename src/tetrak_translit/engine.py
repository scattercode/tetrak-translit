"""The transliteration engine: pure functions over a :class:`Scheme`.

Script to Latin walks each word letter by letter, longest unit first (so
a digraph is taken whole), rendering each through the scheme's table and
carrying the source's case across: a capital letter capitalises its
rendering, a word in capitals renders in capitals. Text outside the
scheme's script passes through untouched, so a mixed-script line -- an
Armenian title with a Latin author -- comes out with only the Armenian
changed.

Latin to script is offered only for the schemes whose tables are
one-to-one. The rest are lossy by construction -- ALA-LC's ``ts`` is
``ծ`` or ``տ``+``ս`` -- and guessing would be worse than refusing. For
*matching* across schemes, which needs no guessing, there is
:func:`tetrak_translit.fold`.

This module knows nothing about which scripts exist; it is given a scheme
and reads the script from it. That is what lets a script package's fold
use it without a circular import.
"""

from __future__ import annotations

import unicodedata

from .script import Scheme

#: Every apostrophe-like mark a reader might type for an aspiration or
#: ejective sign.
APOSTROPHES = "'’‘ʻʿʼˀ`´"


class NotReversibleError(ValueError):
    """Raised when asked to reverse a scheme whose table is lossy."""


def _units(word: str, scheme: Scheme) -> list[tuple[str, bool]]:
    """Split a word into (lowercase unit, was-capitalised) pairs."""
    lowered = [character.lower() for character in word]
    capitals = [character.isupper() for character in word]
    digraphs = {key for key in scheme.digraphs if len(key) == 2}

    units: list[tuple[str, bool]] = []
    index = 0
    while index < len(lowered):
        pair = "".join(lowered[index : index + 2])
        if pair in digraphs:
            units.append((pair, capitals[index]))
            index += 2
        else:
            units.append((lowered[index], capitals[index]))
            index += 1
    return units


def _render_word(word: str, scheme: Scheme) -> str:
    units = _units(word, scheme)
    all_capitals = len(units) > 1 and all(capital for _, capital in units)
    vowels = scheme.script.vowels
    rendered: list[str] = []
    previous: str | None = None
    for position, (unit, capital) in enumerate(units):
        latin = scheme.render(
            unit,
            initial=position == 0,
            after_vowel=previous is not None and previous[-1] in vowels,
        )
        if all_capitals:
            latin = latin.upper()
        elif capital:
            latin = latin[:1].upper() + latin[1:]
        rendered.append(latin)
        previous = unit
    return "".join(rendered)


def render(text: str, scheme: Scheme) -> str:
    """Render the scheme's script in *text* to Latin, leaving the rest alone."""
    script = scheme.script
    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    word: list[str] = []
    for character in text:
        if script.is_letter(character):
            word.append(character)
            continue
        if word:
            out.append(_render_word("".join(word), scheme))
            word = []
        out.append(character)
    if word:
        out.append(_render_word("".join(word), scheme))
    return "".join(out)


def _inverse(scheme: Scheme) -> list[tuple[str, str]]:
    """Latin unit to script unit, longest Latin first, for a reversible table.

    The Latin is decomposed (NFD), as :func:`read` decomposes its input, so
    that a capital with no precomposed form -- ``J̌``, J and a combining
    caron, the capital of ``ǰ`` -- lowercases to the same characters as
    the table's letter.
    """
    pairs = {
        unicodedata.normalize("NFD", latin.lower()): letter
        for letter, latin in scheme.letters.items()
    }
    for unit, latin in scheme.digraphs.items():
        pairs.setdefault(unicodedata.normalize("NFD", latin.lower()), unit)
    return sorted(pairs.items(), key=lambda item: -len(item[0]))


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
        for mark in APOSTROPHES:
            text = text.replace(mark, aspiration)

    inverse = _inverse(scheme)
    cased = scheme.script.cased
    out: list[str] = []
    index = 0
    while index < len(text):
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
