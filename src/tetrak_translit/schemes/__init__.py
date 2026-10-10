"""The romanisation schemes, each a versioned table written from its standard.

A :class:`Scheme` is data, not code: the letter table, the two digraphs
Armenian has (``ու`` and the ligature ``և``), any word-initial overrides,
and the facts a user needs to choose one -- which standard it follows,
whether it can be reversed, and what it is for.

Every table here was written from the published standard it names, never
copied from another implementation. Romanisation tables are facts, but a
copied file is still a copied file (Tetrak brief 015).

Two kinds of scheme live here and the distinction matters:

- **Display schemes** render Armenian for a reader: a catalogue, a
  citation, a caption beside an OCR transcript. ALA-LC, ISO 9985,
  BGN/PCGN and Hübschmann-Meillet are published standards; ``western``
  is the pronunciation spelling diaspora names actually carry.
- **Finding** is a different job, done by :func:`tetrak_translit.fold`,
  which maps every one of these onto a single index form. A scheme says
  how a name *looks*; the fold says which names are the *same*.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

#: The thirty-eight lowercase letters of the Armenian alphabet, ա through ֆ.
#: ``ւ`` (U+0582) is a letter in classical orthography and half of ``ու`` in
#: reformed; ``և`` (U+0587) is the ligature of ``ե`` and ``ւ``.
ARMENIAN_LOWERCASE = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ"

#: The two sequences every scheme treats as a unit.
DIGRAPHS = ("ու", "և")


@dataclass(frozen=True)
class Scheme:
    """One romanisation table.

    Attributes:
        key: The identifier used on the command line and in
            :func:`tetrak_translit.transliterate`, e.g. ``"ala_lc"``.
        name: The scheme's name as people write it, e.g. ``"ALA-LC"``.
        version: This table's own version. Bumped whenever a mapping
            changes, so a user can say which table produced a string.
        standard: The published standard, by name and date, that the
            table was written from.
        reversible: Whether every Latin output maps back to exactly one
            Armenian input. Only true where the standard marks every
            letter distinctly; the others are documented as lossy and
            :func:`tetrak_translit.transliterate` refuses to reverse them.
        letters: Lowercase Armenian letter to its Latin rendering. Must
            cover every letter in :data:`ARMENIAN_LOWERCASE`.
        digraphs: ``ու`` and ``և`` to their renderings.
        initial: Renderings that apply only at the start of a word, for
            the schemes that have them (BGN/PCGN's ``ye`` and ``vo``).
        after_vowel: Renderings that apply only directly after a vowel.
        notes: What a user should know before choosing this scheme.
    """

    key: str
    name: str
    version: str
    standard: str
    reversible: bool
    letters: Mapping[str, str]
    digraphs: Mapping[str, str]
    initial: Mapping[str, str] = field(default_factory=dict)
    after_vowel: Mapping[str, str] = field(default_factory=dict)
    notes: str = ""

    def __post_init__(self) -> None:
        missing = [letter for letter in ARMENIAN_LOWERCASE if letter not in self.letters]
        if missing:
            raise ValueError(f"{self.name} table is missing {''.join(missing)!r}")
        unknown = [letter for letter in self.letters if letter not in ARMENIAN_LOWERCASE]
        if unknown:
            raise ValueError(f"{self.name} table has non-Armenian keys {''.join(unknown)!r}")
        for digraph in DIGRAPHS:
            if digraph not in self.digraphs:
                raise ValueError(f"{self.name} table does not render {digraph!r}")

    def render(self, unit: str, *, initial: bool = False, after_vowel: bool = False) -> str:
        """The Latin rendering of one lowercase letter or digraph."""
        if initial and unit in self.initial:
            return self.initial[unit]
        if after_vowel and unit in self.after_vowel:
            return self.after_vowel[unit]
        if unit in self.digraphs:
            return self.digraphs[unit]
        return self.letters[unit]


from .ala_lc import ALA_LC  # noqa: E402
from .bgn_pcgn import BGN_PCGN  # noqa: E402
from .hubschmann_meillet import HUBSCHMANN_MEILLET  # noqa: E402
from .iso_9985 import ISO_9985  # noqa: E402
from .western import WESTERN  # noqa: E402

#: Every scheme, in the order the documentation lists them.
SCHEMES: Mapping[str, Scheme] = {
    scheme.key: scheme for scheme in (ALA_LC, ISO_9985, BGN_PCGN, HUBSCHMANN_MEILLET, WESTERN)
}

__all__ = [
    "ALA_LC",
    "ARMENIAN_LOWERCASE",
    "BGN_PCGN",
    "DIGRAPHS",
    "HUBSCHMANN_MEILLET",
    "ISO_9985",
    "SCHEMES",
    "Scheme",
    "WESTERN",
]
