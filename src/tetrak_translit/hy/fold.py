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
2. **Latin written in ISO 9985 or Hübschmann-Meillet**, which spell ``ձ``
   ``j`` where ALA-LC and BGN/PCGN spell ``ջ`` ``j``, is recognised by a
   mark only those two schemes make (``č ǰ š ž ġ ł ə ë ç``, the
   Hübschmann-Meillet aspiration ``ʿ``, ``c`` with an aspiration mark, or
   ISO ``ow``) anywhere in the text being folded, not only in the token:
   then its bare ``j`` is read as ``dz``.
3. **Latin** is lowercased and stripped of every diacritic and
   aspiration mark, an aspirate written with *h* loses it (``th``/``t``,
   ``ph``/``p``: *Thoumanian*), an *h* after *v* is dropped
   (``vh``/``v``: *Hovannes*), then its digraphs are collapsed onto one
   spelling each (``ž``/``zh``, ``x``/``kh``, ``ł``/``gh``,
   ``ow``/``ou``/``oo``/``u``, ``iw``/``iu``, ``w``/``v``, ``ivo``/``io``
   for the glide Western says in *Virkilivos*), a ``y`` with a
   consonant beside it and no vowel on either side is read as BGN/PCGN's
   ``ը`` and becomes ``e`` (*zhanry*, *ynker*), the voiced and voiceless
   pairs are merged (``b``/``p``, ``d``/``t``, ``g``/``k``,
   ``dz``/``ts``/``c``, ``j``/``ch``) because Eastern and Western
   pronunciation spellings disagree on exactly those, the glides are
   regularised (initial ``ye``/``e`` and ``vo``/``o``, where a hyphen or
   a bracket also starts a word, as BGN/PCGN and Western count it;
   initial ``iu``/``yu``; ``y`` before a vowel at the start of a word or after a
   hyphen becomes ``h``, and so does the lone initial ``Յ.``, which then
   shares its key with ``Հ.``; initial ``ho``/``o`` for the
   Russian-mediated *Ovanes* and *Ovsep*; ``ya``/``ea``/``ia``), a ``y``
   after ``iu`` at the end of a word is BGN/PCGN's ``ը`` and becomes
   ``e`` (*tʻiwy* for ``թիւը``), any other ``y`` after a vowel is dropped
   at the end of a word and before a hyphen or a bracket (the silent
   ``յ`` of *hay-ṛuseren*), doubled letters are
   collapsed and anything that is not a letter or digit is removed.

Known gaps, because a fold that claims there is a single right answer is
lying (LREC 2020, *cross-script name matching*, cited in Tetrak's
research): popular spellings that insert an unwritten schwa (*Megerdich*
for ``Մկրտիչ``) or come through Russian (*Khachaturian* for
``Խաչատրյան``) do not fold to the Armenian; a classical ``աւ`` that
reformed spelling turned into ``օ`` (``աւր``/``օր``) does not either;
and ISO 9985 or Hübschmann-Meillet ``j`` (which is ``ձ``) folds as if it
were ALA-LC ``j`` (which is ``ջ``) when nothing else in the text shows the
scheme (a lone *Jayn*) and ``scheme=`` does not say. The
test set in ``tests/data/hy_fold_cases.tsv`` is the published claim; what
is not in it is not claimed.
"""

from __future__ import annotations

import re
import unicodedata

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
    # ALA-LC 2022's soft sign (patʹsparan): gone before ts can be merged.
    "ʹ": "",
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

# Marks that only ISO 9985 and Hübschmann-Meillet make, so that in Latin
# text carrying one, a bare j is their ձ and not ALA-LC's ջ. ǰ is matched
# precomposed and as j with a combining caron (the capital has no
# precomposed form). Bare c is left out: popular spellings use it.
_ISO_MARKS = re.compile(r"[čǰšžġłəëçʿ]|j\u030c|c[ʻʼʿ'’]|ow")
_BARE_J = re.compile(r"j(?!\u030c)")


# fold() passes the same text for every token, so remember the last answer.
_J_IS_DZ: dict[str, bool] = {}


def _j_is_dz(context: str) -> bool:
    if context not in _J_IS_DZ:
        _J_IS_DZ.clear()
        _J_IS_DZ[context] = bool(_ISO_MARKS.search(unicodedata.normalize("NFC", context).lower()))
    return _J_IS_DZ[context]


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
    # Classical իւ, which the Armenian side has already made յու: iw in the
    # schemes that write ւ as w, iu in Western, both yu at the start of a word.
    (re.compile(r"iw"), "iu"),
    (re.compile(r"w"), "v"),
    # Western writes ո after a vowel as vo (Virkilivos for Վիրգիլիոս), the
    # glide it is said with; the script and the other schemes write io. Both
    # sides pass through here, so Լիվոռնո and Livorno still agree (liorno).
    (re.compile(r"ivo"), "io"),
    # BGN/PCGN writes ը as y, which the other schemes give a vowel letter.
    # A y with a consonant beside it and no vowel on either side cannot be
    # the glide յ (zhanry, ynker, Hayy). Punctuation is still in the token
    # here, so a lone y, the initial Յ., has neither and is left alone.
    (re.compile(r"(?<=[b-df-hj-np-tv-z])y(?![aeiou])|(?<![a-z])y(?=[b-df-hj-np-tv-z])"), "e"),
    # BGN/PCGN and Western write an initial ե as ye and an initial ո as vo,
    # and their renderers count a hyphen or a bracket as a word boundary
    # (Ter-Yeghishe, hay[yeren], ark'[yepiskopos]); so does the fold.
    (re.compile(r"(?<![a-z])yev"), "ev"),
    (re.compile(r"(?<![a-z])ye"), "e"),
    (re.compile(r"(?<![a-z])vo"), "o"),
    (re.compile(r"^iu"), "yu"),
    # An initial Յ is said h (Յակոբ is Hakob), also after a hyphen
    # (Տէր-Յակոբեան), and ALA-LC 2022 writes it Ḥ. The lone initial Յ. goes
    # the same way, so that Ḥ. and H. find it; it then shares a key with Հ.,
    # which is declared.
    (re.compile(r"(?<![a-z])y(?=[aeiou])"), "h"),
    (re.compile(r"^y(?![a-z])"), "h"),
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
    # BGN/PCGN's y for ը can follow a vowel only after the ւ of classical
    # իւ (tʻiwy for թիւը), which has just become iu; the article is kept as
    # the vowel the other schemes write, before the silent յ is dropped.
    (re.compile(r"(?<=iu)y(?![a-z])"), "e"),
    # A final յ after a vowel is silent and the Armenian side drops it; so
    # here, also before a hyphen or a bracket (hay-ṛuseren, hay[erēn]).
    (re.compile(r"(?<=[aeiou])y(?![a-z])"), ""),
    *FINISH,
)


def fold_token(token: str, context: str | None = None) -> str:
    """Fold one whitespace-free token, Armenian or Latin, to its key.

    Args:
        token: The token.
        context: The whole text the token came from, which is where the
            marks that show a Latin ``j`` is ``ձ`` are looked for. The token
            alone when omitted.
    """
    token = SCRIPT.expand(token)
    if SCRIPT.has_letters(token):
        token = render(apply(token.lower(), _ORTHOGRAPHY), _BASIS)
    elif _j_is_dz(token if context is None else context):
        token = _BARE_J.sub("dz", unicodedata.normalize("NFC", token).lower())
    return apply(clean(token, _LETTERS), _LATIN)


__all__ = ["fold_token"]
