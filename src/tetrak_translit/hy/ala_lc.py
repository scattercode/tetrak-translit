"""ALA-LC: the Library of Congress romanisation, what library catalogues hold.

Written from the ALA-LC Romanization Tables, *Armenian*, 2022 version
(earlier versions 2011 and 1997), published by the Library of Congress.
Aspiration is marked with the modifier letter turned comma ``ʻ``
(U+02BB), which is the character the table uses and the one catalogue
records carry; a plain apostrophe is accepted on input by the fold.

``ե`` is ``e`` and ``ո`` is ``o`` in every position, which is why the
Library of Congress writes *Erevan* and *Oskan* where BGN/PCGN writes
*Yerevan* and *Voskan*. The ligature ``և`` is ``ev`` but the letter
``ւ`` is ``w``, so a classical-orthography imprint spelling the city
``Երեւան`` romanises as *Erewan* -- a real distinction in catalogue
records, not an error, and one the fold equates. ``ռ`` is ``ṛ``, with
the dot below.

The 2022 table's notes add rules this module follows:

- **The soft sign** ``ʹ`` (U+02B9, prime) goes between two letters that
  would otherwise read as a digraph (note 3): ``գհ`` ``gʹh``, ``դզ``
  ``dʹz``, ``կհ`` ``kʹh``, ``սհ`` ``sʹh``, ``տս`` ``tʹs``, as in
  *patʹsparan* and *SSʹH*.
- **A lowercase** ``եվ`` is ``eʹv`` (note 6): reformed spelling writes
  the sound *ev* as ``և``, so ``ե`` then ``վ`` in lowercase is a
  compound (*oskeʹvaz*). In capitals, ``ԵՎ`` and ``Եվ`` are the
  ligature's capitals and are *EV* and *Ev*.
- **In classical orthography**, a ``յ`` at the start of a word is ``ḥ``
  (note 4: *Ḥakob*), and an ``ե`` at the start of a name and before a
  vowel is ``y`` (note 2). A name is taken to be a capitalised word, and
  the start of a stem inside a compound is not detected. Both rules need
  the orthography: say it with ``orthography=``, or it is detected from
  the text, and an indeterminate text gets neither.

Punctuation follows the table's five rules: ``« »`` become “ ”; ``։`` is
a full stop; ``՛`` is dropped; and ``՞`` and ``՜``, set over a vowel
inside the sentence, become ``?`` and ``!`` at its end, in place of the
full stop. A sentence ends at ``։`` or at the end of the line. The table
says nothing of ``՝``, ``․`` or ``֊``, which pass through.

Lossy: the prime separates only the pairs the table lists, so ``zh`` is
still ``ժ`` or ``զ``+``հ``, and an initial ``y`` may be ``յ`` or, in a
classical name, ``ե``; the table cannot be reversed with certainty.
"""

from __future__ import annotations

from ..script import Rule, Scheme
from .descriptor import SCRIPT

ASPIRATION = "ʻ"  # U+02BB
PRIME = "ʹ"  # U+02B9, the soft sign of notes 3 and 6

ALA_LC = Scheme(
    script=SCRIPT,
    key="ala_lc",
    name="ALA-LC",
    version="2.0",
    standard="ALA-LC Romanization Tables, Armenian (2022 version)",
    reversible=False,
    letters={
        "ա": "a",
        "բ": "b",
        "գ": "g",
        "դ": "d",
        "ե": "e",
        "զ": "z",
        "է": "ē",
        "ը": "ě",
        "թ": "t" + ASPIRATION,
        "ժ": "zh",
        "ի": "i",
        "լ": "l",
        "խ": "kh",
        "ծ": "ts",
        "կ": "k",
        "հ": "h",
        "ձ": "dz",
        "ղ": "gh",
        "ճ": "ch",
        "մ": "m",
        "յ": "y",
        "ն": "n",
        "շ": "sh",
        "ո": "o",
        "չ": "ch" + ASPIRATION,
        "պ": "p",
        "ջ": "j",
        "ռ": "ṛ",
        "ս": "s",
        "վ": "v",
        "տ": "t",
        "ր": "r",
        "ց": "ts" + ASPIRATION,
        "ւ": "w",
        "փ": "p" + ASPIRATION,
        "ք": "k" + ASPIRATION,
        "օ": "ō",
        "ֆ": "f",
    },
    digraphs={"ու": "u", "և": "ev"},
    separator="ʹ",
    # Note 3.
    separate=frozenset({("գ", "հ"), ("դ", "զ"), ("կ", "հ"), ("ս", "հ"), ("տ", "ս")}),
    rules=(
        # Note 2: a classical name starting with ե and a vowel.
        Rule("ե", "y", initial=True, before="աեէըիոօ", capital=True, variant="classical"),
        # Note 6: lowercase ե then վ is a compound, not the ligature.
        Rule("ե", "e" + PRIME, before="վ", capital=False),
        # Note 4: a classical word-initial յ.
        Rule("յ", "ḥ", initial=True, variant="classical"),
    ),
    punctuation={"«": "“", "»": "”", "։": ".", "՛": ""},
    sentence_final={"՞": "?", "՜": "!"},
    sentence_end="։",
    notes=(
        "The form in library catalogues (Koha, WorldCat, the Library of Congress). "
        "Aspiration marked with ʻ (U+02BB); a prime ʹ separates letters that would "
        "read as a digraph. Lossy."
    ),
)
