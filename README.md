# tetrak-translit

Detect, transliterate and fold text in scripts that have several
romanisations: Armenian and Georgian so far. A dependency-free Python
library and command-line tool for the problem every catalogue of such
material has: the same name exists in its own script, sometimes in more
than one orthography, and in three or five Latin spellings, and no stock
search engine treats them as one word.

> **Status: alpha.** The tables and the folds are tested against the sets
> in [`tests/data/`](tests/data/); what is not in them is not claimed.
> See [known gaps](#what-it-does-not-do). The API may still change before
> 1.0.

```bash
pip install tetrak-translit
```

```python
>>> import tetrak_translit as tt
>>> tt.detect("Երեւան").orthography
'classical'
>>> tt.transliterate("Երևան", "ala_lc")
'Erevan'
>>> tt.transliterate("Երևան", "bgn_pcgn")
'Yerevan'
>>> tt.transliterate("Յակոբ", "western")
'Hagop'
>>> tt.transliterate("თბილისი", "national")
'tbilisi'
>>> tt.fold("Yerevan", script="hy") == tt.fold("Երեւան") == tt.fold("Erewan", script="hy")
True
>>> tt.fold("Boghossian", script="hy") == tt.fold("Պօղոսեան") == tt.fold("Poghosyan", script="hy")
True
>>> tt.fold("Chavchavadze", script="ka") == tt.fold("ჭავჭავაძე") == tt.fold("Ch'avch'avadze", script="ka")
True
```

```bash
$ tetrak-translit detect "Ազգ եւ հայրենիք" "თბილისი"
armenian (classical)	Ազգ եւ հայրենիք
georgian	თბილისი
$ tetrak-translit transliterate --scheme iso_9985 "Չարենց"
Čarenc'
$ tetrak-translit transliterate --scheme iso_9984 --to script "T'bilisi"
თბილისი
$ cut -f2 titles.tsv | tetrak-translit fold --script hy
```

## Three jobs

**Detection.** Which script a string is in and, for Armenian, which
orthography: *classical* (everything printed before the 1922 reform, and
the diaspora still), *reformed* (Soviet and post-Soviet Armenia) or
*indeterminate* (the string reads the same under both). Unicode character
names plus a few orthographic tells, chiefly a free `ւ` outside the `ու`
digraph.

**Transliteration**, between a script and its named Latin schemes, each a
versioned, tested table written from its published standard:

| Id | Scheme | Where you meet it | Reversible |
|---|---|---|---|
| `hy/ala_lc` | ALA-LC Armenian (2011) | Library catalogues: Koha, WorldCat, the Library of Congress | no |
| `hy/iso_9985` | ISO 9985:2026 | Data exchange; one letter per letter | **yes** |
| `hy/iso_9985_1996` | ISO 9985:1996, superseded | Reading data romanised under the first edition | **yes** |
| `hy/bgn_pcgn` | BGN/PCGN 1981 | Maps and place names: *Yerevan*, *Gyumri* | no |
| `hy/hubschmann_meillet` | Hübschmann-Meillet | Linguistics and classical scholarship | **yes** |
| `hy/western` | Western Armenian pronunciation | Diaspora names: *Hagop*, *Kevork*, *Boghosian* | no |
| `ka/ala_lc` | ALA-LC Georgian (2011) | Library catalogues | no |
| `ka/iso_9984` | ISO 9984:1996 | Data exchange; one letter per letter | **yes** |
| `ka/national` | Georgian national system (2002) | Road signs, passports, maps: *Tbilisi*, *Kutaisi* | no |

A scheme key alone is enough when the text or the key settles the script;
otherwise say `script="ka"` or use the qualified id. Reversible where the
standard is one-to-one; the others are documented as lossy and the library
refuses to guess rather than reverse them.

**The canonical fold.** One function that maps any of the above, script
or Latin, onto a single index form, so that index-time and query-time
normalisation agree. This is what a Solr or Elasticsearch analysis chain
calls. Each script owns its rules, because what should be merged differs
(Armenian folds *b* with *p*, Georgian must not), so Latin input names
the script it is to be folded for. The Armenian fold generalises the
script fold in Tetrak's Armenian recogniser and takes the orthography
findings of Tetrak brief 014 as its first test cases.

The schemes are for **display**; the fold is for **finding**. A fold key is
a deliberately coarse ASCII skeleton (`poghosian`, `kevork`, `haiastan`)
and must never be shown to a reader. Cross-script name-matching research
(LREC 2020) finds there is often no gold form to score against, and this
package does not pretend there is one.

## What it does not do

- **Translate.** Transliteration is the same words in different letters.
- **Guess at lossy reversals.** `transliterate(..., to="script")` works for
  ISO 9985, Hübschmann-Meillet and ISO 9984 and raises for the rest.
- **Fold every popular spelling.** Spellings that insert an unwritten
  schwa (*Megerdich* for `Մկրտիչ`), come through Russian (*Khachaturian*
  for `Խաչատրյան`, *Tiflis* for `თბილისი`) or are translations (*George*
  for `გიორგი`) do not fold to the script, and a classical Armenian `աւ`
  that reformed spelling turned into `օ` does not either. The test sets
  are the claim.
- **Handle every script.** Armenian and Georgian so far. The engine is
  script-agnostic and a new script is a package of tables; see
  [adding a script](https://scattercode.github.io/tetrak-translit/adding-a-script.html).

## Documentation

The user guide and API reference are at
[scattercode.github.io/tetrak-translit](https://scattercode.github.io/tetrak-translit/),
built from the released code at each release.

## Where it comes from

Built as part of [Tetrak](https://tetrak.dev/), a local-first OCR pipeline
for archival material, to support two use cases at once: a catalogue search that has to match records across scripts, and Tetrak's
own transcripts, where an ALA-LC rendering beside the OCR output is both a
catalogue-ready field and an accessibility one (a screen reader with no
Armenian voice can at least read the romanisation). Georgian came next
because Tetrak's recognisers are heading there; Syriac is planned.

## Contributing and licence

See [CONTRIBUTING.md](CONTRIBUTING.md) for the checks, the commit style and
the release automation, and [SECURITY.md](SECURITY.md) for reporting a
vulnerability. MIT licensed — see [LICENSE](LICENSE).
