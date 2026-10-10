"""ISO 9985: the international standard, one Latin letter per Armenian one.

Written from ISO 9985:1996, *Information and documentation -- Transliteration
of Armenian characters into Latin characters*. Every Armenian letter has a
distinct rendering, by diacritic where the plain letters run out, so the
table reverses exactly; that is what the standard was designed for and the
reason to choose it for round-tripping. ``ու`` is ``ow`` and ``օ`` is
``ò``, which look odd to anyone used to the library form but keep the
mapping one-to-one. Aspiration is a plain apostrophe.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "'"

ISO_9985 = Scheme(
    script=SCRIPT,
    key="iso_9985",
    name="ISO 9985",
    version="1.0",
    standard="ISO 9985:1996",
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
        "ծ": "ç",
        "կ": "k",
        "հ": "h",
        "ձ": "j",
        "ղ": "ġ",
        "ճ": "č̣",  # č with dot below
        "մ": "m",
        "յ": "y",
        "ն": "n",
        "շ": "š",
        "ո": "o",
        "չ": "č",
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
        "օ": "ò",
        "ֆ": "f",
    },
    digraphs={"ու": "ow", "և": "ew"},
    notes=(
        "One-to-one by design, so it reverses exactly. Choose it for round-tripping "
        "and data exchange, not for readers: ու is ow, խ is x, ձ is j."
    ),
)
