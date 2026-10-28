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

A third, smaller kind of data, :class:`RomanisationMark`, runs the other
way: a sign in Latin text that it is a romanisation of a script, which
:func:`tetrak_translit.detect` reports as evidence.
"""

from __future__ import annotations

import re
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
        marks: Characters that are not letters but are written inside a
            word, so a word does not end at them: Armenian's stress marks
            ``՛ ՜ ՞``, set over the stressed vowel, and its apostrophe and
            abbreviation mark. A scheme may render them through its
            ``punctuation``; otherwise they pass through where they stand.
        compatibility: Characters that stand for a sequence of the script's
            letters and are written out as those letters before anything
            else happens: Armenian's presentation ligatures (``ﬕ`` is
            ``մի``). Unicode keeps them only for compatibility; they are
            typesetting, not spelling, and no standard has a rendering for
            them. Only these are expanded, not NFKC as a whole, which would
            also rewrite Latin and the modifier letters some schemes output.
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
    marks: str = ""
    compatibility: Mapping[str, str] = field(default_factory=dict)

    def expand(self, text: str) -> str:
        """*text* with each compatibility character written out as its letters."""
        if not any(character in self.compatibility for character in text):
            return text
        return "".join(self.compatibility.get(character, character) for character in text)

    def is_letter(self, character: str) -> bool:
        """Whether *character* is one of this script's letters."""
        code = ord(character)
        return any(low <= code <= high for low, high in self.ranges)

    def has_letters(self, text: str) -> bool:
        return any(
            self.is_letter(character) or character in self.compatibility for character in text
        )


@dataclass(frozen=True)
class Rule:
    """A rendering that replaces a unit's usual one when its conditions hold.

    Every condition given must hold; the first rule that matches wins.

    Attributes:
        unit: The lowercase letter or digraph the rule renders.
        latin: Its rendering when the rule applies.
        initial: Only at the start of a word.
        final: Only at the end of a word. Marks set after the unit (a stress
            mark, a sign the scheme drops) do not stop it being final.
        before: Only when the next letter in the word starts with one of
            these characters (``""`` for any, including none).
        capital: ``True`` only when the unit is a capital, ``False`` only
            when it is lowercase, ``None`` for either.
        variant: Only in text of this variant of the script (Armenian's
            ``"classical"`` orthography), as the caller states it or the
            script's detector finds it.
    """

    unit: str
    latin: str
    initial: bool = False
    final: bool = False
    before: str = ""
    capital: bool | None = None
    variant: str | None = None

    def applies(
        self,
        *,
        initial: bool,
        following: str | None,
        capital: bool,
        variant: str | None,
        final: bool = False,
    ) -> bool:
        """Whether the rule holds for a unit in this position."""
        if self.initial and not initial:
            return False
        if self.final and not final:
            return False
        if self.before and not (following and following[0] in self.before):
            return False
        if self.capital is not None and self.capital != capital:
            return False
        return self.variant is None or self.variant == variant


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
        rules: Conditional renderings, tried before the table (see
            :class:`Rule`).
        punctuation: Marks the standard renders where they stand, to their
            Latin form; ``""`` drops a mark. A mark not listed passes
            through unchanged.
        sentence_final: Marks the standard moves to the end of the
            sentence, to their Latin form (ALA-LC writes ``՞`` as a
            question mark there, not over the vowel that carries it).
        sentence_end: Characters that end a sentence. A moved mark is
            written in place of the first one after it, or at the end of
            the line.
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
    rules: tuple[Rule, ...] = ()
    punctuation: Mapping[str, str] = field(default_factory=dict)
    sentence_final: Mapping[str, str] = field(default_factory=dict)
    sentence_end: str = ""
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
        stray = sorted({rule.unit for rule in self.rules} - set(self.letters) - set(self.digraphs))
        if stray:
            raise ValueError(f"{self.id} rules name unknown units {stray!r}")
        marks = set(self.punctuation) | set(self.sentence_final) | set(self.sentence_end)
        letters = [mark for mark in marks if self.script.is_letter(mark)]
        if letters:
            raise ValueError(f"{self.id} treats letters as punctuation {letters!r}")

    @property
    def id(self) -> str:
        """The fully qualified id, ``"<script>/<key>"``."""
        return f"{self.script.key}/{self.key}"

    def render(
        self,
        unit: str,
        *,
        initial: bool = False,
        final: bool = False,
        after_vowel: bool = False,
        following: str | None = None,
        capital: bool = False,
        variant: str | None = None,
    ) -> str:
        """The Latin rendering of one lowercase letter or digraph.

        A unit the table does not define -- an archaic letter under a
        scheme that has no rendering for it -- is returned as it is. Marks
        are the engine's business: it renders them through ``punctuation``
        where they stand and never asks here.
        """
        for rule in self.rules:
            if rule.unit == unit and rule.applies(
                initial=initial,
                final=final,
                following=following,
                capital=capital,
                variant=variant,
            ):
                return rule.latin
        if initial and unit in self.initial:
            return self.initial[unit]
        if after_vowel and unit in self.after_vowel:
            return self.after_vowel[unit]
        if unit in self.digraphs:
            return self.digraphs[unit]
        return self.letters.get(unit, unit)


@dataclass(frozen=True)
class RomanisationMark:
    """A sign that a Latin-script value is a romanisation of a script.

    Marks are evidence, not a classification. A romanisation without marks
    (*Erker*) shows none, and a mark names a family of schemes rather than
    one: ALA-LC, ISO 9985 and BGN/PCGN all write an aspirate with an
    apostrophe.

    Attributes:
        key: A stable name for the mark, for code to compare against.
        description: What the mark is, for a reader.
        pattern: Where it occurs in a value, matched against NFC text.
        distinctive: Whether no other language's ordinary spelling uses the
            mark, so that it alone is good evidence. False for marks that
            other languages share: Czech has *č* and *ž*, Polish *ł*,
            German *tsch*.
    """

    key: str
    description: str
    pattern: re.Pattern[str]
    distinctive: bool


__all__ = ["RomanisationMark", "Rule", "Scheme", "Script"]
