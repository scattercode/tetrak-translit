"""The Russian script descriptor."""

from __future__ import annotations

from ..script import Script

SCRIPT = Script(
    key="ru",
    name="Russian",
    unicode_name="cyrillic",
    letters="абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    # The four letters the 1918 reform removed: і, ѣ, ѳ and ѵ.
    archaic="іѣѳѵ",
    vowels=frozenset("аеёиоуыэюяіѣѵ"),
    # The Cyrillic block and the Cyrillic Supplement, less the thousands
    # sign and the combining marks of Church Slavonic (U+0482 to U+0489),
    # which are not letters. Every Cyrillic letter is in range, so text in
    # another language written in Cyrillic is detected as this script; the
    # letters Russian lacks (Ukrainian є, ї, ґ) pass through the schemes
    # unrendered.
    ranges=((0x0400, 0x0481), (0x048A, 0x052F)),
)

__all__ = ["SCRIPT"]
