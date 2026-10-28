"""The Syriac script descriptor."""

from __future__ import annotations

from ..script import Script

#: The vowel points ALA-LC renders: the West Syriac signs from Greek
#: letters, above and below (U+0730, U+0731, U+0733, U+0734, U+0736,
#: U+0737, U+073A, U+073B, U+073D, U+073E), and the East Syriac dots
#: (U+0732, U+0735, U+0738, U+0739, U+073C, U+073F).
POINTS = "".join(chr(code) for code in range(0x0730, 0x0740))

#: Letters outside the classical alphabet: the dotless dalath-rish, the
#: letters for Garshuni and for Persian, and the final semkath and
#: reversed pe. No scheme here renders them; the fold maps them onto the
#: consonants they stand for.
OTHER_LETTERS = "ܔܖܜܞܤܧܭܮܯݍݎݏ"

SCRIPT = Script(
    key="syr",
    name="Syriac",
    unicode_name="syriac",
    letters="ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ",
    # The points are not letters, but they are rendered as units like
    # letters, so a scheme's table may define them.
    archaic=OTHER_LETTERS + POINTS,
    vowels=frozenset(POINTS),
    # Letters and the superscript alaph (U+0710 to U+072F), the vowel
    # points (U+0730 to U+073F) and the Garshuni letters (U+074D to
    # U+074F). Punctuation (U+0700 to U+070F) is outside; so are the
    # signs of U+0740 to U+074A, which are marks.
    ranges=((0x0710, 0x073F), (0x074D, 0x074F)),
    cased=False,
    # Signs written inside a word that no scheme here renders: the feminine
    # dot, quššāyā and rukkākā (hard and soft bgdkpt, which ALA-LC does
    # not distinguish), the other dots and lines of U+0743 to U+074A, the
    # seyāmē of the plural (a combining diaeresis), and the tilde of the
    # modern letters ǧ, č and ž.
    marks="".join(chr(code) for code in range(0x0740, 0x074B)) + "̈̃",
)

__all__ = ["OTHER_LETTERS", "POINTS", "SCRIPT"]
