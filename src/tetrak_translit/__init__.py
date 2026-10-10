"""Detect, transliterate and fold Armenian text.

Three functions, one each for the three jobs:

- :func:`detect` says which script a string is in and, for Armenian,
  which orthography -- classical (pre-1922, still used in the diaspora)
  or reformed.
- :func:`transliterate` renders Armenian in a named romanisation scheme
  (ALA-LC, ISO 9985, BGN/PCGN, Hübschmann-Meillet, or the Western
  Armenian pronunciation spelling) and reads the reversible ones back.
  The schemes are for *display*.
- :func:`fold` maps any of the above -- Armenian in either orthography,
  Latin in any scheme -- onto one canonical index form, so that a search
  typed one way finds a record written another. The fold is for
  *finding*; its output is a key, not a spelling.

::

    >>> import tetrak_translit as tt
    >>> tt.detect("Երեւան").orthography
    'classical'
    >>> tt.transliterate("Երևան", "ala_lc")
    'Erevan'
    >>> tt.transliterate("Երևան", "bgn_pcgn")
    'Yerevan'
    >>> tt.fold("Yerevan") == tt.fold("Երեւան") == tt.fold("Erewan")
    True

No runtime dependencies. Built for the Armenian heritage aggregator
described in Tetrak's brief 015 and for `Tetrak <https://tetrak.dev/>`_'s
own OCR output, where an ALA-LC rendering beside a transcript is both a
catalogue-ready field and an accessibility one.
"""

from __future__ import annotations

from .detect import Detection, Markers, detect, orthography
from .fold import fold, fold_token
from .schemes import SCHEMES, Scheme
from .transliterate import (
    NotReversibleError,
    UnknownSchemeError,
    get_scheme,
    to_armenian,
    to_latin,
    transliterate,
)

try:
    # Written by hatch-vcs at build time; absent in a bare checkout.
    from ._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0+unknown"


def schemes() -> list[Scheme]:
    """The available romanisation schemes, in documentation order."""
    return list(SCHEMES.values())


__all__ = [
    "Detection",
    "Markers",
    "NotReversibleError",
    "SCHEMES",
    "Scheme",
    "UnknownSchemeError",
    "__version__",
    "detect",
    "fold",
    "fold_token",
    "get_scheme",
    "orthography",
    "schemes",
    "to_armenian",
    "to_latin",
    "transliterate",
]
