"""Georgian: the script, three romanisation schemes and the fold.

Modern Georgian is written in Mkhedruli, thirty-three letters with no
case, so a transliteration carries no capitals unless the source was set
in Mtavruli (the capital forms Unicode added in 2018, used for emphasis
and all-capitals headings). There is one orthography, so :func:`variant`
has nothing to say. The five archaic letters ``ჱ ჲ ჳ ჴ ჵ`` of older
texts are rendered by the schemes that define them and folded onto their
modern values.

Asomtavruli and Nuskhuri, the older scripts, are encoded separately and
are not handled.
"""

from __future__ import annotations

from .ala_lc import ALA_LC  # noqa: E402
from .descriptor import SCRIPT
from .fold import fold_token  # noqa: E402
from .iso_9984 import ISO_9984  # noqa: E402
from .national import NATIONAL  # noqa: E402

#: Every Georgian scheme, in the order the documentation lists them.
SCHEMES = {scheme.key: scheme for scheme in (ALA_LC, ISO_9984, NATIONAL)}


def variant(text: str) -> None:
    """Georgian has one orthography; there is no variant to detect."""
    return None


__all__ = ["ALA_LC", "ISO_9984", "NATIONAL", "SCHEMES", "SCRIPT", "fold_token", "variant"]
