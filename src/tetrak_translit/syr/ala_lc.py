"""ALA-LC: the Library of Congress romanisation of Syriac.

Written from the ALA-LC Romanization Tables, *Syriac* (2012 version, the
first). The consonants are one letter each, with ``ʾ`` (U+02BE) for alaph
and ``ʿ`` (U+02BF) for ʿē; the hard and soft bgdkpt are not
distinguished, and doubling is not shown. Vowel points are rendered when
the text carries them, West and East alike: ``a ā e i o u``, and ``é``,
``í`` and ``ú`` when the vowel is carried by yod or waw. An alaph at the
end of a word that carries ``ā`` or ``e`` is disregarded.

What this table cannot do is what the standard asks of a cataloguer when
the text has no vowels, which is almost always: supply them from Payne
Smith's dictionary, and for East Syriac texts adjust them by the special
rules. A rendering of unvocalised text is therefore the consonants as
written, ``ʾ``, ``w`` and ``y`` included: ``ܡܠܟܐ`` is *mlkʾ*, not *malkā*.
That is a faithful transliteration of what is on the page, not a
catalogue heading. Nor does it attempt the table's judgements about
silent letters, hyphens after prefixes, or capitals: Syriac has no case,
and the output is lowercase.
"""

from __future__ import annotations

from ..script import Rule, Scheme
from .descriptor import SCRIPT

ALAPH = "ʾ"
E = "ʿ"

# The vowel points, by vowel. West Syriac first, then East.
_A = "ܱܰܲ"
_LONG_A = "ܴܳܵ"
_E = "ܷܸܹܶ"
_I_WEST = "ܻܺ"
_U_WEST = "ܾܽ"
_I_OR_U_EAST = "ܼ"  # East: under yod, i; under waw, u
_O_EAST = "ܿ"

_YOD = "ܝ"
_WAW = "ܘ"
_ALAPH = "ܐ"

ALA_LC = Scheme(
    script=SCRIPT,
    key="ala_lc",
    name="ALA-LC",
    version="1.0",
    standard="ALA-LC Romanization Tables, Syriac (2012)",
    reversible=False,
    letters={
        "ܐ": ALAPH,
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
        "ܥ": E,
        "ܦ": "p",
        "ܨ": "ṣ",
        "ܩ": "q",
        "ܪ": "r",
        "ܫ": "š",
        "ܬ": "t",
        **dict.fromkeys(_A, "a"),
        **dict.fromkeys(_LONG_A, "ā"),
        **dict.fromkeys(_E, "e"),
        **dict.fromkeys(_I_WEST + _I_OR_U_EAST, "i"),
        **dict.fromkeys(_U_WEST, "u"),
        _O_EAST: "o",
    },
    digraphs={
        # The vowel carried by yod or waw: West writes the point on the
        # letter before, East on the yod or waw itself.
        **{point + _YOD: "é" for point in _E},
        **{point + _YOD: "í" for point in _I_WEST},
        **{point + _WAW: "ú" for point in _U_WEST},
        _YOD + _I_OR_U_EAST: "í",
        _WAW + _I_OR_U_EAST: "ú",
        _WAW + _O_EAST: "o",
        # A yod that carries i itself; at the start of a word it is í
        # (ídaʿ), below.
        **{_YOD + point: "yi" for point in _I_WEST},
        # An alaph after ā or e, which is disregarded at the end of a word.
        **{point + _ALAPH: "ā" + ALAPH for point in _LONG_A},
        **{point + _ALAPH: "e" + ALAPH for point in _E},
    },
    rules=(
        *(Rule(point + _ALAPH, "ā", final=True) for point in _LONG_A),
        *(Rule(point + _ALAPH, "e", final=True) for point in _E),
        *(Rule(_YOD + point, "í", initial=True) for point in _I_WEST),
        # A yod that carries i for the letter before and a vowel of its
        # own is a consonant: ʾiyālā.
        *(Rule(point + _YOD, "iy", before="".join(SCRIPT.vowels)) for point in _I_WEST),
    ),
    punctuation=dict.fromkeys(SCRIPT.marks, ""),
    notes=(
        "The form in library catalogues, but only where the text is vocalised: a "
        "cataloguer supplies the vowels of unvocalised text from a dictionary, and a "
        "table cannot. Unvocalised text renders as its consonants, ʾ w y included: ܡܠܟܐ "
        "is mlkʾ. Lossy: hard and soft bgdkpt are one letter, and points are dropped."
    ),
)
