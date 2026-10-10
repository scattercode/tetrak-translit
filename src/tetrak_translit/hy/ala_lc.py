"""ALA-LC: the Library of Congress romanisation, what library catalogues hold.

Written from the ALA-LC Romanization Tables, *Armenian* (approved 2011),
published by the Library of Congress. Aspiration is marked with the
modifier letter turned comma ``ʻ`` (U+02BB), which is the character the
table uses and the one catalogue records carry; a plain apostrophe is
accepted on input by the fold.

The table has no positional rules: ``ե`` is ``e`` and ``ո`` is ``o`` in
every position, which is why the Library of Congress writes *Erevan* and
*Oskan* where BGN/PCGN writes *Yerevan* and *Voskan*. The ligature ``և``
is ``ev`` but the letter ``ւ`` is ``w``, so a classical-orthography
imprint spelling the city ``Երեւան`` romanises as *Erewan* -- a real
distinction in catalogue records, not an error, and one the fold equates.

Lossy: ``ts`` is both ``ծ`` and ``տ``+``ս``, ``dz`` both ``ձ`` and
``դ``+``զ``, ``kh`` both ``խ`` and ``կ``+``հ``, and so on, so the table
cannot be reversed with certainty.
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
    standard="ALA-LC Romanization Tables, Armenian (2011)",
    reversible=False,
    letters={
        "ա": "a",
        "բ": "b",
        "գ": "g",
        "դ": "d",
        "ե": "e",
        "զ": "z",
        "է": "ē",
        "ը": "ě",
        "թ": "t" + ASPIRATION,
        "ժ": "zh",
        "ի": "i",
        "լ": "l",
        "խ": "kh",
        "ծ": "ts",
        "կ": "k",
        "հ": "h",
        "ձ": "dz",
        "ղ": "gh",
        "ճ": "ch",
        "մ": "m",
        "յ": "y",
        "ն": "n",
        "շ": "sh",
        "ո": "o",
        "չ": "ch" + ASPIRATION,
        "պ": "p",
        "ջ": "j",
        "ռ": "ṙ",
        "ս": "s",
        "վ": "v",
        "տ": "t",
        "ր": "r",
        "ց": "ts" + ASPIRATION,
        "ւ": "w",
        "փ": "p" + ASPIRATION,
        "ք": "k" + ASPIRATION,
        "օ": "ō",
        "ֆ": "f",
    },
    digraphs={"ու": "u", "և": "ev"},
    notes=(
        "The form in library catalogues (Koha, WorldCat, the Library of Congress). "
        "No positional rules; aspiration marked with ʻ (U+02BB). Lossy: ts, dz, kh, "
        "ch and sh can each be one letter or two."
    ),
)
