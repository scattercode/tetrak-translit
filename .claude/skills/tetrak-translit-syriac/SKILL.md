---
name: tetrak-translit-syriac
description: Syriac as tetrak-translit handles it — the 22-letter caseless right-to-left alphabet and the Unicode ranges the syr package claims, the West (Greek-letter) and East (dotted) vowel points and why nearly all real text has neither, the vocalisation detect() reports, ALA-LC 2012 letter by letter and point by point (é í ú carried by yod and waw, the final alaph rule that needed Rule(final=True)), what the table asks a cataloguer to do that no table can (supply vowels from Payne Smith), the consonantal fold and why šin is c in the key, Garshuni, the script styles nothing can detect, and the known gaps. Load this whenever Syriac text, a Syriac name or title, Garshuni, the syr/ package, syr_fold_cases.tsv, vowel points, or a romanisation such as Penqítā, Fenqīthō or Qurbono comes up — including "why is ܡܠܟܐ rendered mlkʾ", "why does Edessa not fold to ܐܘܪܗܝ", or "is this East or West Syriac".
---

# Syriac

The fourth script, and the first that is normally written **without vowels**.
That one fact shapes everything: the display table can only render what is
written, and the fold has to work on consonants. The tables in
`src/tetrak_translit/syr/` are the authority on individual letters.

## The script

- **22 letters**, `ܐ`–`ܬ`, U+0710–U+072C. **No case** (`cased=False`).
  Written right to left; Unicode stores logical order, so direction is the
  display's problem, not the engine's.
- **`Script.ranges`**: `(0x0710, 0x073F), (0x074D, 0x074F)` — letters, the
  superscript alaph, the vowel points U+0730–U+073F, and the Garshuni letters.
  Punctuation U+0700–U+070F is outside.
- **`archaic`** holds two kinds of non-alphabet unit a table may render: the
  other letters (`ܔ ܖ ܜ ܞ ܤ ܧ ܭ ܮ ܯ ݍ ݎ ݏ`: Garshuni, Persian, dotless
  dalath-rish, final semkath, reversed pe) and **the 16 vowel points**
  (`descriptor.POINTS`). The points are units the engine walks like letters,
  so `(point, yod)` and `(yod, point)` can be digraphs.
- **`marks`**: U+0740–U+074A (feminine dot, quššāyā, rukkākā and the other
  dots and lines), U+0308 (the seyāmē of the plural, a combining diaeresis)
  and U+0303 (the tilde of the modern letters). Marks must be **outside**
  the ranges: the Scheme validator refuses punctuation that is a letter.
- **Script styles** — Estrangela, Serto, Madnhaya — share one encoding and
  differ only in the font. Nothing in the text tells them apart; don't try.
- **Garshuni** (Arabic, Turkish, Malayalam and others in Syriac letters) is
  detected as Syriac, correctly. The ALA-LC table is not written for it.

## Vowel points and vocalisation

| Vowel | West (Greek letters) | East (dots) | ALA-LC |
|---|---|---|---|
| pthāḥā | U+0730 above, U+0731 below | U+0732 | a |
| zqāpā | U+0733, U+0734 | U+0735 | ā |
| rbāṣā / zlāmā | U+0736, U+0737 | U+0738 horizontal, U+0739 angular | e |
| ḥbāṣā | U+073A, U+073B | U+073C on yod | i |
| ʿṣāṣā | U+073D, U+073E | U+073C on waw | u |
| rwāḥā | — | U+073F on waw | o |

`variant()` is `syr.vocalisation.vocalisation`: `west`, `east`, `mixed` or
`unvocalised`. Measured on a large catalogue of Syriac manuscripts (October
2026): **fewer than 1 in 100** Syriac-script titles and incipits carry any
point. Assume unvocalised.

## ALA-LC 2012

Source: <https://www.loc.gov/catdir/cpso/romanization/syriac.pdf>, "2012
version, No earlier versions". ʾ is U+02BE and ʿ U+02BF.

- Consonants one letter each; bgdkpt hard and soft not distinguished;
  doubling not written. Rukkākā, quššāyā and seyāmē go through
  `punctuation` as `""`.
