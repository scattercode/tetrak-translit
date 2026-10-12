"""The Georgian fold: one index form for every spelling of a word.

For what a fold is for, see :mod:`tetrak_translit.fold`. Georgian is a
simpler case than Armenian: one orthography, and no pronunciation
tradition that swaps consonants. What varies between spellings is the
marking of aspirate against ejective (``ʻ``, ``'`` or nothing, on
opposite members of each pair depending on the system), the sibilants
(``ž``/``zh``, ``š``/``sh``, ``č``/``ch``), ``x``/``kh``, ``ḡ``/``gh``,
and ISO 9984:1996's ``c``/``j`` for ALA-LC's ``ts``/``dz``. ISO 9984:2026
is the national system's spelling, with a middle dot that the fold
removes with the other punctuation.

So the rules are: Georgian is rendered through ALA-LC after the archaic
letters are folded onto their modern values; Latin is lowercased and
stripped of diacritics and apostrophes (which merges each aspirate with
its ejective), the sibilant spellings are collapsed, ``dz`` and ``j``
become one, ``ts`` and ``c`` become one, ``q`` becomes ``k`` (so
*Kazbegi* finds ``ყაზბეგი``), ``y`` becomes ``i``, ``w`` becomes ``v``,
doubled letters are collapsed and anything that is not a letter or digit
is removed.

Known gaps: Russian-mediated forms (*Tiflis* for ``თბილისი``, *Kutais*
for ``ქუთაისი``) and translated names (*George* for ``გიორგი``) do not
fold to the Georgian. The test set in ``tests/data/ka_fold_cases.tsv`` is
the published claim.
"""

from __future__ import annotations

import re

from ..engine import render
from ..latin import FINISH, Rules, apply, clean
from .ala_lc import ALA_LC
from .descriptor import SCRIPT

# Archaic letters to the modern letters that replaced them.
_ARCHAIC = str.maketrans({"ჱ": "ე", "ჲ": "ი", "ჳ": "ვ", "ჴ": "ხ", "ჵ": "ო"})

_LETTERS = {
    "ž": "zh",
    "š": "sh",
    "č": "ch",
    "ǰ": "j",
    "ḡ": "gh",
    "ẖ": "kh",
    "x": "kh",
}

_LATIN: Rules = (
    (re.compile(r"ch"), "\x01"),  # protected while c is merged into ts
    (re.compile(r"dz"), "j"),
    (re.compile(r"ts"), "c"),
    (re.compile(r"\x01"), "ch"),
    (re.compile(r"q"), "k"),
    (re.compile(r"y"), "i"),
    (re.compile(r"w"), "v"),
    *FINISH,
)


def fold_token(token: str) -> str:
    """Fold one whitespace-free token, Georgian or Latin, to its key."""
    if SCRIPT.has_letters(token):
        token = render(token.lower().translate(_ARCHAIC), ALA_LC)
    return apply(clean(token, _LETTERS), _LATIN)


__all__ = ["fold_token"]
