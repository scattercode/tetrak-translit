"""Tell pre-reform Russian spelling from reformed, from the text alone.

The reform decreed in 1917 and enforced from 1918 removed four letters --
``і``, ``ѣ``, ``ѳ`` and ``ѵ`` -- and the hard sign ``ъ`` that ended every
word ending in a hard consonant. Soviet presses followed it at once; many
émigré presses kept the old spelling for decades, so a pre-reform text is
not necessarily a pre-revolutionary one. As with Armenian, the verdict is
made on presence, not on rate, because a catalogue title may hold one
diagnostic letter and no more.

Any of the four letters, or a ``ъ`` closing a word, makes a string
pre-reform. Failing that, a word that ends in a hard consonant with no
``ъ`` after it (``Пушкин``, where the old spelling wrote ``Пушкинъ``)
makes it reformed. Abbreviations ended in a bare consonant under both
spellings (``г.`` for *год*, ``стр.``), so a word followed by a full stop
does not count, nor does one of fewer than three letters or one written
in capitals (``СССР``). A string with no tell either way -- ``Москва`` --
is *indeterminate*.
"""

from __future__ import annotations

import re

PRE_REFORM = "pre-reform"
REFORMED = "reformed"
INDETERMINATE = "indeterminate"

_LETTER = r"[Ѐ-ҁҊ-ԯ]"
_REMOVED_LETTERS = re.compile(r"[іІѣѢѳѲѵѴ]")
_FINAL_HARD_SIGN = re.compile(rf"(?<={_LETTER})[ъЪ](?!{_LETTER})")
#: A word of three or more letters ending in a lowercase hard consonant,
#: not followed by a full stop.
_BARE_FINAL_CONSONANT = re.compile(
    rf"(?<!{_LETTER}){_LETTER}{{2,}}[бвгджзклмнпрстфхцчшщ](?!{_LETTER}|\.)"
)


def orthography(text: str) -> str | None:
    """The orthography of the Russian in *text*, or ``None`` if there is none."""
    if not re.search(_LETTER, text):
        return None
    if _REMOVED_LETTERS.search(text) or _FINAL_HARD_SIGN.search(text):
        return PRE_REFORM
    if _BARE_FINAL_CONSONANT.search(text):
        return REFORMED
    return INDETERMINATE


__all__ = ["INDETERMINATE", "PRE_REFORM", "REFORMED", "orthography"]
