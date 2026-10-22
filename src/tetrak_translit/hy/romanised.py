"""The marks that show a Latin-script value is romanised Armenian.

A catalogue's language code cannot always say which records are Armenian,
and a romanised title is written in the same letters as an English,
French or German one. The value itself can say more. A romanisation
shows itself through marks that ordinary English, French or German
spelling does not carry: the aspirate in *patmutʻiwn*, the *ĕ* of
*Keankʻi mĕ*, the *ṙ* of Hübschmann-Meillet.

The marks are evidence for search and display, never a filter for
excluding records. A romanisation without marks (*Erker*, *Hayery*)
shows none, and the marks other languages share are reported but are not
evidence on their own. Measured on a hand-judged sample of forty
catalogue titles, the distinctive marks found 19 of 21 Armenian works and
none of the other 19. Scholarly
romanisations that write the aspirate as ``ʿ`` and *ł* for ``ղ``, and
German ones (*tsch*, *č*), carry only shared marks, which is why
:func:`tetrak_translit.detect` reports every mark rather than a yes or no.
"""

from __future__ import annotations

import re

from ..script import RomanisationMark

#: Every mark, most distinctive first.
MARKS: tuple[RomanisationMark, ...] = (
    RomanisationMark(
        "aspirate",
        "an aspirate apostrophe after t, k, p, c, ch or ts",
        # tʻ, kʻ, pʻ, cʻ, chʻ, tsʻ, in any of the four marks catalogues use,
        # before a letter or at the end of a word. Not "'s", which is
        # English; not after other consonants, which is French (l’Arménie,
        # jusqu’au); and c only after a letter, since c'est is French too.
        re.compile(
            r"(?:ch|ts|[tkp]|(?<=[^\W\d_])c)[ʻ’'ʼ](?!s\b)(?:[^\W\d_]|(?=[\s.,:;/=)\]]|$))",
            re.IGNORECASE,
        ),
        distinctive=True,
    ),
    RomanisationMark(
        "combining-comma",
        "an aspirate written as a combining comma above right (U+0315)",
        re.compile("̕"),
        distinctive=True,
    ),
    RomanisationMark("e-breve", "ĕ for ը", re.compile("[ĕĔ]"), distinctive=True),
    RomanisationMark("r-dot", "ṛ or ṙ for ռ", re.compile("[ṛṙṚṘ]"), distinctive=True),
    RomanisationMark("long-vowel", "ē or ō for է or օ", re.compile("[ēōĒŌ]"), distinctive=False),
    RomanisationMark(
        "caron-or-dot",
        "ġ, č, š, ž or ǰ",
        re.compile("[ġčšžǰĠČŠŽ]"),
        distinctive=False,
    ),
    RomanisationMark(
        "scholarly",
        "ʿ for the aspirate, ł for ղ or ə for ը",
        re.compile("[ʿłəŁ]"),
        distinctive=False,
    ),
    RomanisationMark(
        "german",
        "tsch or sch, as German romanisations write չ and շ",
        # Not in school or scholar, which fill an English-language catalogue.
        re.compile("t?sch(?!o{1,2}l)", re.IGNORECASE),
        distinctive=False,
    ),
)

__all__ = ["MARKS"]
