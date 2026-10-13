# The canonical fold

`fold()` maps any spelling of a word — its own script, Latin in any
romanisation — onto one canonical index form, so that a search typed one
way finds a record written another. It is the function a Solr or
Elasticsearch analysis chain calls, at index time and at query time.

```python
>>> import tetrak_translit as tt
>>> {tt.fold(s, script="hy") for s in ["Երևան", "Երեւան", "Erevan", "Erewan", "Yerevan"]}
{'erevan'}
>>> {tt.fold(s, script="ka") for s in ["თბილისი", "Tʻbilisi", "T'bilisi", "Tbilisi"]}
{'tbilisi'}
```

## Finding, not display

The key the fold returns is a deliberately coarse Latin skeleton. It
merges things a reader would want kept apart because the point is that
*Hagop* and *Yakob*, or *Chavchavadze* and *Ch'avch'avadze*, land in the
same place. Never show a fold key to a reader. Index the folded field for
search and keep the original for display.

This is also why the fold does not claim there is a single right
spelling. Cross-script name-matching research (LREC 2020, cited in
Tetrak's research notes) finds there is often no gold form to score
against. The [schemes](schemes.md) are for display; the fold is for
finding; the two are kept apart on purpose.

## Each script owns its rules

What should be merged differs between scripts, so each script package
carries its own fold and the top-level function only decides which rules
a token gets. A token in a registered script gets that script's rules. A
Latin token gets the rules of the script named by `script=`, and raises
if none is named: Armenian folds *b* with *p* because Eastern and
Western spellings swap them, Georgian must not because `ბ` and `პ` are
different letters that never swap, and *Batumi* folded under Armenian
rules would never find `ბათუმი`.

### Armenian

1. **Armenian input** is normalised across the 1922 reform, towards the
   reformed spelling: `եւ` becomes `և`; `է` becomes `ե`; the classical
   digraphs `եա` and `իւ` become `յա` and `յու`; `եո` becomes `եվո`
   (*Գէորգ* is *Gevorg*); and a word-final `յ` after a vowel is dropped
   (`ծառայ` is `ծառա`). It is then rendered through ALA-LC, so that
   Armenian and ALA-LC Latin reach the next step by the same road.
2. **Latin** is lowercased and stripped of every diacritic and aspiration
   mark. An aspirate written with an *h* loses it (`th` and `t`, `ph`
   and `p`, so *Thoumanian* finds `Թումանյան`), and an *h* after *v* is
   dropped (`vh` and `v`, so *Hovannes* finds *Hovhannes*). Then its
   digraphs are collapsed onto one spelling each (`ž` and
   `zh`; `x` and `kh`; `ł`, `ġ` and `gh`; `ow`, `ou`, `oo` and `u`; `iw`
   and `iu`, for the classical `իւ`; `w` and `v`); the voiced and voiceless pairs are merged (`b`/`p`, `d`/`t`,
   `g`/`k`, `dz`/`ts`/`c`, `j`/`ch`); the glides are regularised
   (word-initial `ye` and `e`, `vo` and `o`, `iu`, `y` and `h`, and `ho` and
   `o` for the Russian-mediated *Ovanes* and *Ovsep*; `ya`, `ea` and
   `ia`); a final `y` after a vowel is dropped; doubled letters are
   collapsed; and anything that is not a letter or a digit is removed.

### Georgian

1. **Georgian input** has its archaic letters folded onto their modern
   values (`ჱ ე`, `ჲ ი`, `ჳ ვ`, `ჴ ხ`, `ჵ ო`) and is rendered through
   ALA-LC.
2. **Latin** is lowercased and stripped of diacritics and apostrophes,
   which merges each aspirate with its ejective whichever system marked
   which; the sibilant spellings are collapsed (`ž`/`zh`, `š`/`sh`,
   `č`/`ch`, `ǰ`/`j`, `ḡ`/`gh`, `x`/`kh`); `dz` and `j` become one, `ts`
   and `c` become one; `q` becomes `k` (so *Kazbegi* finds `ყაზბეგი`);
   `y` becomes `i` and `w` becomes `v`; doubled letters are collapsed;
   and anything that is not a letter or a digit is removed.

Tokens are folded one at a time and joined with single spaces, so a
title folds to a sequence of keys that a whitespace tokeniser can index.

## The test sets are the claim

`tests/data/hy_fold_cases.tsv` and `tests/data/ka_fold_cases.tsv` in the
repository list groups of spellings that fold together: the cities, the
surnames, the saints and the poets, each in their script (and for
Armenian in both orthographies) and in every scheme that renders them,
plus the popular spellings. The whole set must keep passing, and a
second test checks that different names stay different. The Armenian set
began with the orthography findings of Tetrak brief 014 (`Ազգ եւ
հայրենիք` against `Ազգ և հայրենիք`, `Աւետիքեան` against `Ավետիքյան`);
both grow with the real variants a catalogue turns up. What is not in
them is not claimed; the right way to extend a fold is to add cases
first.

## Known gaps

Things the folds do not do, written down so nobody assumes they do.
Each is a test in the suite, asserting that it does *not* pass; if a
change to the rules closes one, the test moves into the published set.

Armenian:

- **Popular spellings that insert an unwritten schwa.** `Մկրտիչ` is
  *Mkrtich* in every scheme but *Megerdich* on many a gravestone.
- **Spellings that came through Russian.** *Khachaturian* has a *u* that
  `Խաչատրյան` does not. Russian has no *h*, and the fold restores it only
  before *o* (*Ovanes*, *Ovsep*), so *Akop* and *Arutyunyan* still miss
  *Hakob* and *Harutyunyan*. A general initial-*h* rule would also merge
  `իւր` (his) with `ուր` (where).
- **Classical `աւ` that reformed spelling turned into `օ`.** `աւր` and
  `օր` (day) do not fold together; the fold reads `ւ` as *v*.
- **`j` without a scheme hint.** In ALA-LC and BGN/PCGN `j` is `ջ`; in
  ISO 9985 and Hübschmann-Meillet it is `ձ`. The heuristic fold reads it
  the library way. Pass `scheme="iso_9985"` or
  `scheme="hubschmann_meillet"` when you know, and the input is reversed
  exactly instead.
- **BGN/PCGN `y` for `ը`.** It folds as the glide, not the schwa.
- **`իւր` (his) and `հուր` (fire) share a key.** Classical `իւ` becomes
  `յու`, and an initial `y` becomes `h` so that *Hagop* finds *Yakob*;
  the two words are then spelt the same. This is an over-merge, not a
  missed match: a search for one finds the other. Telling them apart
  would cost the `Յ`/`Հ` merge that every *Hakob* and *Hovhannes*
  depends on.

Georgian:

- **Russian-mediated forms.** *Tiflis* for `თბილისი`, *Kutais* for
  `ქუთაისი`.
- **Translated names.** *George* for `გიორგი`.
