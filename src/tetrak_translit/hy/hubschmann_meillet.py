"""Hübschmann-Meillet: the scholarly transcription used in Armenian studies.

Written from the system of Heinrich Hübschmann's *Armenische Grammatik*
(1897) as standardised by Antoine Meillet's *Altarmenisches
Elementarbuch* (1913), in the form the *Revue des Études Arméniennes* and
most linguistic literature use. One letter per letter, with Czech-style
háčeks for the palatals (``ž``, ``š``, ``č``, ``ǰ``), ``x`` for ``խ``,
``ł`` for ``ղ``, ``c`` for ``ծ`` and ``j`` for ``ձ``, and aspiration
marked with the modifier letter left half ring ``ʿ`` (U+02BF). ``ու`` is
``u``, so a classical ``ու`` cannot be told from ``ո``+``ւ`` -- but
reformed orthography never writes a free ``ւ`` after ``ո``, and the
classical digraph is the same two letters, so the table reverses exactly.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

ASPIRATION = "ʿ"  # ʿ

HUBSCHMANN_MEILLET = Scheme(
    script=SCRIPT,
    key="hubschmann_meillet",
    name="Hübschmann-Meillet",
    version="1.0",
    standard="Hübschmann (1897) and Meillet (1913), as used in the Revue des Études Arméniennes",
    reversible=True,
    letters={
        "ա": "a",
        "բ": "b",
        "գ": "g",
        "դ": "d",
        "ե": "e",
        "զ": "z",
        "է": "ē",
        "ը": "ə",
        "թ": "t" + ASPIRATION,
        "ժ": "ž",
        "ի": "i",
        "լ": "l",
        "խ": "x",
        "ծ": "c",
        "կ": "k",
        "հ": "h",
        "ձ": "j",
        "ղ": "ł",
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
    digraphs={"ու": "u", "և": "ew"},
    notes=(
        "Linguistics and classical Armenian scholarship. One letter per letter, so it "
        "reverses exactly. Aspiration marked with ʿ (U+02BF)."
    ),
)
