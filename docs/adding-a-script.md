# Adding a script

The engine knows nothing about any particular script. A script is a
package of data — a descriptor, some tables, a fold — that the engine
runs over, and the registry is the one place that lists them. Adding
Syriac, say, is the work below and nothing else; nothing in
`detect.py`, `engine.py`, `transliterate.py`, `fold.py` or `cli.py`
changes.

## 1. The package

Create `src/tetrak_translit/<key>/` where `<key>` is the short code
users will type (`hy`, `ka`; use the ISO 639 code of the language the
script is used for, or the ISO 15924 script code if the script serves
several). Its `__init__.py` exports five names:

| Name | What |
|---|---|
| `SCRIPT` | A {class}`~tetrak_translit.script.Script`: the alphabet, archaic letters, digraphs every scheme must render, vowels, Unicode ranges, and whether the script has case |
| `SCHEMES` | `dict[str, Scheme]`, in the order the docs should list them |
| `fold_token(token, context=None)` | The script's fold: one whitespace-free token, in the script or in Latin, to its key. `context` is the whole text the token came from, for a rule that looks beyond the token; a fold with no such rule accepts and ignores it |
| `variant(text)` | Whatever the script has by way of orthographies or variants, as a string, or `None` |
| `MARKS` | A tuple of {class}`~tetrak_translit.script.RomanisationMark`: the signs that a Latin value is a romanisation of this script, most distinctive first. An empty tuple until they have been measured on real data |

The Georgian package is the smaller example to copy; the Armenian one
shows positional rules, digraphs, a variant detector and a fold with
pre-normalisation.

## 2. The tables

One module per scheme, each a {class}`~tetrak_translit.script.Scheme`
bound to the script. Write every table from the published standard and
name the standard in `standard=`. Never copy a table from another
implementation, whatever its licence: romanisation tables are facts, but
a copied file is still a copied file. Say in `notes=` where a reader
meets the scheme and what it loses, and set `reversible=True` only when
every rendering is distinct — the test suite checks that claim.

The {class}`~tetrak_translit.script.Scheme` constructor refuses a table
that misses a letter of the alphabet, renders a letter outside it, omits
a required digraph, or puts a positional rule on a unit it does not
define.

## 3. The fold

Decide what the fold should merge for this script, and write it as
rules. {mod}`tetrak_translit.latin` provides the cleaning every fold
starts with (lowercase, diacritics off, apostrophes off) and the finish
every fold ends with (ASCII only, doubled letters collapsed); between
them go the script's own merges. Render the script side through one
scheme, usually ALA-LC, so that the script and its catalogue
romanisation reach the Latin rules by the same road; and render it
through a frozen copy of that table kept in the fold module, not the
scheme itself, so that following a new edition of the standard never
moves a key that a search index already holds. Both existing folds do
this (`_BASIS`).

A script whose text is normally unvocalised (Syriac, Arabic) needs a
different kind of fold — consonantal, dropping vowels on the Latin side
as well — and a transliteration that is honest about what it cannot
recover from plain text. Design that before writing tables.

## 4. The test set

`tests/data/<key>_fold_cases.tsv`: groups of spellings that must fold
together, each with the script's own spelling and every scheme's
rendering, plus the popular spellings that actually occur. At least
fifteen groups. The existing fold tests pick the file up by name and run
every group; add the known gaps that cannot be closed to
`test_does_not_claim_the_known_gaps`, and write them up in `docs/fold.md`.

Add the script's known forms to `tests/test_transliterate.py` and a
round-trip test for each reversible scheme.

## 5. The registry and the docs

Register the package in `registry.py`'s `PACKAGES`. Add the script to
`docs/schemes.md` and `docs/fold.md`, the usage table, the README, and
the autosummary in `docs/api.md`. The command line, detection and the
qualified scheme ids pick the new script up from the registry.
