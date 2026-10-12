"""ISO 9984:1996: the first edition of the international standard.

Written from ISO 9984:1996, *Information and documentation --
Transliteration of Georgian characters into Latin characters*, which
ISO 9984:2026 cancelled and replaced (see :mod:`.iso_9984`). Kept
because records romanised under it remain in catalogues and data sets,
and only this table reads them back into Georgian. Every letter has a
distinct rendering, so the table reverses exactly: háčeks for the
sibilants and affricates (``ž š č ǰ``), ``x`` for ``ხ``, ``ḡ`` for
``ღ``, ``q`` for ``ყ``, and an apostrophe on the aspirates
(``t' p' k' č' c'``), as in ALA-LC, against plain ejectives -- the
opposite of the second edition.

``ჶ`` is ``f``: ISO 9984:2026 (Table 5) says its first six historical
letters are taken unchanged from this edition, and that is the sixth.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "'"

ISO_9984_1996 = Scheme(
    script=SCRIPT,
    key="iso_9984_1996",
    name="ISO 9984:1996",
    version="1.1",
    standard="ISO 9984:1996",
    reversible=True,
    letters={
        "ა": "a",
        "ბ": "b",
        "გ": "g",
        "დ": "d",
        "ე": "e",
        "ვ": "v",
        "ზ": "z",
        "თ": "t" + ASPIRATION,
        "ი": "i",
        "კ": "k",
        "ლ": "l",
        "მ": "m",
        "ნ": "n",
        "ო": "o",
        "პ": "p",
        "ჟ": "ž",
        "რ": "r",
        "ს": "s",
        "ტ": "t",
        "უ": "u",
        "ფ": "p" + ASPIRATION,
        "ქ": "k" + ASPIRATION,
        "ღ": "ḡ",
        "ყ": "q",
        "შ": "š",
        "ჩ": "č" + ASPIRATION,
        "ც": "c" + ASPIRATION,
        "ძ": "j",
        "წ": "c",
        "ჭ": "č",
        "ხ": "x",
        "ჯ": "ǰ",
        "ჰ": "h",
        "ჱ": "ē",
        "ჲ": "y",
        "ჳ": "w",
        "ჴ": "ẖ",
        "ჵ": "ō",
        "ჶ": "f",
    },
    notes=(
        "The superseded first edition, for reading and writing data made under it. "
        "One-to-one, so it reverses exactly; the apostrophe marks the aspirate."
    ),
)
