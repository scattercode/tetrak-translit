"""BGN/PCGN: the geographic names system, the source of *Yekaterinburg*.

Written from the BGN/PCGN 1947 System for Russian, adopted by the United
States Board on Geographic Names in 1944 and the Permanent Committee on
Geographical Names for British Official Use in 1947, as published in
*Romanization of Russian* (checked for validity and accuracy, June 2019).
No ties and few diacritics: ``е`` is *ye* at the start of a word, after a
vowel and after ``й``, ``ъ`` and ``ь`` (Note 1), and *e* elsewhere; ``ё``
is *yë* and *ë* in the same places (Note 2). The soft and hard signs are
the right single and double quotation marks ``’`` (U+2019) and ``”``
(U+201D), as Note 5 and the table give them.

Note 3's middle dot is applied: it separates a ``й`` or ``ы`` from a
following ``а``, ``у``, ``ы`` or ``э``, an ``ы`` from a vowel before it,
an ``э`` from a consonant other than ``й`` before it, and ``т`` from
``с`` and ``ш`` from ``ч``, so that *y·a* is not ``я`` and *t·s* is not
``ц``. The note says these sequences "may" be so romanised; it is the
only way the table distinguishes them.

The table has no rendering for the letters the 1918 reform removed; they
pass through unrendered. Lossy: ``y`` is ``й`` and ``ы``, and ``e`` is
``е`` and ``э``.
"""

from __future__ import annotations

from ..script import Scheme
from .descriptor import SCRIPT

SOFT_SIGN = "’"
HARD_SIGN = "”"

_CONSONANTS = "бвгджзклмнпрстфхцчшщ"
_VOWELS = "аеёиоуыэюя"

BGN_PCGN = Scheme(
    script=SCRIPT,
    key="bgn_pcgn",
    name="BGN/PCGN",
    version="1.0",
    standard="BGN/PCGN 1947 System (Russian), checked June 2019",
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
        "й": "y",
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
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": HARD_SIGN,
        "ы": "y",
        "ь": SOFT_SIGN,
        "э": "e",
        "ю": "yu",
        "я": "ya",
    },
    # Notes 1 and 2: ye and yë after й, ъ and ь. The engine's after-vowel
    # rule covers the vowels; these three are rendered whole with the
    # letter after them.
    digraphs={
        "йе": "yye",
        "йё": "yyë",
        "ъе": HARD_SIGN + "ye",
        "ъё": HARD_SIGN + "yë",
        "ье": SOFT_SIGN + "ye",
        "ьё": SOFT_SIGN + "yë",
    },
    initial={"е": "ye", "ё": "yë"},
    after_vowel={"е": "ye", "ё": "yë"},
    separator="·",
    separate=frozenset(
        {(first, second) for first in "йы" for second in "ауыэ"}
        | {(vowel, "ы") for vowel in _VOWELS}
        | {(consonant, "э") for consonant in _CONSONANTS}
        | {("т", "с"), ("ш", "ч")}
    ),
    notes=(
        "The form on maps and in gazetteers: Yekaterinburg, Rostov-na-Donu. ye and yë "
        "initially, after vowels and after й, ъ, ь; signs as ’ and ”; middle dot in t·s, "
        "sh·ch, y·a. No pre-1918 letters. Lossy: y is й and ы, e is е and э."
    ),
)
