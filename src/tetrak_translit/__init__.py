"""Detect, transliterate and fold text in scripts that have several romanisations.

Three functions, one each for the three jobs:

- :func:`detect` says which script a string is in and, where the script
  has variants, which -- for Armenian, the classical (pre-1922, still used
  in the diaspora) or reformed orthography.
- :func:`transliterate` renders a script in a named romanisation scheme
  and reads the reversible ones back. The schemes are for *display*.
- :func:`fold` maps any of the above -- the script itself, Latin in any
  of its schemes -- onto one canonical index form, so that a search typed
  one way finds a record written another. The fold is for *finding*; its
  output is a key, not a spelling.

Two scripts so far, each a package of tables the engine runs over:
**Armenian** (:mod:`tetrak_translit.hy`: ALA-LC, ISO 9985 in its 2026
and 1996 editions, BGN/PCGN, Hübschmann-Meillet and the Western
pronunciation spelling) and
**Georgian** (:mod:`tetrak_translit.ka`: ALA-LC, ISO 9984 and the
national system).

::

    >>> import tetrak_translit as tt
    >>> tt.detect("Երեւան").orthography
    'classical'
    >>> tt.transliterate("Երևան", "ala_lc")
    'Erevan'
    >>> tt.transliterate("თბილისი", "national")
    'tbilisi'
    >>> tt.fold("Yerevan", script="hy") == tt.fold("Երեւան") == tt.fold("Erewan", script="hy")
    True
    >>> tt.fold("Chavchavadze", script="ka") == tt.fold("ჭავჭავაძე")
    True

No runtime dependencies. Built for a catalogue search and for
`Tetrak <https://tetrak.dev/>`_'s own OCR output, where a
romanisation beside a transcript is both a catalogue-ready field and
an accessibility one.
"""

from __future__ import annotations

from .detect import Detection, detect, orthography
from .engine import NotReversibleError
from .fold import ScriptRequiredError, fold, fold_token
from .registry import (
    PACKAGES,
    SCHEMES,
    UnknownSchemeError,
    UnknownScriptError,
    get_scheme,
    get_script,
)
from .script import Scheme, Script
from .transliterate import to_armenian, to_latin, to_script, transliterate

try:
    # Written by hatch-vcs at build time; absent in a bare checkout.
    from ._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0+unknown"


def schemes(script: str | Script | None = None) -> list[Scheme]:
    """The available romanisation schemes, for one script or for all."""
    if script is not None:
        return list(get_script(script).schemes.values())
    return list(SCHEMES.values())


def scripts() -> list[Script]:
    """The registered scripts, in documentation order."""
    return [package.script for package in PACKAGES.values()]


__all__ = [
    "Detection",
    "NotReversibleError",
    "SCHEMES",
    "Scheme",
    "Script",
    "ScriptRequiredError",
    "UnknownSchemeError",
    "UnknownScriptError",
    "__version__",
    "detect",
    "fold",
    "fold_token",
    "get_scheme",
    "get_script",
    "orthography",
    "schemes",
    "scripts",
    "to_armenian",
    "to_latin",
    "to_script",
    "transliterate",
]
