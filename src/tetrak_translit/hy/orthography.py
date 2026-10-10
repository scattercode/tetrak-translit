"""Tell classical Armenian orthography from reformed, from the text alone.

The 1922 reform changed no letters, only where they appear, so a
classical string and a reformed one share a charset and differ in
distribution. For a long text that distribution can be measured; for a
catalogue title or a name there may be only one diagnostic letter, so
the verdict is made on presence, not on rate.

The discriminating marker is ``ւ`` (U+0582) outside the ``ու`` digraph
(tetrak-hy-trainer's ``orthography`` module, measured on 2026-10-08 for
Tetrak brief 014). Reformed spelling writes ``ւ`` only inside ``ու`` and
the ligature ``և``; classical spelling uses it freely -- ``նաւ``,
``իւր``, ``եւ``, ``հաւատք`` -- so one free ``ւ`` is enough to call a
string classical. The classical digraphs ``եա`` and ``եօ`` (reformed
``յա``, ``յո``) and an ``է`` inside a word (reformed ``ե``) are also
taken as classical. On long texts the trainer found inner ``է``
overlapping at the edges and left it out of the verdict; on a single
name there is no rate to measure, and a ``Գէորգ`` with no other tell is
better called classical than nothing.

Two tells point the other way: a ``յ`` between a consonant and a vowel
(reformed ``Պողոսյան``, where classical wrote ``եա``), and the ligature
``և``, which reformed presses set and some classical ones do too. Either
marks a string reformed when no classical tell is present; a string with
none is *indeterminate*, because ``Արմեն`` is spelled the same way under
both.

One marker that looks useful and is not, kept here so nobody re-tries
it: a word-final ``յ`` after a vowel is classical (``ծառայ``) but also
reformed (``հայ``, ``թեյ``). It is reported, never decides.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

CLASSICAL = "classical"
REFORMED = "reformed"
INDETERMINATE = "indeterminate"

_LETTER = r"[Ա-Ֆՠ-ֈ]"
#: ``ւ`` not preceded by ``ո``: a free yiwn, the classical tell.
_FREE_YIWN = re.compile(r"(?<![ոՈ])[ւՒ]")
_TWO_LETTER_EW = re.compile(r"[եԵ][ւՒ]")
_LIGATURE_EW = re.compile(r"և")
#: The classical digraphs for *ya* and *yo*, which reformed writes ``յա``/``յո``.
_CLASSICAL_DIGRAPH = re.compile(r"[եԵ][աօ]")
#: ``յ`` between a consonant and a vowel: the reformed ``յա``/``յո``/``յու``.
_MEDIAL_Y = re.compile(r"(?<=[բգդզթժլխծկհձղճմնշչպջռսվտրցփքֆ])յ(?=[աեէըիոօու])")
#: A vowel followed by ``յ`` at the end of a word.
_FINAL_Y = re.compile(rf"[աոեէիօ]յ(?!{_LETTER})")
#: ``է`` after another letter, where reformed spelling writes ``ե``.
_INNER_E = re.compile(rf"(?<={_LETTER})[էԷ]")


@dataclass(frozen=True)
class Markers:
    """Counts of the orthographic tells in one string."""

    free_yiwn: int
    two_letter_ew: int
    ligature_ew: int
    classical_digraph: int
    medial_y: int
    final_y: int
    inner_e: int


def markers(text: str) -> Markers:
    """Count the orthographic tells in *text*."""
    return Markers(
        free_yiwn=len(_FREE_YIWN.findall(text)),
        two_letter_ew=len(_TWO_LETTER_EW.findall(text)),
        ligature_ew=len(_LIGATURE_EW.findall(text)),
        classical_digraph=len(_CLASSICAL_DIGRAPH.findall(text)),
        medial_y=len(_MEDIAL_Y.findall(text)),
        final_y=len(_FINAL_Y.findall(text)),
        inner_e=len(_INNER_E.findall(text)),
    )


def orthography(text: str) -> str | None:
    """The orthography of the Armenian in *text*, or ``None`` if there is none.

    A free ``ւ`` (which a two-letter ``եւ`` always contains), a classical
    ``եա``/``եօ`` digraph or an inner ``է`` makes it classical. Failing
    that, a ``յ`` between a consonant and a vowel or the ligature ``և``
    makes it reformed. With no tell present the string is *indeterminate*:
    it reads the same under both orthographies.
    """
    if not re.search(_LETTER, text):
        return None
    tells = markers(text)
    if tells.free_yiwn or tells.classical_digraph or tells.inner_e:
        return CLASSICAL
    if tells.medial_y or tells.ligature_ew:
        return REFORMED
    return INDETERMINATE


__all__ = ["CLASSICAL", "INDETERMINATE", "REFORMED", "Markers", "markers", "orthography"]
