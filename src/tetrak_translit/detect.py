"""Say which script a string is in and, where the script has one, which variant.

Cheap and deterministic: Unicode character names give the script, so
any script is recognised, not only the ones this package transliterates.
For a registered script, the script package's ``variant`` function is
asked for more -- Armenian answers with its orthography, classical or
reformed; Georgian, with one orthography, has nothing to add.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

from .registry import scripts_in

MIXED = "mixed"
NONE = "none"


@dataclass(frozen=True)
class Detection:
    """What :func:`detect` found.

    Attributes:
        script: The script's Unicode name, lowercased -- ``"armenian"``,
            ``"georgian"``, ``"latin"``, ``"cyrillic"`` and so on -- or
            ``"mixed"`` (letters from more than one script) or ``"none"``
            (no letters at all).
        dominant: The script with the most letters, or ``None`` when
            there are none. Equal to *script* unless that is ``"mixed"``.
        key: The registry key of the one registered script present
            (``"hy"``, ``"ka"``), the value to pass as ``script=``; or
            ``None`` if none or several are present.
        orthography: What the script package's variant detector says,
            for a string with letters of exactly one registered script:
            Armenian's ``"classical"``, ``"reformed"`` or
            ``"indeterminate"``. ``None`` otherwise.
        letters: Letter counts per script, for every script seen.
    """

    script: str
    dominant: str | None
    key: str | None
    orthography: str | None
    letters: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        """A JSON-ready view, for the command line."""
        return {
            "script": self.script,
            "dominant": self.dominant,
            "key": self.key,
            "orthography": self.orthography,
            "letters": dict(self.letters),
        }


def _script_of(character: str) -> str | None:
    """The script a letter belongs to, from its Unicode name.

    Modifier letters (the aspiration marks ``ʻ`` and ``ʿ``) are letters to
    Unicode but belong to no script, and are left out.
    """
    if not character.isalpha() or unicodedata.category(character) == "Lm":
        return None
    try:
        return unicodedata.name(character).split(" ", 1)[0].lower()
    except ValueError:
        return None


def detect(text: str) -> Detection:
    """Detect the script of *text* and, for a registered script, its variant.

    Args:
        text: Any string. Digits, punctuation and whitespace are ignored;
            only letters count.

    Returns:
        A :class:`Detection`.
    """
    text = unicodedata.normalize("NFC", text)
    counts: dict[str, int] = {}
    for character in text:
        script = _script_of(character)
        if script is not None:
            counts[script] = counts.get(script, 0) + 1

    if not counts:
        return Detection(NONE, None, None, None, {})

    dominant = max(counts, key=lambda script: (counts[script], script))
    script = dominant if len(counts) == 1 else MIXED
    present = scripts_in(text)
    if len(present) == 1:
        package = present[0]
        return Detection(script, dominant, package.script.key, package.variant(text), counts)
    return Detection(script, dominant, None, None, counts)


def orthography(text: str) -> str | None:
    """The variant of the one registered script in *text*, or ``None``."""
    return detect(text).orthography


__all__ = ["Detection", "detect", "orthography"]
