"""ALA-LC: the Library of Congress romanisation of Georgian.

Written from the ALA-LC Romanization Tables, *Georgian* (approved 2011).
The aspirated consonants ``თ ფ ქ ჩ ც`` carry the modifier letter turned
comma ``ʻ`` (U+02BB); the ejectives ``ტ პ კ ჭ წ`` are the plain letters.
That is the opposite convention from the national system, where the
apostrophe marks the ejective, and the commonest source of confusion
between the two. Lossy: ``dz``, ``zh``, ``gh``, ``sh`` and ``kh`` can each
be one letter or two.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "ʻ"  # ʻ

ALA_LC = Scheme(
    script=SCRIPT,
    key="ala_lc",
    name="ALA-LC",
    version="1.0",
    standard="ALA-LC Romanization Tables, Georgian (2011)",
    reversible=False,
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
        "ჟ": "zh",
        "რ": "r",
        "ს": "s",
        "ტ": "t",
        "უ": "u",
        "ფ": "p" + ASPIRATION,
        "ქ": "k" + ASPIRATION,
        "ღ": "gh",
        "ყ": "q",
        "შ": "sh",
        "ჩ": "ch" + ASPIRATION,
        "ც": "ts" + ASPIRATION,
        "ძ": "dz",
        "წ": "ts",
        "ჭ": "ch",
        "ხ": "kh",
        "ჯ": "j",
        "ჰ": "h",
        # Archaic letters, as the table renders them.
        "ჱ": "ē",
        "ჲ": "y",
        "ჳ": "w",
        "ჴ": "ẖ",
        "ჵ": "ō",
    },
    notes=(
        "The form in library catalogues. Aspirates marked with ʻ (U+02BB), ejectives "
        "plain: Tʻbilisi, Kʻutʻaisi. Lossy: dz, zh, gh, sh and kh can be one letter or two."
    ),
)
