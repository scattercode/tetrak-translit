"""The Georgian script descriptor."""

from __future__ import annotations

from ..script import Script

SCRIPT = Script(
    key="ka",
    name="Georgian",
    unicode_name="georgian",
    letters="აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ",
    # Every letter outside the modern alphabet that a scheme renders: the
    # five archaic letters, and the historical and phonetic letters of
    # ISO 9984:2026 Table 5.
    archaic="ჱჲჳჴჵჶჷჸჹჺჼჽჾჿ",
    vowels=frozenset("აეიოუ"),
    # Mkhedruli (with the archaic and extended letters) and Mtavruli.
    ranges=((0x10D0, 0x10FF), (0x1C90, 0x1CBF)),
    cased=False,
)

__all__ = ["SCRIPT"]
