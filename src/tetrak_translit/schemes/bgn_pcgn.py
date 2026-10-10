"""BGN/PCGN: the geographic names system, the source of *Yerevan*.

Written from the BGN/PCGN 1981 romanisation system for Armenian, agreed by
the United States Board on Geographic Names and the Permanent Committee on
Geographical Names for British Official Use. It is a pronunciation-led
system for reformed (Eastern) Armenian and the only standard here with
positional rules: ``ե`` is ``ye`` and ``ո`` is ``vo`` at the start of a
word, and ``և`` is ``yev`` there, ``ev`` elsewhere. ``ռ`` is ``rr``, ``ը``
is ``y`` and aspiration is a plain apostrophe. Lossy: ``y`` is both ``ը``
and ``յ``, and the digraphs are as ambiguous as ALA-LC's.
"""

from __future__ import annotations

from . import Scheme

ASPIRATION = "'"

BGN_PCGN = Scheme(
    key="bgn_pcgn",
    name="BGN/PCGN",
    version="1.0",
    standard="BGN/PCGN 1981 System (Armenian)",
    reversible=False,
    letters={
        "ա": "a",
        "բ": "b",
        "գ": "g",
        "դ": "d",
        "ե": "e",
        "զ": "z",
        "է": "e",
        "ը": "y",
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
        "ռ": "rr",
        "ս": "s",
        "վ": "v",
        "տ": "t",
        "ր": "r",
        "ց": "ts" + ASPIRATION,
        "ւ": "w",
        "փ": "p" + ASPIRATION,
        "ք": "k" + ASPIRATION,
        "օ": "o",
        "ֆ": "f",
    },
    digraphs={"ու": "u", "և": "ev"},
    initial={"ե": "ye", "ո": "vo", "և": "yev"},
    notes=(
        "Place names and maps: Yerevan, Vanadzor, Gyumri. Word-initial ե, ո and և "
        "are ye, vo and yev. Lossy: y is both ը and յ."
    ),
)
