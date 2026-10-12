"""The Georgian national system of romanisation (2002).

Written from the system adopted by the Georgian State Department of
Geodesy and Cartography and the Institute of Linguistics in 2002, and
taken up by BGN/PCGN in 2009; the spelling on Georgian road signs,
passports and maps. No diacritics, and the apostrophe marks the
**ejective** (``k' p' t' q' ts' ch'``) with the aspirates plain -- the
reverse of ALA-LC and ISO 9984:1996. ISO 9984:2026 is built on this
system and makes it reversible (see :mod:`.iso_9984`). *Tbilisi*, *Kutaisi* and *Batumi* are
this system; so is *Ts'ereteli*. Lossy: the digraphs are as ambiguous as
ALA-LC's, and the archaic letters are not defined.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

EJECTIVE = "'"

NATIONAL = Scheme(
    script=SCRIPT,
    key="national",
    name="Georgian national system",
    version="1.0",
    standard="Georgian national system of romanization (2002); BGN/PCGN 2009 agreement",
    reversible=False,
    letters={
        "ა": "a",
        "ბ": "b",
        "გ": "g",
        "დ": "d",
        "ე": "e",
        "ვ": "v",
        "ზ": "z",
        "თ": "t",
        "ი": "i",
        "კ": "k" + EJECTIVE,
        "ლ": "l",
        "მ": "m",
        "ნ": "n",
        "ო": "o",
        "პ": "p" + EJECTIVE,
        "ჟ": "zh",
        "რ": "r",
        "ს": "s",
        "ტ": "t" + EJECTIVE,
        "უ": "u",
        "ფ": "p",
        "ქ": "k",
        "ღ": "gh",
        "ყ": "q" + EJECTIVE,
        "შ": "sh",
        "ჩ": "ch",
        "ც": "ts",
        "ძ": "dz",
        "წ": "ts" + EJECTIVE,
        "ჭ": "ch" + EJECTIVE,
        "ხ": "kh",
        "ჯ": "j",
        "ჰ": "h",
    },
    notes=(
        "Road signs, passports and maps: Tbilisi, Kutaisi, Batumi. The apostrophe marks "
        "the ejective, the opposite of ALA-LC. Not reversible; ISO 9984 is its reversible form."
    ),
)
