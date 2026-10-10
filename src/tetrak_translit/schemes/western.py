"""Western Armenian pronunciation spelling: how diaspora names are written.

Not a standard: the practice. Western Armenian swapped the stops, so the
letter ``բ`` is pronounced *p* and ``պ`` is pronounced *b*, ``գ`` is *k*
and ``կ`` is *g*, ``դ`` is *t* and ``տ`` is *d*, and the affricates
likewise (``ձ`` *ts*, ``ծ`` *dz*, ``ջ`` *ch*, ``ճ`` *j*). A name spelled
by sound in Istanbul, Beirut, Aleppo, Paris or Los Angeles therefore
romanises the opposite way from the same name in a Yerevan catalogue:
*Hagop* and *Yakob* are both ``Յակոբ``; *Kevork* and *Gevorg* are both
``Գէորգ``/``Գևորգ``; *Boghosian* and *Poghosyan* are one surname.

The table renders the Western sound values without diacritics, the way
the names are actually written: word-initial ``յ`` is ``h``, ``ե`` and
``ո`` take ``ye`` and ``vo`` at the start of a word, ``ո`` after a vowel
is ``vo``, and the classical digraphs ``եա`` and ``իւ`` are ``ia`` and
``iu`` (*Vartanian*, *Harutiun*), which is where *-ian* comes from. ``ը`` is written ``e``; many real spellings omit it
altogether (*Mkrtich*), which no table can predict.

Lossy by nature: it was never meant to be reversed, and a scheme that
cannot say whether *p* is ``բ`` or ``փ`` is for display and finding
only. The fold treats the voiced and voiceless pairs as one, which is
what makes the two traditions' spellings match.
"""

from __future__ import annotations

from . import Scheme

WESTERN = Scheme(
    key="western",
    name="Western Armenian pronunciation",
    version="1.0",
    standard="Common practice, not a published standard",
    reversible=False,
    letters={
        "ա": "a",
        "բ": "p",
        "գ": "k",
        "դ": "t",
        "ե": "e",
        "զ": "z",
        "է": "e",
        "ը": "e",
        "թ": "t",
        "ժ": "zh",
        "ի": "i",
        "լ": "l",
        "խ": "kh",
        "ծ": "dz",
        "կ": "g",
        "հ": "h",
        "ձ": "ts",
        "ղ": "gh",
        "ճ": "j",
        "մ": "m",
        "յ": "y",
        "ն": "n",
        "շ": "sh",
        "ո": "o",
        "չ": "ch",
        "պ": "b",
        "ջ": "ch",
        "ռ": "r",
        "ս": "s",
        "վ": "v",
        "տ": "d",
        "ր": "r",
        "ց": "ts",
        "ւ": "v",
        "փ": "p",
        "ք": "k",
        "օ": "o",
        "ֆ": "f",
    },
    digraphs={"ու": "u", "և": "ev", "եա": "ia", "իւ": "iu"},
    initial={"ե": "ye", "ո": "vo", "և": "yev", "յ": "h"},
    after_vowel={"ո": "vo"},
    notes=(
        "The spelling diaspora names carry: Hagop, Kevork, Boghosian, Vartanian. "
        "Stops and affricates take their Western values; no diacritics. Not reversible."
    ),
)
