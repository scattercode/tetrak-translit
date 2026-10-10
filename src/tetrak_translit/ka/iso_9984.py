"""ISO 9984: the international standard, one Latin letter per Georgian one.

Written from ISO 9984:1996, *Information and documentation --
Transliteration of Georgian characters into Latin characters*. Every
letter has a distinct rendering, so the table reverses exactly:
háčeks for the sibilants and affricates (``ž š č ǰ``), ``x`` for ``ხ``,
``ḡ`` for ``ღ``, ``q`` for ``ყ``, and an apostrophe on the aspirates
(``t' p' k' č' c'``), as in ALA-LC, against plain ejectives.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "'"

ISO_9984 = Scheme(
    script=SCRIPT,
    key="iso_9984",
    name="ISO 9984",
    version="1.0",
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
    },
    notes=(
        "One-to-one by design, so it reverses exactly. Choose it for round-tripping and "
        "data exchange, not for readers: ხ is x, ძ is j, წ is c."
    ),
)
