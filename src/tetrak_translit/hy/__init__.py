"""Armenian: the script, its five romanisation schemes, orthography and fold.

The package this library was built for. Armenian has two orthographies
in use -- classical (pre-1922, still used across the diaspora) and
reformed -- and two pronunciation traditions, Eastern and Western, that
romanise the same name opposite ways. :mod:`.orthography` tells the
orthographies apart; the schemes render for display; :func:`fold_token`
makes every spelling one key for finding.
"""

from __future__ import annotations

from .ala_lc import ALA_LC  # noqa: E402
from .bgn_pcgn import BGN_PCGN  # noqa: E402
from .descriptor import SCRIPT
from .fold import fold_token  # noqa: E402
from .hubschmann_meillet import HUBSCHMANN_MEILLET  # noqa: E402
from .iso_9985 import ISO_9985  # noqa: E402
from .orthography import orthography as variant  # noqa: E402
from .western import WESTERN  # noqa: E402

#: Every Armenian scheme, in the order the documentation lists them.
SCHEMES = {
    scheme.key: scheme for scheme in (ALA_LC, ISO_9985, BGN_PCGN, HUBSCHMANN_MEILLET, WESTERN)
}

__all__ = [
    "ALA_LC",
    "BGN_PCGN",
    "HUBSCHMANN_MEILLET",
    "ISO_9985",
    "SCHEMES",
    "SCRIPT",
    "WESTERN",
    "fold_token",
    "variant",
]
