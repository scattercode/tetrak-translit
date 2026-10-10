# Usage

Everything is reachable from the top-level package, and every function
takes a string and returns one.

```python
import tetrak_translit as tt
```

## Detection

```python
>>> found = tt.detect("Ազգ եւ հայրենիք")
>>> found.script
'armenian'
>>> found.orthography
'classical'
>>> tt.detect("Republic of Armenia").script
'latin'
>>> tt.detect("Հայաստան / Armenia").script
'mixed'
>>> tt.detect("Հայաստան / Armenia").dominant
'armenian'
```

`script` is one of `armenian`, `latin`, `cyrillic`, `mixed` (letters
from more than one of those) or `none` (no letters at all). `dominant`
is the script with the most letters. For a string with any Armenian in
it, `orthography` is one of:

- `classical` — the pre-1922 spelling, still used across the diaspora.
  Called on a free `ւ` outside the `ու` digraph (`իւր`, `հաւատք`, the
  two-letter `եւ`), a classical `եա`/`եօ` digraph, or an `է` inside a
  word.
- `reformed` — the Soviet reform's spelling, used in Armenia. Called on
  a `յ` between a consonant and a vowel (`Պողոսյան`) or the ligature `և`
  when no classical tell is present.
- `indeterminate` — the string reads the same under both. `Արմեն` is
  `Արմեն` in any orthography, and the function says so rather than guess.

The counts the verdict rests on are in `found.markers`, and
`found.as_dict()` gives a JSON-ready view. The tells come from the
measurements in Tetrak brief 014; the reasoning is in the module
docstring of {mod}`tetrak_translit.detect`.

## Transliteration

```python
>>> tt.transliterate("Երևան", "ala_lc")
'Erevan'
>>> tt.transliterate("Երևան", "bgn_pcgn")
'Yerevan'
>>> tt.transliterate("Յակոբ Պարոնեան", "western")
'Hagop Baronian'
>>> tt.transliterate("Չարենց", "iso_9985")
"Čarenc'"
```

Only the Armenian in the string is touched; Latin, digits and
punctuation pass through, so a whole catalogue line can go in. Capitals
carry across: a capital letter capitalises its rendering, a word in
capitals renders in capitals.

The default scheme is `ala_lc`, the one library catalogues hold. The
schemes and what each is for are on [their own page](schemes.md).

Reading Latin back into Armenian works for the schemes whose tables are
one-to-one:

```python
>>> tt.transliterate("Erewan", "iso_9985", to="armenian")
'Երևան'
>>> tt.transliterate("Erevan", "ala_lc", to="armenian")
Traceback (most recent call last):
  ...
tetrak_translit.transliterate.NotReversibleError: ALA-LC is not reversible: ...
```

The refusal is deliberate. ALA-LC `ts` is `ծ` and also `տ` + `ս`; a
library that guessed would be wrong often enough to be worse than one
that says it cannot know. For matching names across schemes, which needs
no guessing, use the fold.

## The fold

```python
>>> tt.fold("Պօղոսեան")
'poghosian'
>>> tt.fold("Boghossian")
'poghosian'
>>> tt.fold("Poghosyan")
'poghosian'
```

`fold` returns a lowercase ASCII key. It is for comparing and indexing,
never for display: `kevork`, `hakop` and `haiastan` are not spellings
anyone should see. Index with it and query with it, and a record
catalogued one way is found by a reader who types another. The rules,
and the gaps, are on [the fold page](fold.md).

When the Latin input is known to be in a reversible scheme, say so and
the fold reads it back exactly before folding, which removes the one
ambiguity the heuristic has:

```python
>>> tt.fold("Jowkn", scheme="iso_9985") == tt.fold("Ձուկն")
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
search.

## On the command line

Each subcommand takes its text as arguments or, with none given, one
string per line on standard input, so a column from a spreadsheet can be
piped straight through.

```bash
tetrak-translit detect "Երեւան" "Yerevan"
tetrak-translit detect --json < titles.txt
tetrak-translit transliterate --scheme bgn_pcgn "Երևան"
tetrak-translit transliterate --scheme iso_9985 --to armenian "Erewan"
cut -f2 records.tsv | tetrak-translit fold > keys.txt
tetrak-translit schemes --json
```

Exit status is 0 on success and 2 for an unknown scheme or a lossy
reversal, with the reason on standard error. The full option list is in
the [command-line reference](cli.md).
