"""Armenian: the script, its six romanisation schemes, orthography and fold.

The package this library was built for. Armenian has two orthographies
in use -- classical (pre-1922, still used across the diaspora) and
reformed -- and two pronunciation traditions, Eastern and Western, that
romanise the same name opposite ways. :mod:`.orthography` tells the
orthographies apart; the schemes render for display; :func:`fold_token`
makes every spelling one key for finding; :data:`MARKS` are the signs
that a Latin value is romanised Armenian.
"""

from __future__ import annotations

from .ala_lc import ALA_LC
from .bgn_pcgn import BGN_PCGN
from .descriptor import SCRIPT
from .fold import fold_token
from .hubschmann_meillet import HUBSCHMANN_MEILLET
from .iso_9985 import ISO_9985
from .iso_9985_1996 import ISO_9985_1996
from .orthography import orthography as variant
from .romanised import MARKS
from .western import WESTERN

#: Every Armenian scheme, in the order the documentation lists them.
SCHEMES = {
    scheme.key: scheme
    for scheme in (ALA_LC, ISO_9985, ISO_9985_1996, BGN_PCGN, HUBSCHMANN_MEILLET, WESTERN)
}

__all__ = [
    "ALA_LC",
    "BGN_PCGN",
    "HUBSCHMANN_MEILLET",
    "ISO_9985",
    "ISO_9985_1996",
    "MARKS",
    "SCHEMES",
    "SCRIPT",
    "WESTERN",
    "fold_token",
    "variant",
]
