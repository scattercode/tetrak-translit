"""The Armenian fold: one index form for every spelling of a word.

For what a fold is for, see :mod:`tetrak_translit.fold`. This module is
the Armenian rules. In order:

1. **Armenian input** is normalised across the 1922 reform, towards the
   reformed spelling: ``եւ`` becomes ``և``, ``է`` becomes ``ե``, ``եա``
   becomes ``յա`` and ``իւ`` becomes ``յու`` (the classical digraphs for
   *ya* and *yu*), ``եո`` becomes ``եվո`` (*Գէորգ* is *Gevorg*), and a
   word-final ``յ`` after a vowel is dropped (``ծառայ`` is ``ծառա``).
   Then it is rendered through ALA-LC -- the 2011 table, frozen in this
   module so that a new edition of the display table never moves a key
   -- so that Armenian and ALA-LC Latin reach the next step by the same
   road.
2. **Latin** is lowercased and stripped of every diacritic and
   aspiration mark, an aspirate written with *h* loses it (``th``/``t``,
   ``ph``/``p``: *Thoumanian*), an *h* after *v* is dropped
   (``vh``/``v``: *Hovannes*), then its digraphs are collapsed onto one
   spelling each (``ž``/``zh``, ``x``/``kh``, ``ł``/``gh``,
   ``ow``/``ou``/``oo``/``u``, ``w``/``v``), the voiced and voiceless pairs are merged (``b``/``p``,
   ``d``/``t``, ``g``/``k``, ``dz``/``ts``/``c``, ``j``/``ch``) because
   Eastern and Western pronunciation spellings disagree on exactly those,
   the glides are regularised (initial ``ye``/``e``, initial ``vo``/``o``,
   initial ``y``/``h``, initial ``ho``/``o`` for the Russian-mediated
   *Ovanes* and *Ovsep*, ``ya``/``ea``/``ia``), a final ``y`` after a vowel
   is dropped, doubled letters are collapsed and anything that is not a
   letter or digit is removed.

Known gaps, because a fold that claims there is a single right answer is
lying (LREC 2020, *cross-script name matching*, cited in Tetrak's
research): popular spellings that insert an unwritten schwa (*Megerdich*
for ``Մկրտիչ``) or come through Russian (*Khachaturian* for
``Խաչատրյան``) do not fold to the Armenian; a classical ``աւ`` that
reformed spelling turned into ``օ`` (``աւր``/``օր``) does not either;
and ISO 9985 or Hübschmann-Meillet ``j`` (which is ``ձ``) folds as if it
were ALA-LC ``j`` (which is ``ջ``) unless ``scheme=`` says otherwise. The
test set in ``tests/data/hy_fold_cases.tsv`` is the published claim; what
is not in it is not claimed.
"""

from __future__ import annotations

import re

from ..engine import render
from ..latin import FINISH, Rules, apply, clean
from ..script import Scheme
from .descriptor import SCRIPT

# The road Armenian takes into Latin before the skeleton rules: the
# ALA-LC table as it stood in 2011, frozen here. The fold's keys are data
# other systems store, so they must not move when the display table
# follows a new edition of its standard; :mod:`.ala_lc` is free to change
# and this is not. It is never registered as a scheme.
_BASIS = Scheme(
    script=SCRIPT,
    key="fold_basis",
    name="Fold basis (ALA-LC 2011)",
    version="1.0",
    standard="ALA-LC Romanization Tables, Armenian (2011), frozen for the fold",
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
        "թ": "tʻ",
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
        "չ": "chʻ",
        "պ": "p",
        "ջ": "j",
        "ռ": "ṙ",
        "ս": "s",
        "վ": "v",
        "տ": "t",
        "ր": "r",
        "ց": "tsʻ",
        "ւ": "w",
        "փ": "pʻ",
        "ք": "kʻ",
        "օ": "ō",
        "ֆ": "f",
    },
    digraphs={"ու": "u", "և": "ev"},
)

# Classical-orthography spellings, lowercase, towards their reformed forms.
_ORTHOGRAPHY: Rules = (
    (re.compile(r"եւ"), "և"),
    (re.compile(r"է"), "ե"),
    (re.compile(r"եա"), "յա"),
    (re.compile(r"իւ"), "յու"),
    (re.compile(r"եո"), "եվո"),
    (re.compile(r"(?<=[աոեիօ])յ(?![ա-ֈ])"), ""),
)

# Letters outside ASCII that NFKD does not decompose, and the ISO 9985 and
# Hübschmann-Meillet letters whose diacritic carries the whole distinction.
_LETTERS = {
    "ž": "zh",
    "š": "sh",
    "č": "ch",
    "ǰ": "j",
    "ġ": "gh",
    "ł": "gh",
    "ç": "c",
    "ə": "e",
    "x": "kh",
}

# The Latin skeleton rules, applied in this order to one lowercase token.
_LATIN: Rules = (
    # Older English and French spellings mark an aspirate with h (Thoumanian,
    # Thoros, Pharantsem), where the schemes use an apostrophe or nothing.
    (re.compile(r"th"), "t"),
    (re.compile(r"ph"), "p"),
    # An h after v is dropped by popular spellings (Hovannes for Hovhannes).
    (re.compile(r"vh"), "v"),
    (re.compile(r"ow|ou|oo"), "u"),
    (re.compile(r"ew"), "ev"),
    (re.compile(r"w"), "v"),
    (re.compile(r"^yev"), "ev"),
    (re.compile(r"^ye"), "e"),
    (re.compile(r"^vo"), "o"),
    (re.compile(r"^y(?=[aeiou])"), "h"),
    # Russian has no h, so Russian-mediated forms drop it: Ovanes, Ovsep.
    # Only before o; a general drop would merge իւր (his) with ուր (where).
    (re.compile(r"^ho"), "o"),
    (re.compile(r"dz"), "ts"),
    (re.compile(r"ts|tz"), "c"),
    (re.compile(r"j"), "ch"),
    (re.compile(r"gh"), "\x01"),  # protected while g is merged into k
    (re.compile(r"b"), "p"),
    (re.compile(r"d"), "t"),
    (re.compile(r"g"), "k"),
    (re.compile(r"\x01"), "gh"),
    (re.compile(r"eo"), "evo"),
    (re.compile(r"ya|ea"), "ia"),
    (re.compile(r"yo"), "io"),
    (re.compile(r"yu|eu"), "iu"),
    (re.compile(r"(?<=[aeiou])y$"), ""),
    *FINISH,
)


def fold_token(token: str) -> str:
    """Fold one whitespace-free token, Armenian or Latin, to its key."""
    if SCRIPT.has_letters(token):
        token = render(apply(token.lower(), _ORTHOGRAPHY), _BASIS)
    return apply(clean(token, _LETTERS), _LATIN)


__all__ = ["fold_token"]
