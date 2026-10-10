"""The Armenian script descriptor."""

from __future__ import annotations

from ..script import Script

SCRIPT = Script(
    key="hy",
    name="Armenian",
    unicode_name="armenian",
    # The thirty-eight lowercase letters, ա through ֆ. ւ (U+0582) is a
    # letter in classical orthography and half of ու in reformed; և
    # (U+0587) is the ligature of ե and ւ.
    letters="աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ",
    digraphs=("ու", "և"),
    vowels=frozenset("աեէըիոօ"),
    ranges=((0x0531, 0x0556), (0x0560, 0x0588)),
    cased=True,
)

__all__ = ["SCRIPT"]
