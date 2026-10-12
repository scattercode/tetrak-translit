"""The two kinds of data everything else runs over: a script and a scheme.

A :class:`Script` describes a writing system as this package needs it --
its alphabet, which sequences every scheme must render as a unit, its
vowels, where its letters live in Unicode and whether it has case. A
:class:`Scheme` is one romanisation table for one script. Both are data;
the engine in :mod:`tetrak_translit.engine` is the only code that reads
them, and it reads nothing else, which is what makes a new script a matter
of adding a package of tables rather than touching the engine.

Every table is written from the published standard it names, never copied
from another implementation. Romanisation tables are facts, but a copied
file is still a copied file (Tetrak brief 015).

Two kinds of scheme live here and the distinction matters:

- **Display schemes** render a script for a reader: a catalogue, a
  citation, a caption beside an OCR transcript.
- **Finding** is a different job, done by :func:`tetrak_translit.fold`,
  which maps every scheme of a script, and the script itself, onto a
  single index form. A scheme says how a name *looks*; the fold says which
  names are the *same*.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Script:
    """A writing system, as the engine needs to know it.

    Attributes:
        key: The short identifier used in scheme ids, on the command line
            and as the ``script=`` argument: ``"hy"``, ``"ka"``.
        name: The script's name as people write it: ``"Armenian"``.
        unicode_name: The first word of the script's letters' Unicode
            character names, lowercased, which is how :func:`detect`
            recognises it: ``"armenian"``, ``"georgian"``.
        letters: The lowercase alphabet, in order. Every scheme must
            render every one of these.
        archaic: Letters outside the modern alphabet that a scheme may
            also render (Georgian's ``ჱ ჲ ჳ ჴ ჵ``).
        digraphs: Sequences every scheme must render as a unit
            (Armenian's ``ու`` and ``և``).
        vowels: The lowercase vowels, for the schemes with after-vowel
            rules.
        ranges: Inclusive code point ranges of the script's letters, in
            every case form the engine should walk.
        cased: Whether the script has upper and lower case. Determines
            whether a capital in Latin input becomes a capital when read
            back; a caseless script is always written in its one form.
    """

    key: str
    name: str
    unicode_name: str
    letters: str
    archaic: str = ""
    digraphs: tuple[str, ...] = ()
    vowels: frozenset[str] = frozenset()
    ranges: tuple[tuple[int, int], ...] = ()
    cased: bool = True

    def is_letter(self, character: str) -> bool:
        """Whether *character* is one of this script's letters."""
        code = ord(character)
        return any(low <= code <= high for low, high in self.ranges)

    def has_letters(self, text: str) -> bool:
        return any(self.is_letter(character) for character in text)


@dataclass(frozen=True)
class Scheme:
    """One romanisation table for one script.

    Attributes:
        script: The :class:`Script` the table renders.
        key: The identifier within its script, e.g. ``"ala_lc"``. The
            fully qualified id is :attr:`id`, ``"hy/ala_lc"``.
        name: The scheme's name as people write it, e.g. ``"ALA-LC"``.
        version: This table's own version. Bumped whenever a mapping
            changes, so a user can say which table produced a string.
        standard: The published standard, by name and date, that the
            table was written from.
        reversible: Whether every Latin output maps back to exactly one
            letter. Only true where the standard marks every letter
            distinctly; the others are documented as lossy and
            :func:`tetrak_translit.transliterate` refuses to reverse them.
        letters: Lowercase letter to its Latin rendering. Must cover every
            letter in the script's alphabet; may cover its archaic letters.
        digraphs: The script's digraphs, and any others this scheme
            renders whole, to their renderings.
        initial: Renderings that apply only at the start of a word.
        after_vowel: Renderings that apply only directly after a vowel.
        separator: Written between two units whose renderings would
            otherwise read as a different unit, as ISO 9984:2026 writes
            ``z·h`` for ``ზ`` and ``ჰ`` so that it is not ``zh``, ``ჟ``.
            Skipped when reading back.
        separate: The pairs of units, in order, that take the separator.
        notes: What a user should know before choosing this scheme.
    """

    script: Script
    key: str
    name: str
    version: str
    standard: str
    reversible: bool
    letters: Mapping[str, str]
    digraphs: Mapping[str, str] = field(default_factory=dict)
    initial: Mapping[str, str] = field(default_factory=dict)
    after_vowel: Mapping[str, str] = field(default_factory=dict)
    separator: str = ""
    separate: frozenset[tuple[str, str]] = frozenset()
    notes: str = ""

    def __post_init__(self) -> None:
        alphabet = self.script.letters
        missing = [letter for letter in alphabet if letter not in self.letters]
        if missing:
            raise ValueError(f"{self.id} table is missing {''.join(missing)!r}")
        allowed = set(alphabet) | set(self.script.archaic)
        unknown = [letter for letter in self.letters if letter not in allowed]
        if unknown:
            raise ValueError(f"{self.id} table has keys outside the script {''.join(unknown)!r}")
        for digraph in self.script.digraphs:
            if digraph not in self.digraphs:
                raise ValueError(f"{self.id} table does not render {digraph!r}")
        for name, table in (("initial", self.initial), ("after_vowel", self.after_vowel)):
            stray = [
                unit for unit in table if unit not in self.letters and unit not in self.digraphs
            ]
            if stray:
                raise ValueError(f"{self.id} {name} rule names unknown units {stray!r}")
        if self.separate and not self.separator:
            raise ValueError(f"{self.id} names pairs to separate but no separator")
        stray = sorted(
            {
                unit
                for pair in self.separate
                for unit in pair
                if unit not in self.letters and unit not in self.digraphs
            }
        )
        if stray:
            raise ValueError(f"{self.id} separate names unknown units {stray!r}")

    @property
    def id(self) -> str:
        """The fully qualified id, ``"<script>/<key>"``."""
        return f"{self.script.key}/{self.key}"

    def render(self, unit: str, *, initial: bool = False, after_vowel: bool = False) -> str:
        """The Latin rendering of one lowercase letter or digraph.

        A unit the table does not define -- an archaic letter under a
        scheme that has no rendering for it -- is returned as it is.
        """
        if initial and unit in self.initial:
            return self.initial[unit]
        if after_vowel and unit in self.after_vowel:
            return self.after_vowel[unit]
        if unit in self.digraphs:
            return self.digraphs[unit]
        return self.letters.get(unit, unit)


__all__ = ["Scheme", "Script"]
