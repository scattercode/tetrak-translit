"""The Syriac fold: one consonantal index form for every spelling of a word.

For what a fold is for, see :mod:`tetrak_translit.fold`. Syriac is the
first script here that is normally written without vowels, and the
romanisations disagree most about exactly what the script leaves out.
ALA-LC supplies the vowels of a dictionary (*Penqítā*, *Qúrbānā*); a
romanisation by West Syriac pronunciation writes *Fenqīthō* and
*Qūrbōnō*, with *o* for ALA-LC's *ā* and the soft consonants spelled
out; an East Syriac one, *Ḥūdrā*; a popular one, *Qurbono*. And the
script writes ``ܦܢܩܝܬܐ``, ``ܩܘܪܒܢܐ``. The one thing all of them share is
the consonants, so the key is the consonants.

So the rules are: Syriac is rendered through ALA-LC -- the 2012
consonant table, frozen here as the other folds freeze theirs -- with any
vowel points it carries. Both sides are lowercased, with diacritics and
the half rings ``ʾ`` and ``ʿ`` gone (so alaph and ʿē are dropped, as most
romanisations drop them), and ``š`` kept apart from *s* and *h* and
written *c* in the key, a letter nothing else leaves. Latin alone then
has its spellings reduced: *sh* to ``š``, the spelled-out soft
consonants of the West romanisations (*th*, *ph*, *kh*, *gh*, *dh*, *bh*)
and *ch* to their letters, ``f`` to *p* and ``c`` to *k* -- never the
Syriac side, whose ``ܕܗ`` is *d* and *h*, not a soft *d*. Then, on both
sides, ``q`` becomes *k* and every vowel is removed, and with them
``w``, ``y``, ``j`` and ``v``, which are waw and yod -- the letters
that also write long vowels, so that *ú* and ``ܘ`` meet. ``ḥ`` and ``h``
become one, ``ṭ`` and ``t``, ``ṣ`` and ``s``, ``q`` and ``k``. Doubled
letters are collapsed and anything that is not a letter or digit is
removed: *da-qdām* is ``ܕܩܕܡ``, one word, as the script writes it.

The key is deliberately coarse. Words that differ only in their matres
or in alaph and ʿē share it (``ܥܠ``, *on*, and ``ܠܐ``, *not*), which
costs little in a search over titles and names and is the price of
matching any romanisation at all.

Known gaps: Greek and Latin forms of names (*Edessa* for ``ܐܘܪܗܝ``,
*Nisibis* for ``ܢܨܝܒܝܢ``), translated names (*Bar Hebraeus*, *Isaac*
without the ``ḥ`` of ``ܐܝܣܚܩ``), and Arabic in Syriac letters, whose
romanisation writes *j* for ``ܓ``. The test set in
``tests/data/syr_fold_cases.tsv`` is the published claim.
"""

from __future__ import annotations

import re

from ..engine import render
from ..latin import FINISH, Rules, apply, clean
from ..script import Scheme
from .descriptor import POINTS, SCRIPT

# The road Syriac takes into Latin before the skeleton rules: the ALA-LC
# consonants as they stood in 2012, frozen here, and the letters outside
# the alphabet on the consonants they stand for. The points are rendered as
# a vowel the rules then drop. It is never registered as a scheme.
_BASIS = Scheme(
    script=SCRIPT,
    key="fold_basis",
    name="Fold basis (ALA-LC 2012)",
    version="1.0",
    standard="ALA-LC Romanization Tables, Syriac (2012), frozen for the fold",
    reversible=False,
    letters={
        "ܐ": "ʾ",
        "ܒ": "b",
        "ܓ": "g",
        "ܕ": "d",
        "ܗ": "h",
        "ܘ": "w",
        "ܙ": "z",
        "ܚ": "ḥ",
        "ܛ": "ṭ",
        "ܝ": "y",
        "ܟ": "k",
        "ܠ": "l",
        "ܡ": "m",
        "ܢ": "n",
        "ܣ": "s",
        "ܥ": "ʿ",
        "ܦ": "p",
        "ܨ": "ṣ",
        "ܩ": "q",
        "ܪ": "r",
        "ܫ": "š",
        "ܬ": "t",
        # Outside the alphabet: Garshuni, Persian and the variant forms.
        "ܔ": "g",
        "ܖ": "r",
        "ܜ": "ṭ",
        "ܞ": "yh",
        "ܤ": "s",
        "ܧ": "p",
        "ܭ": "b",
        "ܮ": "g",
        "ܯ": "d",
        "ݍ": "z",
        "ݎ": "k",
        "ݏ": "p",
        **dict.fromkeys(POINTS, "a"),
    },
)

_LETTERS = {
    # Kept apart until the end, so that the soft-consonant digraphs below
    # cannot take their h: Šḥímā is š and ḥ, not s and a soft h.
    "š": "\x01",
    "ḥ": "\x02",
}

# How romanisations spell a letter with two, or with a letter ALA-LC does
# not use. Only Latin input gets these: the Syriac side is rendered one
# letter at a time, so its ܕܗ (d and h) is not a soft d.
_SPELLING: Rules = (
    (re.compile(r"sh"), "\x01"),
    (re.compile(r"ch"), "k"),
    (re.compile(r"([tpkgdb])h"), r"\1"),
    (re.compile(r"f"), "p"),
    (re.compile(r"c"), "k"),
)

# What every token gets, Syriac or Latin.
_SKELETON: Rules = (
    (re.compile(r"q"), "k"),
    # Vowels, and waw and yod in every spelling: the matres go with them.
    (re.compile(r"[aeiouwyjv]"), ""),
    # Šin is c in the key, a letter no other rule leaves behind, so that
    # ܫ never meets ܣ and ܚ (s and h).
    (re.compile(r"\x01"), "c"),
    (re.compile(r"\x02"), "h"),
    *FINISH,
)

_LATIN: Rules = (*_SPELLING, *_SKELETON)


def fold_token(token: str, context: str | None = None) -> str:
    """Fold one whitespace-free token, Syriac or Latin, to its key.

    *context* is accepted for the registry's sake and unused: no Syriac
    rule depends on the rest of the text.
    """
    if SCRIPT.has_letters(token):
        return apply(clean(render(token, _BASIS), _LETTERS), _SKELETON)
    return apply(clean(token, _LETTERS), _LATIN)


__all__ = ["fold_token"]
