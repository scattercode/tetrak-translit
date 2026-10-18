---
name: tetrak-translit-extending
description: The workflows for changing tetrak-translit — correct a romanisation table, add a scheme to an existing script, add a whole new script package (Syriac design notes included), and extend or fix a fold with its test cases first. Covers the sequence for each, the hardcoded tests and docs that silently go stale, the Scheme validator and the reversibility tests, the rule-ordering traps in a fold, which commit type cuts which version (a table or fold-rule change is never a patch; a changed fold case is breaking), the checks to run and the probe script that renders a name through every scheme or traces a fold rule by rule. Load this whenever editing anything under src/tetrak_translit/hy/ or ka/, adding a scheme or a script, touching tests/data/*_fold_cases.tsv, debugging why two spellings do not fold together, planning Syriac, or preparing a commit or release in this repository.
---

# Extending tetrak-translit

Four kinds of change, each with a sequence and a set of things that fail
silently when skipped. Read the hard rules in `AGENTS.md` first; they are not
repeated here. Load `tetrak-translit-romanisation` for the concepts and the
per-script skill for the letters.

## Before anything

```bash
# the project's interpreter, from the repository root
.venv/bin/python -m pytest -q
```

If `.venv` is missing: `uv venv .venv && uv pip install -e '.[dev,apidocs]'`.
Every command below assumes the repository root and the venv's interpreter.

The two scripts bundled with this skill save repeated hand-work:

```bash
# every scheme's rendering of a text, its detection and its fold key
.venv/bin/python .claude/skills/tetrak-translit-extending/scripts/probe.py render "Երևան" "თბილისი"
# why several spellings do or do not reach one key: the fold, rule by rule
.venv/bin/python .claude/skills/tetrak-translit-extending/scripts/probe.py trace --script hy Պօղոսեան Boghossian Poghosyan
```

`trace` reads private names from the script packages (`_ORTHOGRAPHY`,
`_ARCHAIC`, `_LETTERS`, `_LATIN`) and checks its own result against the public
`fold_token()`, so if it ever disagrees with itself the fold module changed
shape and the script needs updating, not the fold.

## 1. Correcting a table

A mapping is wrong, or the standard says something the table does not.

1. **Find the sentence in the standard** that settles it. The fix cites the
   standard in the commit body and, if there is doubt about which edition, in
   the module docstring. Never settle it by comparing with another
   implementation.
2. Change the mapping and **bump the scheme's `version`** (`"1.0"` → `"1.1"`
   for a correction). Users may have stored strings that say which table
   produced them.
3. Update the module docstring, the matching section of `docs/schemes.md`
   and, if the letter is in it, the "same name N ways" table there and in the
   per-script skill.
4. Add or adjust the known form in `tests/test_transliterate.py`.
5. Run the full suite. **If a fold case changes its key, stop**: a change to
   what `fold()` returns for an existing case is a breaking change and the
   commit takes a `!`. Otherwise the commit is at least a `fix`.

## 2. Adding a scheme to an existing script

1. **One module per scheme** in `src/tetrak_translit/<key>/`, a `Scheme`
   bound to that package's `SCRIPT`. Copy the shape of the nearest existing
   one. Fill `standard=` with the published source by name and date,
   `notes=` with where a reader meets the scheme and what it loses, and a
   module docstring saying the same at more length — the docstring is the API
   reference.
2. The **`Scheme` constructor refuses** a table that misses a letter of the
   alphabet, renders a letter outside it, omits a required digraph (`ու` and
   `և` for Armenian) or puts a positional rule on a unit it does not define.
   Those errors fire at import, so the test suite will not even collect until
   the table is complete.
3. **`reversible=True` only when every rendering is distinct** and no
   positional rule exists; `test_reversible_schemes_are_one_to_one` and
   `TestToScript.test_round_trips_every_letter` check it. Any apostrophe-like
   mark in the table is treated as the aspiration mark on read-back.
4. **Add it to `SCHEMES`** in the package's `__init__.py`, in the order the
   docs should list it. The CLI's `schemes` subcommand, the registry and the
   qualified ids pick it up from there. If its key already exists in another
   script (as `ala_lc` does), a bare key becomes ambiguous and users need
   `script=` or the qualified id; the error message handles that.
5. **The fold must take its output back.** `TestAllSchemesFoldToTheirScript`
   runs every scheme's rendering of every script form in the test set through
   the fold and expects the script's own key; the renderings it is known not
   to take back are listed in its `KNOWN`, each a declared gap. A scheme that introduces a diacritic letter the fold
   has not seen (`ġ`, `ł`, `ẖ`) needs a `_LETTERS` entry in that script's fold,
   before NFKD strips the mark. Use `probe.py trace` on the failing sample.
6. Known forms in `tests/test_transliterate.py`; a round-trip test if
   reversible; add the scheme's renderings to a few groups in
   `tests/data/<key>_fold_cases.tsv` with a note naming the scheme.
7. Docs: the scheme table and a section in `docs/schemes.md`, the "same name
   N ways" table, the table in `docs/usage.md`, the README table, and the
   per-script skill's comparison table.
8. Commit: `feat(<key>): add the <name> scheme`. It cuts a minor release.

## 3. Adding a script

`docs/adding-a-script.md` is the public procedure: package with `SCRIPT`,
`SCHEMES`, `fold_token`, `variant`; tables from the standards; a fold; a case
set of at least fifteen groups; registration. Follow it, and also do these,
which it does not say:

- **Two tests hardcode the script list** and must be updated:
  `test_there_is_a_test_set_for_every_script` in `tests/test_fold.py`
  (`{"hy", "ka"}`) and `test_two_scripts_in_order` in `tests/test_registry.py`
  (`["hy", "ka"]`).
- **`unicode_name` must be the first word of the letters' Unicode character
  names, lowercased** (`unicodedata.name("ա").split()[0].lower()`), because
  that is how `detect()` finds the script; and **`ranges` must contain every
  letter and no other registered script's letters**
  (`test_script_ranges_do_not_overlap`, `test_every_letter_is_in_the_ranges`).
  A letter the ranges omit is detected and silently not rendered (and the
  fold drops it). If the script has compatibility characters that stand for
  letter sequences, list them in `compatibility` rather than widening the
  ranges, as Armenian does for its presentation ligatures.
- **`letters` are lowercase** and `test_every_letter_is_in_the_ranges` checks
  that. For a caseless script set `cased=False`, or Latin capitals on read-back
  will try to uppercase letters that have no uppercase.
- **`variant()` returns `None`** when the script has nothing to say; it is
  still required, because the registry calls it.
- **Four places mention the scripts by name**: the `description` in
  `cli.py`'s `build_parser()` ("Armenian and Georgian text"), the project
  `description`, `keywords` and `Natural Language` classifiers in
  `pyproject.toml`, the title and keywords in `CITATION.cff`, and the
  README's opening sentence. Update all four.
- **`docs/api.md`'s autosummary** lists each package; add the new one or the
  Sphinx build (`-W`) still passes but the reference is silently incomplete.
- Registry order is documentation order and CLI order; append.
- A **right-to-left or unvocalised script** needs its fold designed before its
  tables. `references/syriac-design-notes.md` holds the open questions for
  Syriac, the next script planned.
- Commit as one `feat` (not `feat!`): adding a script changes no existing
  behaviour, and the shared release action bumps **major on `!` even at 0.x**.

## 4. Extending or fixing a fold

The fold's failure modes are under-merging (two spellings of one name get two
keys) and over-merging (two names get one key). The second is worse and
harder to notice, which is why the sequence starts with cases.

1. **Add the cases first.** `tests/data/<key>_fold_cases.tsv` is tab-separated
   with the header `group\tform\tnote`; every line has exactly two tabs
   (`test_the_file_is_well_formed`). Put the new spelling in its group with a
   note saying where it comes from (which scheme, or "popular", "Western",
   "Russian-mediated"). If it is a new name, give the group the script's own
   spelling and every scheme's rendering too — `probe.py render` prints them.
2. **Run the suite and read the failure.** `test_every_group_folds_to_one_key`
   names every group that misses, with each form's key, in one assertion.
3. **Trace the divergence**: `probe.py trace --script <key> <form> <form>`
   prints the orthography step, the ALA-LC rendering, the `clean()` output and
   every `_LATIN` rule that changed the token, side by side, so the step at
   which two forms part company is visible.
4. **Write the rule where it belongs**:
   - A diacritic-bearing letter that should mean a digraph (`ž`→`zh`) goes in
     `_LETTERS`, because `clean()` applies that map before NFKD would turn `ž`
     into `z`.
   - A classical-to-reformed normalisation goes in `_ORTHOGRAPHY` (Armenian),
     on the script side, before ALA-LC rendering.
   - Everything else is a `_LATIN` rule, and **order matters**: digraph
     collapses before the single-letter merges that would break them; initial
     glides before the letter they produce is merged; `FINISH` last. When a
     later rule would eat part of a digraph an earlier rule must keep, protect
     it with the `\x01` placeholder and restore it afterwards, as `gh` is
     protected while `g` becomes `k`.
5. **Run everything again**, including `test_different_names_stay_different`
   (the over-merge check), `test_does_not_claim_the_known_gaps` and
   `TestAllSchemesFoldToTheirScript`. A new rule that makes a declared gap
   start passing is good news: move that pair from the gap test into the case
   set and out of `docs/fold.md`'s known gaps.
6. **A gap you cannot close without breaking a case** is not forced. Add the
   inequality to `test_does_not_claim_the_known_gaps`, write it up under
   known gaps in `docs/fold.md` and in the per-script skill, and leave it.
7. Update the rule table in `docs/fold.md` and in the per-script skill.
8. **Commit type**: never `fix`. A rule that moves no existing case is
   `feat`, even when it reads as a bug fix: it still changes the key of some
   real input (3.0.2's `iw` → `iu` moved no case and re-keyed every Latin
   value containing `iw`), and dependants who take patches automatically
   would find their index silently stale. One that changes any existing
   case's key is a breaking change, `feat!` or `fix!`, with the old and new
   keys in the body. Either way, say in the body which inputs now fold
   differently and that indexes must be rebuilt. Run the whole case file
   through `fold()` before and after and diff the keys if unsure.

## The checks, and what cuts a version

```bash
.venv/bin/ruff check src tests docs && .venv/bin/ruff format --check src tests docs
.venv/bin/python -m mypy
.venv/bin/python -m pytest --cov
uv lock --check                      # after any change to an extra: uv lock
.venv/bin/sphinx-build -W -b html docs docs/_build/html
```

All must pass; the lefthook hooks run Ruff and the lockfile check on commit,
tests and mypy on push, and the Conventional Commits check on every message.
Sphinx runs with `-W`, so a docstring cross-reference to a name that does not
exist fails the build. Docstrings are Google style.

| Change | Type | Release |
|---|---|---|
| A fix that changes no output for any input that already worked: a crash, an error message, performance, typing | `fix` | patch |
| Table correction; new fold rule or merge with no existing case moved; new scheme; new script | `feat` | minor |
| Any existing fold case's key or rendering changes | `feat!` / `fix!` | **major**, even at 0.x |

A change to a mapping table or a fold rule is **never a patch**, however
small: renderings are stored in catalogues and keys in search indexes, and
dependants take patch releases without looking. See `AGENTS.md`.
| Docs, tests, tooling, skills | `docs` / `test` / `chore` | none |

Releases, tags, the changelog and PyPI publication are automated on push to
`main`; never do any by hand. `cliff.toml` and `.githooks/commit-msg` are
byte-for-byte copies of `scattercode/release-pipelines` templates and CI checks
they have not drifted; change them there.

## Writing about it

British English, sentence case headings, first person plural in the docs
(this is a collaborative project). Describe the use case generically —
catalogue search across scripts, OCR transcripts with a romanisation beside
them — and never name partner projects. Each scheme's docstring says what the
standard is, where the scheme is met in the wild and what it loses; keep all
three current when anything changes.
