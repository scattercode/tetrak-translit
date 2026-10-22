"""Say which script a string is in and, where the script has one, which variant.

Cheap and deterministic: Unicode character names give the script, so
any script is recognised, not only the ones this package transliterates.
For a registered script, the script package's ``variant`` function is
asked for more -- Armenian answers with its orthography, classical or
reformed; Georgian, with one orthography, has nothing to add.

Latin letters are a script too, but a romanisation is written in them,
so for any text with Latin letters each registered script is asked
whether the text carries its romanisation marks: the evidence a
catalogue search across scripts needs when a title's language code says
nothing. The marks are reported as found, never turned into a verdict.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

from .registry import PACKAGES, scripts_in

MIXED = "mixed"
NONE = "none"


@dataclass(frozen=True)
class Romanisation:
    """The marks of one script's romanisation found in a Latin value.

    Attributes:
        key: The registry key of the script romanised (``"hy"``).
        marks: The :attr:`~tetrak_translit.script.RomanisationMark.key` of
            every mark found, most distinctive first.
        distinctive: Whether any of them is a mark no other language's
            ordinary spelling uses. False means the evidence is real but
            shared: *č* is Czech as well.
    """

    key: str
    marks: tuple[str, ...]
    distinctive: bool

    def as_dict(self) -> dict[str, object]:
        """A JSON-ready view, for the command line."""
        return {"key": self.key, "marks": list(self.marks), "distinctive": self.distinctive}


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
        romanisations: For text with Latin letters, one
            :class:`Romanisation` per registered script whose marks occur
            in it, in registry order; empty otherwise. Evidence for search
            and display, not a classification: a romanisation without
            marks (*Erker*) shows nothing, and the result should never be
            used to exclude a record.
    """

    script: str
    dominant: str | None
    key: str | None
    orthography: str | None
    letters: dict[str, int] = field(default_factory=dict)
    romanisations: tuple[Romanisation, ...] = ()

    def as_dict(self) -> dict[str, object]:
        """A JSON-ready view, for the command line."""
        return {
            "script": self.script,
            "dominant": self.dominant,
            "key": self.key,
            "orthography": self.orthography,
            "letters": dict(self.letters),
            "romanisations": [found.as_dict() for found in self.romanisations],
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


def romanisations(text: str) -> tuple[Romanisation, ...]:
    """The romanisation marks of every registered script found in *text*.

    Reads the whole text, whatever its letters; :func:`detect` calls it
    only when there are Latin letters to read.
    """
    text = unicodedata.normalize("NFC", text)
    found = []
    for package in PACKAGES.values():
        present = [mark for mark in package.marks if mark.pattern.search(text)]
        if present:
            found.append(
                Romanisation(
                    package.script.key,
                    tuple(mark.key for mark in present),
                    any(mark.distinctive for mark in present),
                )
            )
    return tuple(found)


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
    marks = romanisations(text) if "latin" in counts else ()
    present = scripts_in(text)
    if len(present) == 1:
        package = present[0]
        return Detection(script, dominant, package.script.key, package.variant(text), counts, marks)
    return Detection(script, dominant, None, None, counts, marks)


def orthography(text: str) -> str | None:
    """The variant of the one registered script in *text*, or ``None``."""
    return detect(text).orthography


__all__ = ["Detection", "Romanisation", "detect", "orthography", "romanisations"]
