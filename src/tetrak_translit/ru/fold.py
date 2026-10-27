"""The Russian fold: one index form for every spelling of a word.

For what a fold is for, see :mod:`tetrak_translit.fold`. Russian names
reach a catalogue in more Latin spellings than any other script here:
ALA-LC in libraries (*Chaĭkovskiĭ*), BGN/PCGN on maps (*Yekaterinburg*),
ISO 9 and the scholarly transliteration in European libraries
(*Čajkovskij*), and the popular English, German and French forms
(*Tchaikovsky*, *Tschaikowski*). And the Cyrillic itself comes in two
spellings, before and after the 1918 reform.

So the rules are: Cyrillic is rendered through ALA-LC -- the 2012 table,
frozen here as the other folds freeze theirs, so that a new edition of
the display table never moves a key -- which takes the pre-reform letters
to their modern values on the way (``ѣ`` and ``е`` both reach *e*, ``і``
and ``и`` both *i*). Latin is lowercased; the scholarly letters become
their ALA-LC digraphs (``č`` *ch*, ``ŝ`` and ``šč`` *shch*) and ISO 9's
``â`` and ``û`` become *ia* and *iu*; diacritics, ties, the signs and the
apostrophes go. Then the German and French digraphs are collapsed
(*schtsch*, *tsch*, *tch*, *sch*, *ou*), ``x`` becomes *ks*, ``w`` *v*,
``j`` and ``y`` *i*, a ``c`` that does not start *ch* becomes *ts*, and an
``h`` that is not part of a digraph becomes *kh*. The glide before *e* is
dropped (*Yevgeniy*, *Vasilyev* to *evgenii*, *vasilev*), because ALA-LC
writes none; *yo* and *io* after a consonant become *e*, because ALA-LC's
``ё`` is *ë*; a closing *ff* becomes *v*. Doubled letters are collapsed
and anything that is not a letter or digit is removed.

Known gaps: the German and French spellings that use a letter for
another sound (German *ch* for ``х`` and *z* for ``ц``, French *ch* for
``ш`` and *j* for ``ж``), the English *Rachmaninoff*, and translated
names (*Peter* for ``Пётр``). The test set in
``tests/data/ru_fold_cases.tsv`` is the published claim.
"""

from __future__ import annotations

import re

from ..engine import render
from ..latin import FINISH, Rules, apply, clean
from ..script import Scheme
from .descriptor import SCRIPT

# The road Russian takes into Latin before the skeleton rules: the ALA-LC
# table as it stood in 2012, frozen here. The fold's keys are data other
# systems store, so they must not move when the display table follows a
# new edition of its standard; :mod:`.ala_lc` is free to change and this
# is not. It is never registered as a scheme.
_BASIS = Scheme(
    script=SCRIPT,
    key="fold_basis",
    name="Fold basis (ALA-LC 2012)",
    version="1.0",
    standard="ALA-LC Romanization Tables, Russian (2012), frozen for the fold",
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
        "ц": "t͡s",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": "ʺ",
        "ы": "y",
        "ь": "ʹ",
        "э": "ė",
        "ю": "i͡u",
        "я": "i͡a",
        "і": "ī",
        "ѣ": "i͡e",
        "ѳ": "ḟ",
        "ѵ": "ẏ",
    },
)

_LETTERS = {
    # BGN/PCGN's middle dot (t·s, y·a): gone before the digraphs are merged.
    "·": "",
    "ž": "zh",
    "š": "sh",
    "č": "ch",
    "ŝ": "shch",
    # ISO 9's ya and yu, which would otherwise lose their glide to NFKD.
    "â": "ia",
    "û": "iu",
}

_CONSONANT = "[bcdfgklmnprstvz]"

_LATIN: Rules = (
    # German and French spellings of the sibilants, longest first.
    (re.compile(r"schtsch|shtch"), "shch"),
    (re.compile(r"tsch"), "ch"),
    (re.compile(r"sch"), "sh"),
    (re.compile(r"tch"), "ch"),
    (re.compile(r"ou"), "u"),
    (re.compile(r"x"), "ks"),
    (re.compile(r"w"), "v"),
    (re.compile(r"[jy]"), "i"),
    (re.compile(r"tz"), "ts"),
    (re.compile(r"c(?!h)"), "ts"),
    # An h on its own is х: ISO 9's h, and the popular Mihail.
    (re.compile(r"(?<![zkcs])h"), "kh"),
    # The glide before e: ALA-LC writes none (Evgeniĭ, Vasilʹev, Andreev).
    (re.compile(r"i+e"), "e"),
    # ALA-LC's ë after a consonant: Fyodor, Pyotr, Semyon.
    (re.compile(rf"(?<={_CONSONANT})i+o"), "e"),
    (re.compile(r"ff$"), "v"),
    *FINISH,
)


def fold_token(token: str, context: str | None = None) -> str:
    """Fold one whitespace-free token, Cyrillic or Latin, to its key.

    *context* is accepted for the registry's sake and unused: no Russian
    rule depends on the rest of the text.
    """
    if SCRIPT.has_letters(token):
        token = render(token.lower(), _BASIS)
    return apply(clean(token, _LETTERS), _LATIN)


__all__ = ["fold_token"]
