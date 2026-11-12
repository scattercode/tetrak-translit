"""ISO 9984: the international standard for Georgian, reversible.

Written from ISO 9984:2026, *Information and documentation --
Transliteration of Georgian characters into Latin characters*, second
edition, Tables 4 and 5. The second edition is based on the Georgian
national system of 2002 (see :mod:`.national`), with what it takes to
make that system reversible. So it has the national system's digraphs
(``zh sh ch ts dz kh gh``) and its apostrophe on the **ejective**
(``k' p' t' q' ts' ch'``) with the aspirates plain -- the reverse of the
first edition, which marked the aspirate (:mod:`.iso_9984_1996`).

Reversibility comes from a middle dot (U+00B7) between two letters whose
renderings would otherwise read as a digraph: ``z·h`` for ``ზ`` and
``ჰ``, which is not ``zh`` (``ჟ``). The standard lists the pairs: ``გ``,
``ზ``, ``ს`` or ``ქ`` before ``ჰ``, ``თ`` before ``ს`` and ``დ`` before
``ზ``. Two sequences the list does not cover still read two ways:
``tsh`` is ``თ`` and ``შ`` or ``ც`` and ``ჰ``, and ``dzh`` is ``დ`` and
``ჟ`` or ``ძ`` and ``ჰ``. The table is written as published, with no dot
in either, and reading back takes the first of each, which is the one
Georgian itself has: ``თშ`` is in every noun in ``-თ`` that takes the
postposition ``-ში`` (``საათში``, in an hour; ``საფრანგეთში``, in
France) and in compounds (``ხუთშაბათი``, Thursday). The other reading
turns up only in borrowed names, mostly German (``ალცჰაიმერი``,
Alzheimer; ``ერცჰერცოგი``, archduke), and those do not read back: the
titles of the Georgian Wikipedia in November 2026 had 82 words with
``თშ`` against 19 with ``ცჰ``, and seven with ``დჟ`` against one with
``ძჰ``. A middle dot typed by hand settles either one, since the dot is
skipped in reading: ``ts·h`` reads as ``ცჰ``.

Table 5 gives the historical and phonetic letters that standard Georgian
does not use. The first six are unchanged from the first edition.
Capitals are optional (4.1.2): Mkhedruli has no case, and output is in
lower case unless the source was set in Mtavruli.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

EJECTIVE = "'"

ISO_9984 = Scheme(
    script=SCRIPT,
    key="iso_9984",
    name="ISO 9984",
    version="2.0",
    standard="ISO 9984:2026",
    reversible=True,
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
        # Table 5: letters standard Georgian does not use.
        "ჱ": "ē",
        "ჲ": "y",
        "ჳ": "w",
        "ჴ": "ẖ",
        "ჵ": "ō",
        "ჶ": "f",
        "ჷ": "ȳ",
        "ჸ": "ʔ",
        "ჹ": "ĝ",
        "ჺ": "ʕ",
        "ჼ": "ⁿ",
        "ჽ": "æ",
        "ჾ": "ʸ",
        "ჿ": "ʷ",
    },
    separator="·",
    separate=frozenset({("გ", "ჰ"), ("ზ", "ჰ"), ("ს", "ჰ"), ("ქ", "ჰ"), ("თ", "ს"), ("დ", "ზ")}),
    # The two sequences the standard's list leaves ambiguous, read as the
    # letters Georgian words have (see the module docstring).
    readings={"tsh": "თშ", "dzh": "დჟ"},
    notes=(
        "Reversible, and since 2026 built on the national system: the apostrophe marks "
        "the ejective, and a middle dot separates letters that would read as a digraph "
        "(z·h is ზჰ, not ჟ). Choose it for round-tripping and data exchange. Two "
        "sequences the standard leaves ambiguous are read as Georgian words have them: "
        "tsh as თშ and dzh as დჟ, so a borrowed name with ცჰ or ძჰ does not read back."
    ),
)
