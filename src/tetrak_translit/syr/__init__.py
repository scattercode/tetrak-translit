"""Syriac: the script, its romanisation, vocalisation and a consonantal fold.

Syriac is written right to left, has no case, and is normally written
without vowels; where vowels are written they are points, West Syriac or
East Syriac. Unicode stores the text in logical order, so direction is a
matter for whoever displays a romanisation beside it, not for this
package. :mod:`.vocalisation` says whether and how a text is pointed; the
ALA-LC table renders what is written; :func:`fold_token` reduces every
spelling to its consonants.

Arabic and other languages written in Syriac letters (Garshuni) are
detected as Syriac, because they are, but the ALA-LC Syriac table is not
written for them, and the fold takes the letters at their Syriac values.
"""

from __future__ import annotations

from ..script import RomanisationMark
from .ala_lc import ALA_LC
from .descriptor import SCRIPT
from .fold import fold_token
from .vocalisation import vocalisation as variant

#: Every Syriac scheme, in the order the documentation lists them.
SCHEMES = {scheme.key: scheme for scheme in (ALA_LC,)}

#: No marks yet: the half rings and the acute vowels of ALA-LC Syriac are
#: shared with the romanisations of Arabic and Hebrew, and nothing has been
#: measured on real records.
MARKS: tuple[RomanisationMark, ...] = ()

__all__ = [
    "ALA_LC",
    "MARKS",
    "SCHEMES",
    "SCRIPT",
    "fold_token",
    "variant",
]
