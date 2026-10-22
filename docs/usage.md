# Usage

Everything is reachable from the top-level package, and every function
takes a string and returns one.

```python
import tetrak_translit as tt
```

## Scripts and schemes

Two scripts are registered, each by a short key: `hy` (Armenian) and
`ka` (Georgian). Each has its own romanisation schemes, identified by a
key within the script and by a qualified id across scripts:

| Script | Schemes |
|---|---|
| `hy` Armenian | `ala_lc`, `iso_9985`, `iso_9985_1996`, `bgn_pcgn`, `hubschmann_meillet`, `western` |
| `ka` Georgian | `ala_lc`, `iso_9984`, `iso_9984_1996`, `national` |

A scheme key alone is enough when the text settles which script is meant
(`transliterate("თბილისი", "ala_lc")`), or when only one script has a
scheme of that name (`"national"`, `"western"`). When neither is true,
say which: `script="ka"` or the qualified id `"ka/ala_lc"`. An ambiguous
key raises an error that names the choices rather than guessing.

## Detection

```python
>>> found = tt.detect("Ազգ եւ հայրենիք")
>>> found.script, found.key, found.orthography
('armenian', 'hy', 'classical')
>>> tt.detect("თბილისი").key
'ka'
>>> tt.detect("Republic of Armenia").script
'latin'
>>> tt.detect("Հայաստան / Armenia").script, tt.detect("Հայաստան / Armenia").dominant
('mixed', 'armenian')
```

`script` is the Unicode script name of the letters (`armenian`,
`georgian`, `latin`, `cyrillic`, any other), or `mixed` for letters from
more than one script, or `none`. `dominant` is the script with the most
letters. `key` is the registry key of the one registered script present,
ready to pass as `script=`, or `None`. For Armenian, `orthography` is:

- `classical` — the pre-1922 spelling, still used across the diaspora.
  Called on a free `ւ` outside the `ու` digraph (`իւր`, `հաւատք`, the
  two-letter `եւ`), a classical `եա`/`եօ` digraph, or an `է` inside a
  word.
- `reformed` — the Soviet reform's spelling, used in Armenia. Called on
  a `յ` between a consonant and a vowel (`Պողոսյան`) or the ligature `և`
  when no classical tell is present.
- `indeterminate` — the string reads the same under both. `Արմեն` is
  `Արմեն` in any orthography, and the function says so rather than guess.

Georgian has one orthography, so its `orthography` is `None`. The
Armenian tells come from the measurements in Tetrak brief 014; the
reasoning is in {mod}`tetrak_translit.hy.orthography`.

### Romanisation marks

A romanised title is written in the same letters as an English or French
one, and in catalogue search across scripts its language code often says
nothing. For any text with Latin letters, `romanisations` lists each
registered script whose romanisation marks it carries:

```python
>>> tt.detect("Keankʻi mĕ").romanisations
(Romanisation(key='hy', marks=('aspirate', 'e-breve'), distinctive=True),)
>>> tt.detect("Łazar Pʿarpecʿi").romanisations
(Romanisation(key='hy', marks=('scholarly',), distinctive=False),)
>>> tt.detect("Histoire de l’Arménie").romanisations
()
```

`marks` names every mark found, most distinctive first; `distinctive`
says whether any of them is one no other language's ordinary spelling
uses. The Armenian marks are in {mod}`tetrak_translit.hy.romanised`:

| Mark | What | Distinctive |
|---|---|---|
| `aspirate` | An apostrophe (`ʻ ’ ' ʼ`) after `t`, `k`, `p`, `c`, `ch` or `ts`, as ALA-LC, ISO 9985 and BGN/PCGN write the aspirate | yes |
| `combining-comma` | The aspirate as a combining comma above right (U+0315) | yes |
| `e-breve` | `ĕ` for `ը` | yes |
| `r-dot` | `ṛ` or `ṙ` for `ռ` | yes |
| `long-vowel` | `ē` or `ō` for `է` or `օ` | no |
| `caron-or-dot` | `ġ`, `č`, `š`, `ž` or `ǰ` | no: Czech, Slovak, Croatian |
| `scholarly` | `ʿ` for the aspirate, `ł` for `ղ`, `ə` for `ը` | no: Polish has `ł` |
| `german` | `tsch` or `sch`, as German romanisations write `չ` and `շ` | no |

The aspirate is not read in English `'s`, in a French elision after any
other consonant (`l’Arménie`, `jusqu’au`), or in `c'est`. On a
hand-judged sample of forty catalogue titles, the distinctive marks found
19 of 21 Armenian works and none of the other 19.

This is evidence for search and display, not a classification. A
romanisation without marks (*Erker*, *Hayery*) shows nothing, so never
use the result to exclude a record: use it to count, to rank, or to say
which records a fold will serve. Georgian has no marks yet.

## Transliteration

```python
>>> tt.transliterate("Երևան", "ala_lc")
'Erevan'
>>> tt.transliterate("Երևան", "bgn_pcgn")
'Yerevan'
>>> tt.transliterate("Յակոբ Պարոնեան", "western")
'Hagop Baronian'
>>> tt.transliterate("ქუთაისი", "ala_lc")
'kʻutʻaisi'
>>> tt.transliterate("ქუთაისი", "national")
'kutaisi'
```

