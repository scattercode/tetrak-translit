"""The Georgian script descriptor."""

from __future__ import annotations

from ..script import Script

SCRIPT = Script(
    key="ka",
    name="Georgian",
    unicode_name="georgian",
    letters="აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ",
    archaic="ჱჲჳჴჵ",
    vowels=frozenset("აეიოუ"),
    # Mkhedruli (with the archaic and extended letters) and Mtavruli.
    ranges=((0x10D0, 0x10FF), (0x1C90, 0x1CBF)),
    cased=False,
)

__all__ = ["SCRIPT"]
