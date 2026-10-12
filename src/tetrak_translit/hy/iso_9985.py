"""ISO 9985: the international standard, one Latin letter per Armenian one.

Written from ISO 9985:2026, *Information and documentation -- Transliteration
of Armenian characters into Latin characters*, second edition, Table 1.
Every Armenian letter has a distinct rendering, by diacritic where the
plain letters run out, so the table reverses exactly; that is what the
standard was designed for and the reason to choose it for round-tripping.
``ու`` is ``ow`` and ``օ`` is ``ō``, which look odd to anyone used to the
library form but keep the mapping one-to-one.

The second edition marks every aspirate the same way: the unaspirated
letter is plain and its aspirated partner takes a neutral apostrophe
(U+0027). The first edition did that only for *p*, *t* and *k*; the
2026 edition extends it to ``ծ``/``ց`` (``c``/``c'``) and ``ճ``/``չ``
(``č``/``č'``), where 1996 wrote ``ç`` and ``č̣`` for the unaspirated
letters. ``օ`` moved from ``ò`` to ``ō``. Data romanised under the first
edition is read by :mod:`.iso_9985_1996`.

Punctuation follows Table 2, mark for mark and where it stands: the full
stop ``։`` is ``.``, the comma ``՝`` is ``:``, the dot ``․`` (U+2024)
is ``;``, the hyphen ``֊`` is ``-``, and the stress marks set over a
vowel stay there, ``՞`` as ``?``, ``՜`` as ``!`` and ``՛`` as ``ˆ``
(U+02C6), so ``կարդացե՞լ`` is ``kardac'e?l``. Reading back maps each of
those Latin marks to its Armenian one, a full stop to ``։`` included;
other characters pass through both ways.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "'"

ISO_9985 = Scheme(
    script=SCRIPT,
    key="iso_9985",
    name="ISO 9985",
    version="2.1",
    standard="ISO 9985:2026",
    reversible=True,
    letters={
        "ա": "a",
        "բ": "b",
        "գ": "g",
        "դ": "d",
        "ե": "e",
        "զ": "z",
        "է": "ē",
        "ը": "ë",
        "թ": "t" + ASPIRATION,
        "ժ": "ž",
        "ի": "i",
        "լ": "l",
        "խ": "x",
        "ծ": "c",
        "կ": "k",
        "հ": "h",
        "ձ": "j",
        "ղ": "ġ",
        "ճ": "č",
        "մ": "m",
        "յ": "y",
        "ն": "n",
        "շ": "š",
        "ո": "o",
        "չ": "č" + ASPIRATION,
        "պ": "p",
        "ջ": "ǰ",
        "ռ": "ṙ",
        "ս": "s",
        "վ": "v",
        "տ": "t",
        "ր": "r",
        "ց": "c" + ASPIRATION,
        "ւ": "w",
        "փ": "p" + ASPIRATION,
        "ք": "k" + ASPIRATION,
        "օ": "ō",
        "ֆ": "f",
    },
    digraphs={"ու": "ow", "և": "ew"},
    # Table 2.
    punctuation={
        ",": ",",
        "․": ";",
        "՝": ":",
        "։": ".",
        "՞": "?",
        "՜": "!",
        "՛": "ˆ",
        "֊": "-",
    },
    notes=(
        "One-to-one by design, so it reverses exactly. Choose it for round-tripping "
        "and data exchange, not for readers: ու is ow, խ is x, ձ is j."
    ),
)