- **Vowel carried by yod or waw**: West writes the point on the letter
  *before* (`point + ܝ` → *í*/*é*, `point + ܘ` → *ú*); East writes it on the
  yod or waw itself (`ܝ + U+073C` → *í*, `ܘ + U+073C` → *ú*, `ܘ + U+073F` →
  *o*). All digraphs.
- **Final alaph** after ā or e is disregarded (*zadíqā*, not *zadíqāʾ*);
  inside a word it is kept (*ʾÍsrāʾyel*). Digraph `(point, ܐ)` → *āʾ*, with
  `Rule(..., final=True)` → *ā*. `final` was added to the engine for this, in
  its own PR first, as `CONTRIBUTING.md` requires.
- Initial yod with ḥbāṣā is *í* (*ídaʿ*); `(ḥbāṣā, ܝ)` before another vowel
  is *iy* (*ʾiyālā*), via `Rule(before=…)`.
- Every pointed example in the table renders exactly (`TestSyriacToLatin`).

**What no table can do**: for unvocalised text the standard tells the
cataloguer to *supply* the vowels from J. Payne Smith's *Syriac English
Dictionary*, with special East Syriac rules and Sokoloff for doubt. So the
library renders unvocalised text as its consonants, `ʾ w y` included:
`ܡܠܟܐ` → *mlkʾ*, not *malkā*. Also not attempted: silent letters, the hyphen
after a prefix (*da-qdām*), capitals, the Greek *-os* exception, and the
modern letters `ǧ č ž` (rendered as the letter under the tilde). Never
"improve" the table by guessing vowels.

## The fold (`syr/fold.py`)

The key is the **consonants**, because that is all every romanisation shares:
ALA-LC *Penqítā*, West *Fenqīthō*, popular *Fenqitho* and `ܦܢܩܝܬܐ` are all
*pnkt*.

1. Syriac is rendered through `_BASIS`, ALA-LC's consonants frozen, with the
   other letters on the consonants they write and the points as a vowel.
2. `clean()` with `š` → `\x01` and `ḥ` → `\x02`, so the next rule cannot take
   their *h*.
3. **Latin tokens only** (`_SPELLING`): `sh` → `\x01`; `ch` → *k* (Greek
   chi: *Antioch*); `th ph kh gh dh bh` → the letter (the West romanisation's
   soft consonants); `f` → *p*; `c` → *k*. Syriac tokens skip these and get
   only `_SKELETON`, because the basis renders one letter at a time and
   `ܕܗ` (*d* + *h*) is not a soft *d*. `probe.py trace` follows the same split.
4. `q` → *k*. Drop `a e i o u w y j v`: the vowels, and waw and yod in every spelling.
   *j* is yod in *Jacob* and *Joseph*; *v* is waw in *David*, *Nineveh*,
   *Evangelion* (measured: *v* almost never writes a soft *b* in these records).
5. `\x01` → **c** (not *sh*: `ܫ` must not meet `ܣܚ`; *c* is otherwise
   impossible in a key because step 3 removed it); `\x02` → *h*.
6. `FINISH`. Alaph and ʿē went with the half rings in `clean()`.

### Known gaps and over-merges

- Greek, Latin and translated names: *Edessa*, *Nisibis*, *Bar Hebraeus*,
  *Isaac* (no ḥ), *Gregory*. In the measured catalogue most author headings
  are of this kind; they are a name authority's job (tetrak-authority).
- Arabic romanisation's *j* for `ܓ` (*Jirjis*).
- **Over-merge** (declared): words differing only in alaph, ʿē, waw or yod
  share a key — `ܥܠ` (on) and `ܠܐ` (not) are both *l*.

## The test data

`tests/data/syr_fold_cases.tsv`: 21 groups — liturgical book titles
(*Penqítā*, *Šḥímā*, *Qúrbānā*, *Qúdāšā*, *Ḥúdrā*, *Bét gazā*,
*Ktābā da-qdām wad-bātar*), authors (*ʾAprém*, *ʾAprahaṭ*, *ʿAbdíšoʿ*,
*Gíwargís*, *Yaʿqúb*, *Yúḥanān*), places (*Ṭúr ʿAbdín*, *Naṣíbín*,
*ʾÚrhāy*), words (*ktābā*, *zadíqā*, *tešbúḥtā*, *Súryāyā*), each in the
script (some vocalised), ALA-LC (with U+02BB as records carry it, too), and
the West, East and popular spellings.

## Traps

- **ʿ in catalogue records** is often U+02BB (ʻ, the turned comma) rather than
  U+02BF. Both are in `engine.APOSTROPHES`; the fold strips both.
- **The PDF's text layer garbles some East points**; the code points above come
  from the Unicode names and the table's legible rows, checked against every
  example.
- **`Script.letters` must not hold the points**: every scheme must render every
  letter, and `test_renders_nothing_empty` forbids `""`. Points live in
  `archaic`.
