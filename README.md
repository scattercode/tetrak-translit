# tetrak-translit

Detect, transliterate and fold Armenian text. A dependency-free Python
library and command-line tool for the problem every Armenian catalogue
has: the same name exists in Armenian script in two orthographies and in
four or five Latin spellings, and no stock search engine treats them as
one word.

> **Status: alpha.** The tables and the fold are tested against the set in
> [`tests/data/fold_cases.tsv`](tests/data/fold_cases.tsv); what is not in
> that set is not claimed. See [known gaps](#what-it-does-not-do).

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
>>> tt.fold("Yerevan") == tt.fold("Երեւան") == tt.fold("Erewan")
True
>>> tt.fold("Boghossian") == tt.fold("Պօղոսեան") == tt.fold("Poghosyan")
True
```

```bash
$ tetrak-translit detect "Ազգ եւ հայրենիք"
armenian (classical)	Ազգ եւ հայրենիք
$ tetrak-translit transliterate --scheme iso_9985 "Չարենց"
Čarenc'
$ tetrak-translit transliterate --scheme iso_9985 --to armenian "Čarenc'"
Չարենց
$ cut -f2 titles.tsv | tetrak-translit fold
```

## Three jobs

**Detection.** Which script a string is in and, for Armenian, which
orthography: *classical* (everything printed before the 1922 reform, and
the diaspora still), *reformed* (Soviet and post-Soviet Armenia) or
*indeterminate* (the string reads the same under both). Character ranges
plus a few orthographic tells, chiefly a free `ւ` outside the `ու`
digraph.

**Transliteration**, between Armenian and five named Latin schemes, each a
versioned, tested table written from its published standard:

| Key | Scheme | Where you meet it | Reversible |
|---|---|---|---|
| `ala_lc` | ALA-LC (2011) | Library catalogues: Koha, WorldCat, the Library of Congress | no |
| `iso_9985` | ISO 9985:1996 | Data exchange; one letter per letter | **yes** |
| `bgn_pcgn` | BGN/PCGN 1981 | Maps and place names: *Yerevan*, *Gyumri* | no |
| `hubschmann_meillet` | Hübschmann-Meillet | Linguistics and classical scholarship | **yes** |
| `western` | Western Armenian pronunciation | Diaspora names: *Hagop*, *Kevork*, *Boghosian* | no |

Reversible where the standard is one-to-one; the others are documented as
lossy and the library refuses to guess rather than reverse them.

**The canonical fold.** One function that maps any of the above, Armenian
or Latin, onto a single index form, so that index-time and query-time
normalisation agree. This is what a Solr or Elasticsearch analysis chain
calls. It generalises the script fold in Tetrak's Armenian recogniser and
takes the orthography findings of Tetrak brief 014 as its first test cases.

The schemes are for **display**; the fold is for **finding**. A fold key is
a deliberately coarse ASCII skeleton (`poghosian`, `kevork`, `haiastan`)
and must never be shown to a reader. Cross-script name-matching research
(LREC 2020) finds there is often no gold form to score against, and this
package does not pretend there is one.

## What it does not do

- **Translate.** Transliteration is the same words in different letters.
- **Guess at lossy reversals.** `transliterate(..., to="armenian")` works for
  ISO 9985 and Hübschmann-Meillet and raises for the rest.
- **Fold every popular spelling.** Spellings that insert an unwritten
  schwa (*Megerdich* for `Մկրտիչ`) or come through Russian (*Khachaturian*
  for `Խաչատրյան`) do not fold to the Armenian, and a classical `աւ` that
  reformed spelling turned into `օ` does not either. The test set is the
  claim.

## Documentation

The user guide and API reference are at
[scattercode.github.io/tetrak-translit](https://scattercode.github.io/tetrak-translit/),
built from the released code at each release.

## Where it comes from

Built as part of [Tetrak](https://tetrak.dev/), a local-first OCR pipeline
for archival material, for two users at once: an Armenian cultural heritage
aggregator that has to match catalogue records across scripts, and Tetrak's
own Armenian transcripts, where an ALA-LC rendering beside the OCR output
is both a catalogue-ready field and an accessibility one (a screen reader
with no Armenian voice can at least read the romanisation).

## Contributing and licence

See [CONTRIBUTING.md](CONTRIBUTING.md) for the checks, the commit style and
the release automation, and [SECURITY.md](SECURITY.md) for reporting a
vulnerability. MIT licensed — see [LICENSE](LICENSE).
