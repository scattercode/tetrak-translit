"""Say which script a string is in and, for Armenian, which orthography.

Cheap and deterministic: Unicode character names give the script, and a
few orthographic tells give the orthography. The 1922 reform changed no
letters, only where they appear, so classical and reformed Armenian share
a charset and differ in distribution. For a long text that distribution
can be measured; for a catalogue title or a name there may be only one
diagnostic letter, so the verdict is made on presence, not on rate.

The discriminating marker is ``ւ`` (U+0582) outside the ``ու`` digraph
(tetrak-hy-trainer's ``orthography`` module, measured on 2026-10-08 for
Tetrak brief 014). Reformed spelling writes ``ւ`` only inside ``ու`` and
the ligature ``և``; classical spelling uses it freely -- ``նաւ``,
``իւր``, ``եւ``, ``հաւատք`` -- so one free ``ւ`` is enough to call a
string classical. Two tells point the other way: a ``յ`` between a
consonant and a vowel (reformed ``Պողոսյան``, where classical wrote
``եա``), and the ligature ``և``, which reformed presses set and some
classical ones do too. Either marks a string reformed when no classical
tell is present; a string with none is reported *indeterminate*, because
``Արմեն`` is spelled the same way under both.

The classical digraphs ``եա`` and ``եօ`` (reformed ``յա``, ``յո``) and an
``է`` inside a word (reformed ``ե``) are also taken as classical. On long
texts the trainer found inner ``է`` overlapping at the edges and left it
out of the verdict; on a single name there is no rate to measure, and a
``Գէորգ`` with no other tell is better called classical than nothing.
One marker that looks useful and is not, kept here so nobody re-tries
it: a word-final ``յ`` after a vowel is classical (``ծառայ``) but also
reformed (``հայ``, ``թեյ``). It is reported, never decides.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

ARMENIAN = "armenian"
LATIN = "latin"
CYRILLIC = "cyrillic"
MIXED = "mixed"
NONE = "none"

CLASSICAL = "classical"
REFORMED = "reformed"
INDETERMINATE = "indeterminate"

#: ``ւ`` not preceded by ``ո``: a free yiwn, the classical tell.
_FREE_YIWN = re.compile(r"(?<![ոՈ])[ւՒ]")
_TWO_LETTER_EW = re.compile(r"[եԵ][ւՒ]")
_LIGATURE_EW = re.compile(r"և")
#: The classical digraphs for *ya* and *yo*, which reformed writes ``յա``/``յո``.
_CLASSICAL_DIGRAPH = re.compile(r"[եԵ][աօ]")
_ARMENIAN_LETTER = r"[Ա-Ֆՠ-ֈ]"
#: ``յ`` between a consonant and a vowel: the reformed ``յա``/``յո``/``յու``.
_MEDIAL_Y = re.compile(r"(?<=[բգդզթժլխծկհձղճմնշչպջռսվտրցփքֆ])յ(?=[աեէըիոօու])")
#: A vowel followed by ``յ`` at the end of a word.
_FINAL_Y = re.compile(rf"[աոեէիօ]յ(?!{_ARMENIAN_LETTER})")
#: ``է`` after a lowercase letter, where reformed spelling writes ``ե``.
_INNER_E = re.compile(r"(?<=[\u0531-\u0588])[էԷ]")


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


@dataclass(frozen=True)
class Detection:
    """What :func:`detect` found.

    Attributes:
        script: ``"armenian"``, ``"latin"``, ``"cyrillic"``, ``"mixed"``
            (letters from more than one of those) or ``"none"`` (no
            letters at all).
        dominant: The script with the most letters, or ``None`` when
            there are none. Equal to *script* unless that is ``"mixed"``.
        orthography: For a string with any Armenian letters,
            ``"classical"``, ``"reformed"`` or ``"indeterminate"``;
            otherwise ``None``.
        letters: Letter counts per script, for every script seen.
        markers: The orthographic tell counts the verdict was made on.
    """

    script: str
    dominant: str | None
    orthography: str | None
    letters: dict[str, int] = field(default_factory=dict)
    markers: Markers = field(default_factory=lambda: Markers(0, 0, 0, 0, 0, 0, 0))

    def as_dict(self) -> dict[str, object]:
        """A JSON-ready view, for the command line."""
        return {
            "script": self.script,
            "dominant": self.dominant,
            "orthography": self.orthography,
            "letters": dict(self.letters),
            "markers": vars(self.markers),
        }


def _script_of(character: str) -> str | None:
    """The script a letter belongs to, from its Unicode name.

    Modifier letters (the aspiration marks ``ʻ`` and ``ʿ``) are letters to
    Unicode but belong to no script, and are left out.
    """
    if not character.isalpha() or unicodedata.category(character) == "Lm":
        return None
    try:
        return unicodedata.name(character).split(" ", 1)[0].lower()
    except ValueError:
        return None


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
    makes it reformed. With no tell present the string
    is *indeterminate*: it reads the same under both orthographies.
    """
    if not re.search(_ARMENIAN_LETTER, text):
        return None
    tells = markers(text)
    if tells.free_yiwn or tells.classical_digraph or tells.inner_e:
        return CLASSICAL
    if tells.medial_y or tells.ligature_ew:
        return REFORMED
    return INDETERMINATE


def detect(text: str) -> Detection:
    """Detect the script of *text* and, for Armenian, its orthography.

    Args:
        text: Any string. Digits, punctuation and whitespace are ignored;
            only letters count.

    Returns:
        A :class:`Detection`.
    """
    text = unicodedata.normalize("NFC", text)
    counts: dict[str, int] = {}
    for character in text:
        script = _script_of(character)
        if script is not None:
            counts[script] = counts.get(script, 0) + 1

    if not counts:
        return Detection(NONE, None, None, {}, markers(text))

    dominant = max(counts, key=lambda script: (counts[script], script))
    script = dominant if len(counts) == 1 else MIXED
    return Detection(script, dominant, orthography(text), counts, markers(text))
