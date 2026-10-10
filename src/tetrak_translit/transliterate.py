"""Transliterate between Armenian script and the named Latin schemes.

Armenian to Latin walks each word letter by letter, longest unit first
(so ``ու`` and the ligature are taken whole), rendering each through the
scheme's table and carrying the source's case across: a capital letter
capitalises its rendering, a word in capitals renders in capitals. Text
that is not Armenian passes through untouched, so a mixed-script line --
an Armenian title with a Latin author -- comes out with only the Armenian
changed.

The two-letter ``եւ`` and the ligature ``և`` are rendered as the scheme's
table says, separately: ALA-LC writes *Erevan* for ``Երևան`` and *Erewan*
for ``Երեւան``, and a catalogue record carries whichever its source had.
They are the same letters -- the ligature is a typographic habit, not an
orthography (Tetrak brief 014) -- so it is :func:`tetrak_translit.fold`,
not the display scheme, that treats them as one.

Latin to Armenian is offered only for the schemes whose tables are
one-to-one (ISO 9985 and Hübschmann-Meillet). The rest are lossy by
construction -- ALA-LC's ``ts`` is ``ծ`` or ``տ``+``ս`` -- and guessing
would be worse than refusing, so :func:`transliterate` raises
:class:`NotReversibleError` for them. For *matching* across schemes, which
needs no guessing, use :func:`tetrak_translit.fold`.
"""

from __future__ import annotations

import unicodedata

from .schemes import ARMENIAN_LOWERCASE, SCHEMES, Scheme

#: Lowercase Armenian vowels, for the schemes with after-vowel rules.
_VOWELS = frozenset("աեէըիոօ")
#: Every apostrophe-like mark a reader might type for an aspiration sign.
_APOSTROPHES = "'’‘ʻʿʼˀ`´"


class UnknownSchemeError(KeyError):
    """Raised when a scheme key names no table."""


class NotReversibleError(ValueError):
    """Raised when asked to reverse a scheme whose table is lossy."""


def get_scheme(scheme: str | Scheme) -> Scheme:
    """Resolve a scheme key (``"ala_lc"``) or pass a :class:`Scheme` through.

    Raises:
        UnknownSchemeError: *scheme* is a key that names no table.
    """
    if isinstance(scheme, Scheme):
        return scheme
    key = scheme.lower().replace("-", "_").replace(" ", "_")
    try:
        return SCHEMES[key]
    except KeyError:
        known = ", ".join(SCHEMES)
        raise UnknownSchemeError(f"unknown scheme {scheme!r}; known schemes: {known}") from None


def _is_armenian_letter(character: str) -> bool:
    return "Ա" <= character <= "ֈ"


def _units(word: str, scheme: Scheme) -> list[tuple[str, bool]]:
    """Split an Armenian word into (lowercase unit, was-capitalised) pairs.

    ``ու`` and any other digraph the scheme renders whole are taken as
    one; everything else is a single letter.
    """
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
    rendered: list[str] = []
    previous: str | None = None
    for position, (unit, capital) in enumerate(units):
        latin = scheme.render(
            unit,
            initial=position == 0,
            after_vowel=previous is not None and previous[-1] in _VOWELS,
        )
        if all_capitals:
            latin = latin.upper()
        elif capital:
            latin = latin[:1].upper() + latin[1:]
        rendered.append(latin)
        previous = unit
    return "".join(rendered)


def to_latin(text: str, scheme: str | Scheme) -> str:
    """Render the Armenian in *text* through *scheme*, leaving the rest alone."""
    table = get_scheme(scheme)
    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    word: list[str] = []
    for character in text:
        if _is_armenian_letter(character):
            word.append(character)
            continue
        if word:
            out.append(_render_word("".join(word), table))
            word = []
        out.append(character)
    if word:
        out.append(_render_word("".join(word), table))
    return "".join(out)


def _inverse(scheme: Scheme) -> list[tuple[str, str]]:
    """Latin unit to Armenian unit, longest Latin first, for a reversible table."""
    pairs = {latin.lower(): armenian for armenian, latin in scheme.letters.items()}
    for armenian, latin in scheme.digraphs.items():
        pairs.setdefault(latin.lower(), armenian)
    return sorted(pairs.items(), key=lambda item: -len(item[0]))


def to_armenian(text: str, scheme: str | Scheme) -> str:
    """Read Latin written in *scheme* back into Armenian script.

    Raises:
        NotReversibleError: *scheme* is lossy and cannot be reversed.
    """
    table = get_scheme(scheme)
    if not table.reversible:
        raise NotReversibleError(
            f"{table.name} is not reversible: more than one Armenian spelling can "
            f"produce the same Latin, so reading it back would be a guess. Reversible "
            f"schemes: {', '.join(key for key, s in SCHEMES.items() if s.reversible)}. "
            f"To match names across schemes without reversing, use fold()."
        )
    aspiration = next(
        (latin[-1] for latin in table.letters.values() if latin[-1] in _APOSTROPHES), None
    )
    text = unicodedata.normalize("NFC", text)
    if aspiration is not None:
        for mark in _APOSTROPHES:
            text = text.replace(mark, aspiration)

    inverse = _inverse(table)
    out: list[str] = []
    index = 0
    while index < len(text):
        for latin, armenian in inverse:
            candidate = text[index : index + len(latin)]
            if candidate.lower() == latin:
                if candidate[0].isupper():
                    armenian = armenian[0].upper() + armenian[1:]
                out.append(armenian)
                index += len(latin)
                break
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def transliterate(text: str, scheme: str | Scheme = "ala_lc", *, to: str = "latin") -> str:
    """Transliterate *text* between Armenian and *scheme*.

    Args:
        text: The text. For ``to="latin"`` the Armenian in it is rendered
            and everything else is passed through; for ``to="armenian"``
            the whole string is read as Latin in *scheme*.
        scheme: A key from :data:`tetrak_translit.schemes.SCHEMES`
            (``"ala_lc"``, ``"iso_9985"``, ``"bgn_pcgn"``,
            ``"hubschmann_meillet"``, ``"western"``) or a :class:`Scheme`.
        to: ``"latin"`` (the default) or ``"armenian"``.

    Returns:
        The transliterated string.

    Raises:
        UnknownSchemeError: *scheme* names no table.
        NotReversibleError: ``to="armenian"`` with a lossy scheme.
        ValueError: *to* is neither direction.
    """
    if to == "latin":
        return to_latin(text, scheme)
    if to == "armenian":
        return to_armenian(text, scheme)
    raise ValueError(f"to must be 'latin' or 'armenian', not {to!r}")


__all__ = [
    "ARMENIAN_LOWERCASE",
    "NotReversibleError",
    "UnknownSchemeError",
    "get_scheme",
    "to_armenian",
    "to_latin",
    "transliterate",
]
