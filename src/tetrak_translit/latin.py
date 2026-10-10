"""Shared pieces of the Latin side of a fold.

Each script package owns its fold rules, because what should be merged
differs: Armenian folds ``b`` with ``p`` because Eastern and Western
spellings swap them, and Georgian must not, because ``ბ`` and ``პ`` are
different letters that never swap. What is common is the cleaning that
comes first -- lowercase, diacritics off, aspiration marks off, ASCII
only -- and the rule runner, so those live here.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence

from .engine import APOSTROPHES

_APOSTROPHES = re.compile(f"[{re.escape(APOSTROPHES)}]")

Rules = Sequence[tuple[re.Pattern[str], str]]


def clean(token: str, letters: Mapping[str, str]) -> str:
    """Lowercase *token*, map *letters*, strip diacritics and aspiration marks.

    *letters* maps the non-ASCII letters whose diacritic carries the whole
    distinction (``ž`` to ``zh``) and is applied before the diacritics are
    stripped, or ``ž`` would become ``z``.
    """
    lowered = unicodedata.normalize("NFC", token).lower()
    lowered = "".join(letters.get(character, character) for character in lowered)
    lowered = unicodedata.normalize("NFKD", lowered)
    lowered = "".join(character for character in lowered if not unicodedata.combining(character))
    return _APOSTROPHES.sub("", lowered)


def apply(token: str, rules: Rules) -> str:
    """Apply *rules* to *token* in order."""
    for pattern, replacement in rules:
        token = pattern.sub(replacement, token)
    return token


#: The closing rules every script's fold ends with: ASCII letters and
#: digits only, doubled letters collapsed.
FINISH: Rules = (
    (re.compile(r"[^a-z0-9]"), ""),
    (re.compile(r"(.)\1+"), r"\1"),
)

__all__ = ["FINISH", "Rules", "apply", "clean"]
