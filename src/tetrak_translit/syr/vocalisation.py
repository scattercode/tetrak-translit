"""Whether Syriac text is vocalised, and with which system of points.

Most Syriac, manuscript or print, is written without vowels, and a
catalogue's title in the script almost never has them; where vowels are
written, they are one of two systems. West Syriac uses small Greek
letters above or below the line, East Syriac uses dots, and a reader who
knows which can tell a text's tradition from its pointing even when the
script style is not recorded. The three script styles themselves --
Estrangela, Serto, Madnhaya -- share one encoding and differ only in the
font, so nothing in the text can tell them apart, and this does not try.
"""

from __future__ import annotations

import re

UNVOCALISED = "unvocalised"
WEST = "west"
EAST = "east"
MIXED = "mixed"

_LETTER = re.compile(r"[ܐ-ܯݍ-ݏ]")
#: The West Syriac vowel signs: Greek letters above or below the line.
_WEST = re.compile(r"[ܱܴܷܻܾܰܳܶܺܽ]")
#: The East Syriac vowel dots.
_EAST = re.compile(r"[ܸܹܼܲܵܿ]")


def vocalisation(text: str) -> str | None:
    """The vowel pointing of the Syriac in *text*, or ``None`` if there is none.

    ``west`` or ``east`` by the points it carries, ``mixed`` if both, and
    ``unvocalised`` if neither.
    """
    if not _LETTER.search(text):
        return None
    west, east = bool(_WEST.search(text)), bool(_EAST.search(text))
    if west and east:
        return MIXED
    if west:
        return WEST
    if east:
        return EAST
    return UNVOCALISED


__all__ = ["EAST", "MIXED", "UNVOCALISED", "WEST", "vocalisation"]
