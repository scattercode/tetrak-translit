"""ALA-LC: the Library of Congress romanisation of Russian.

Written from the ALA-LC Romanization Tables, *Russian* (2012 version),
which superseded the 2011 and 1997 tables. It covers the four letters the
1918 reform removed -- ``і`` (*ī*), ``ѣ`` (*i͡e*), ``ѳ`` (*ḟ*) and ``ѵ``
(*ẏ*) -- so pre-reform and émigré imprints romanise under the same table
as Soviet ones. Since 2012 a hard sign at the end of a word is romanised
like any other (*ʺ*); the earlier tables disregarded it, so catalogue
records made before 2012 write *Mir* where this table writes *Mirʺ*.

The soft and hard signs are the modifier letters prime ``ʹ`` (U+02B9) and
double prime ``ʺ`` (U+02BA). ``ц``, ``ю``, ``я`` and ``ѣ`` are written
with a tie over two letters, encoded as the combining double inverted
breve U+0361 (*t͡s*, *i͡u*, *i͡a*, *i͡e*), the Unicode form the MARC
mapping has used since 2004; older records carry the ligature halves
U+FE20 and U+FE21 instead. A capital takes both letters of a tie in
capitals, as the table's upper-case column gives them: *T͡Svetaeva*.

Lossy: without the tie, ``ts`` is ``ц`` or ``т`` and ``с``, and *shch*
is ``щ`` or ``ш`` and ``ч``.
"""

from __future__ import annotations

from ..script import Rule, Scheme
from .descriptor import SCRIPT

TIE = "͡"
SOFT_SIGN = "ʹ"
HARD_SIGN = "ʺ"

ALA_LC = Scheme(
    script=SCRIPT,
    key="ala_lc",
    name="ALA-LC",
    version="1.0",
    standard="ALA-LC Romanization Tables, Russian (2012)",
    reversible=False,
    letters={
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "ë",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "ĭ",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "t" + TIE + "s",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": HARD_SIGN,
        "ы": "y",
        "ь": SOFT_SIGN,
        "э": "ė",
        "ю": "i" + TIE + "u",
        "я": "i" + TIE + "a",
        # The letters the 1918 reform removed.
        "і": "ī",
        "ѣ": "i" + TIE + "e",
        "ѳ": "ḟ",
        "ѵ": "ẏ",
    },
    rules=(
        Rule("ц", "T" + TIE + "S", capital=True),
        Rule("ю", "I" + TIE + "U", capital=True),
        Rule("я", "I" + TIE + "A", capital=True),
        Rule("ѣ", "I" + TIE + "E", capital=True),
    ),
    notes=(
        "The form in library catalogues, for modern and pre-1918 spelling alike. Ties "
        "over t͡s, i͡u, i͡a and i͡e (U+0361); soft and hard signs ʹ and ʺ. Lossy: without "
        "the tie, ts is one letter or two, and shch is щ or ш and ч."
    ),
)
