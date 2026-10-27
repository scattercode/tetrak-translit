"""Russian: the script, its romanisation schemes, orthography and fold.

Russian is written in Cyrillic, thirty-three letters with case. The
reform decreed in 1917 and enforced from 1918 removed four letters (``і``,
``ѣ``, ``ѳ``, ``ѵ``) and the hard sign at the end of a word, and émigré
presses kept the old spelling for decades after, so a collection holds
both. :mod:`.orthography` tells them apart; the ALA-LC table renders
both; :func:`fold_token` brings both, and every Latin spelling, to one
key.

The package handles the Russian alphabet. Other languages written in
Cyrillic are detected as this script, since they share its letters, but
the letters Russian lacks (Ukrainian ``є``, ``ї``, ``ґ``; Serbian ``ђ``,
``љ``) are not rendered, and the Church Slavonic letters and marks are
outside its claim.
"""

from __future__ import annotations

from ..script import RomanisationMark
from .ala_lc import ALA_LC
from .bgn_pcgn import BGN_PCGN
from .descriptor import SCRIPT
from .fold import fold_token
from .orthography import orthography as variant

#: Every Russian scheme, in the order the documentation lists them.
SCHEMES = {scheme.key: scheme for scheme in (ALA_LC, BGN_PCGN)}

#: No marks yet: the soft-sign prime and the tie that would be candidates
#: are shared with the ALA-LC tables for every other Cyrillic language,
#: and nothing has been measured on real records.
MARKS: tuple[RomanisationMark, ...] = ()

__all__ = [
    "ALA_LC",
    "BGN_PCGN",
    "MARKS",
    "SCHEMES",
    "SCRIPT",
    "fold_token",
    "variant",
]
