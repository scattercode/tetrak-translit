# The canonical fold

`fold()` maps any spelling of an Armenian word — Armenian script in
either orthography, Latin in any romanisation — onto one canonical index
form, so that a search typed one way finds a record written another. It
is the function a Solr or Elasticsearch analysis chain calls, at index
time and at query time, and it is what the Armenian heritage aggregator
in Tetrak brief 015 actually depends on.

```python
>>> import tetrak_translit as tt
>>> {tt.fold(s) for s in ["Երևան", "Երեւան", "Erevan", "Erewan", "Yerevan"]}
{'erevan'}
>>> {tt.fold(s) for s in ["Գէորգ", "Գևորգ", "Gēorg", "Gevorg", "Kevork"]}
{'kevork'}
```

## Finding, not display

The key the fold returns is a deliberately coarse Latin skeleton. It
merges things a reader would want kept apart — `բ` and `պ`, `ե` and `է`,
`ց` and `ձ` — because Eastern and Western spellings disagree on exactly
those, and the point is that *Hagop* and *Yakob* land in the same place.
Never show a fold key to a reader. Index the folded field for search and
keep the original for display.

This is also why the fold does not claim there is a single right
spelling. Cross-script name-matching research (LREC 2020, cited in
Tetrak's research notes) finds there is often no gold form to score
against. The [schemes](schemes.md) are for display; the fold is for
finding; the two are kept apart on purpose.

## How it works

In order:

1. **Armenian input** is normalised across the 1922 reform, towards the
   reformed spelling: `եւ` becomes `և`; `է` becomes `ե`; the classical
   digraphs `եա` and `իւ` become `յա` and `յու`; `եո` becomes `եվո`
   (*Գէորգ* is *Gevorg*); and a word-final `յ` after a vowel is dropped
   (`ծառայ` is `ծառա`). It is then rendered through ALA-LC, so that
   Armenian and ALA-LC Latin reach the next step by the same road.
2. **Latin written in a reversible scheme**, when named with `scheme=`,
   is read back into Armenian exactly and treated as above.
3. **Latin** is lowercased and stripped of every diacritic and aspiration
   mark. Then its digraphs are collapsed onto one spelling each (`ž` and
   `zh`; `x` and `kh`; `ł`, `ġ` and `gh`; `ow`, `ou`, `oo` and `u`; `w`
   and `v`); the voiced and voiceless pairs are merged (`b`/`p`, `d`/`t`,
   `g`/`k`, `dz`/`ts`/`c`, `j`/`ch`); the glides are regularised
   (word-initial `ye` and `e`, `vo` and `o`, `y` and `h`; `ya`, `ea`
   and `ia`); a final `y` after a vowel is dropped; doubled letters are
   collapsed; and anything that is not a letter or a digit is removed.

Tokens are folded one at a time and joined with single spaces, so a
title folds to a sequence of keys that a whitespace tokeniser can index.

## The test set is the claim

`tests/data/fold_cases.tsv` in the repository lists groups of spellings
that fold together: the city, the surnames, the saints and the poets,
each in Armenian in both orthographies and in every scheme that renders
it, plus the popular spellings. The whole set must keep passing, and a
second test checks that different names stay different. It began with
the orthography findings of Tetrak brief 014 (`Ազգ եւ հայրենիք` against
`Ազգ և հայրենիք`, `Աւետիքեան` against `Ավետիքյան`) and grows with the
real variants a catalogue turns up. What is not in it is not claimed; the
right way to extend the fold is to add cases first.

## Known gaps

Things the fold does not do, written down so nobody assumes it does:

- **Popular spellings that insert an unwritten schwa.** `Մկրտիչ` is
  *Mkrtich* in every scheme but *Megerdich* on many a gravestone. No
  table can predict where a writer put the *e*.
- **Spellings that came through Russian.** *Khachaturian* has a *u* that
  `Խաչատրյան` does not; the fold gives `khachatrian`.
- **Classical `աւ` that reformed spelling turned into `օ`.** `աւր` and
  `օր` (day) do not fold together; the fold reads `ւ` as *v*.
- **`j` without a scheme hint.** In ALA-LC and BGN/PCGN `j` is `ջ`; in
  ISO 9985 and Hübschmann-Meillet it is `ձ`. The heuristic fold reads it
  the library way. Pass `scheme="iso_9985"` or
  `scheme="hubschmann_meillet"` when you know, and the input is reversed
  exactly instead.
- **BGN/PCGN `y` for `ը`.** It folds as the glide, not the schwa.

Each of these is a test in the suite, asserting that it does *not* pass.
If a change to the rules closes one, the test moves into the published
set.
