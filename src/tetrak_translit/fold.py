"""The canonical fold: one index form for every spelling of an Armenian word.

This is the function a search index calls, at index time and at query
time, so that a record catalogued as ``Պօղոսեան`` is found by a reader who
types *Poghosyan*, *Boghossian*, *Pōghosean* or ``Պողոսյան``. It is for
**finding**, not display: the key it returns is a deliberately coarse
Latin skeleton that nobody should ever show to a reader. The schemes in
:mod:`tetrak_translit.schemes` are for display; this is the other half of
the job, and the two must not be confused.

How it works, in order:

1. **Armenian input** is first normalised across the 1922 reform, towards
   the reformed spelling: ``եւ`` becomes ``և``, ``է`` becomes ``ե``,
   ``եա`` becomes ``յա`` and ``իւ`` becomes ``յու`` (the classical
   digraphs for *ya* and *yu*), ``եո`` becomes ``եվո`` (*Գէորգ* is
   *Gevorg*), and a word-final ``յ`` after a vowel is dropped (``ծառայ``
   is ``ծառա``). Then it is rendered through ALA-LC, so that Armenian and
   ALA-LC Latin reach the next step by the same road.
2. **Latin input written in a reversible scheme** can be named with
   ``scheme=``; it is read back into Armenian exactly and treated as
   above. Without a scheme hint, Latin is folded heuristically.
3. **Latin** is lowercased and stripped of every diacritic and
   aspiration mark, then its digraphs are collapsed onto one spelling
   each (``ž``/``zh``, ``x``/``kh``, ``ł``/``gh``, ``ow``/``ou``/``oo``/``u``,
   ``w``/``v``), the voiced and voiceless pairs are merged (``b``/``p``,
   ``d``/``t``, ``g``/``k``, ``dz``/``ts``/``c``, ``j``/``ch``) because
   Eastern and Western pronunciation spellings disagree on exactly those,
   the glides are regularised (initial ``ye``/``e``, initial ``vo``/``o``,
   initial ``y``/``h``, ``ya``/``ea``/``ia``), a final ``y`` after a vowel
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
test set in ``tests/data/fold_cases.tsv`` is the published claim; what is
not in it is not claimed.
"""

from __future__ import annotations

import re
import unicodedata

from .schemes import ALA_LC
from .transliterate import get_scheme, to_armenian, to_latin

_ARMENIAN_LETTER = re.compile(r"[Ա-ֈ]")
_TOKEN = re.compile(r"\S+")

# Classical-orthography spellings, lowercase, towards their reformed forms.
# Applied in this order; see the module docstring.
_ORTHOGRAPHY = (
    (re.compile(r"եւ"), "և"),
    (re.compile(r"է"), "ե"),
    (re.compile(r"եա"), "յա"),
    (re.compile(r"իւ"), "յու"),
    (re.compile(r"եո"), "եվո"),
    (re.compile(r"(?<=[աոեիօ])յ(?![ա-ֈ])"), ""),
)

# Letters outside ASCII that NFKD does not decompose, and the ISO 9985 and
# Hübschmann-Meillet letters whose diacritic carries the whole distinction.
# Mapped before the diacritics are stripped, or ž would become z.
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
_APOSTROPHES = re.compile(r"['’‘ʻʿʼˀ`´]")

# The Latin skeleton rules, applied in this order to one lowercase token.
_LATIN = (
    (re.compile(r"ow|ou|oo"), "u"),
    (re.compile(r"ew"), "ev"),
    (re.compile(r"w"), "v"),
    (re.compile(r"^yev"), "ev"),
    (re.compile(r"^ye"), "e"),
    (re.compile(r"^vo"), "o"),
    (re.compile(r"^y(?=[aeiou])"), "h"),
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
    (re.compile(r"[^a-z0-9]"), ""),
    (re.compile(r"(.)\1+"), r"\1"),
)


def _fold_armenian(token: str) -> str:
    lowered = token.lower()
    for pattern, replacement in _ORTHOGRAPHY:
        lowered = pattern.sub(replacement, lowered)
    return to_latin(lowered, ALA_LC)


def _fold_latin(token: str) -> str:
    lowered = unicodedata.normalize("NFC", token).lower()
    lowered = "".join(_LETTERS.get(character, character) for character in lowered)
    lowered = unicodedata.normalize("NFKD", lowered)
    lowered = "".join(character for character in lowered if not unicodedata.combining(character))
    lowered = _APOSTROPHES.sub("", lowered)
    for pattern, replacement in _LATIN:
        lowered = pattern.sub(replacement, lowered)
    return lowered


def fold_token(token: str) -> str:
    """Fold one whitespace-free token. Empty when nothing survives."""
    if _ARMENIAN_LETTER.search(token):
        token = _fold_armenian(token)
    return _fold_latin(token)


def fold(text: str, scheme: str | None = None) -> str:
    """Fold *text* onto its canonical index form.

    Args:
        text: Armenian in either orthography, Latin in any of the
            romanisations, or a mixture. Tokens are folded one at a time
            and joined with single spaces.
        scheme: Optional. When the Latin in *text* is known to be written
            in a reversible scheme (``"iso_9985"`` or
            ``"hubschmann_meillet"``), name it and the text is read back
            into Armenian exactly before folding, which removes the one
            ambiguity the heuristic fold has (``j``). Ignored for
            Armenian input; for a lossy scheme the heuristic fold is used.

    Returns:
        A lowercase ASCII key: for comparing and indexing, never for
        display.
    """
    text = unicodedata.normalize("NFC", text)
    if scheme is not None and not _ARMENIAN_LETTER.search(text):
        table = get_scheme(scheme)
        if table.reversible:
            text = to_armenian(text, table)
    keys = (fold_token(match.group()) for match in _TOKEN.finditer(text))
    return " ".join(key for key in keys if key)


__all__ = ["fold", "fold_token"]