Only the scheme's own script is touched; everything else passes through,
so a whole catalogue line can go in. Capitals carry across: a capital
letter capitalises its rendering, a word in capitals renders in capitals.
Georgian Mkhedruli has no capitals, so its renderings are lowercase
unless the source was set in Mtavruli.

The default scheme is `ala_lc`, the one library catalogues hold, for
whichever script the text is in. The schemes and what each is for are on
[their own page](schemes.md).

Punctuation follows each scheme's standard: ALA-LC moves Armenian's
question and exclamation marks to the end of the sentence, ISO 9985
converts every mark where it stands, and the schemes whose standards say
nothing leave punctuation alone ([details](schemes.md#punctuation)).

```python
>>> tt.transliterate("Դու կարդացե՞լ ես այս գիրքը։", "ala_lc")
'Du kardatsʻel es ays girkʻě?'
>>> tt.transliterate("Դու կարդացե՞լ ես այս գիրքը։", "iso_9985")
"Dow kardac'e?l es ays girk'ë."
```

Two ALA-LC rules hold only in classical orthography (a word-initial `յ`
is `ḥ`). The orthography is detected from the text, but a single name
often has nothing to tell by, so say it when you know it:

```python
>>> tt.transliterate("Յակոբ", "ala_lc")
'Yakob'
>>> tt.transliterate("Յակոբ", "ala_lc", orthography="classical")
'Ḥakob'
```

Reading Latin back works for the schemes whose tables are one-to-one:

```python
>>> tt.transliterate("Erewan", "iso_9985", to="armenian")
'Երևան'
>>> tt.transliterate("Tbilisi", "iso_9984", to="script")
'თბილისი'
>>> tt.transliterate("Erevan", "hy/ala_lc", to="script")
Traceback (most recent call last):
  ...
tetrak_translit.engine.NotReversibleError: ALA-LC (hy/ala_lc) is not reversible: ...
```

`to` is `"latin"` (the default), `"script"`, or a script key or name.
The refusal is deliberate. ALA-LC `zh` is `ժ` and also `զ` + `հ`; a
library that guessed would be wrong often enough to be worse than one
that says it cannot know. For matching names across schemes, which needs
no guessing, use the fold.

## The fold

```python
>>> tt.fold("Պօղոսեան")
'poghosian'
>>> tt.fold("Boghossian", script="hy")
'poghosian'
>>> tt.fold("ჭავჭავაძე")
'chavchavaje'
>>> tt.fold("Ch'avch'avadze", script="ka")
'chavchavaje'
```

`fold` returns a lowercase ASCII key. It is for comparing and indexing,
never for display: `kevork`, `hakop` and `mckheta` are not spellings
anyone should see. Index with it and query with it, and a record
catalogued one way is found by a reader who types another.

Text in a registered script is recognised and folded by that script's
rules. Latin text needs `script=`, because the rules differ: Armenian
merges *b* with *p* (Eastern *Boghosian*, Western *Poghosyan*) and
Georgian must not (`ბ` and `პ` never swap). Folding Latin with no script
raises rather than silently applying the wrong rules. The rules, and the
gaps, are on [the fold page](fold.md).

When the Latin input is known to be in a reversible scheme, say so and
the fold reads each Latin token back exactly before folding, leaving any
token already in the script as it is. That removes the one
ambiguity the Armenian heuristic has, ISO 9985 and Hübschmann-Meillet `j`
for `ձ`, in the case the heuristic cannot settle: a text with no other
mark of the scheme. *Jowkn* needs no hint, because ISO's *ow* shows the
scheme; a lone *Jayn* does:

```python
>>> tt.fold("Jowkn", script="hy") == tt.fold("Ձուկն")
True
>>> tt.fold("Jayn", scheme="iso_9985") == tt.fold("Ձայն")
True
```

## In a search index

The fold is designed to be called at index time and at query time, with
the same function on both sides. A typical arrangement with Solr or
Elasticsearch is a small service, or an update processor, that adds a
`*_fold` copy of each title and name field, and a query parser that folds
the user's input before searching that field. Because the output is
plain ASCII, the folded field needs nothing more than a whitespace
tokeniser. Keep the original field too, for display and for exact
search. An index holding both Armenian and Georgian material folds a
Latin query under each script and searches for either key.

## On the command line

Each subcommand takes its text as arguments or, with none given, one
string per line on standard input, so a column from a spreadsheet can be
piped straight through.

```bash
tetrak-translit detect "Երեւան" "თბილისი"
tetrak-translit detect --json < titles.txt
tetrak-translit transliterate --scheme bgn_pcgn "Երևան"
tetrak-translit transliterate --scheme national "თბილისი"
tetrak-translit transliterate --scheme iso_9984 --to script "Tbilisi"
cut -f2 records.tsv | tetrak-translit fold --script hy > keys.txt
tetrak-translit schemes --json
```

Exit status is 0 on success and 2 for an unknown or ambiguous scheme, a
lossy reversal, or Latin folded with no script, with the reason on
standard error. The full option list is in the [command-line
reference](cli.md).
