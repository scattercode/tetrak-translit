# AGENTS.md

Guidance for anyone working in this repository with a coding agent --
Claude Code, Codex, Cursor, Gemini CLI or whatever else reads this file --
and a fair summary of the house rules for contributors who use none. The
rules are the repository's, not any one tool's; `CONTRIBUTING.md` has the
checks and the commit style at more length.

## What this repository is

**tetrak-translit** is a dependency-free Python library and CLI that
detects the script and orthography of a string, transliterates a script to
and from its named Latin schemes, and folds any spelling onto one
canonical index form for cross-script search. Armenian (five schemes, ISO 9985 in two editions) and
Georgian (three schemes, ISO 9984 in two editions) are the scripts so far; Syriac is planned. It was specified in Tetrak's
brief 015 (product zone, private), and is a separate repository rather than a fourth
`tetrak` package because its audience — catalogue and search developers —
will never install an OCR tool.

Published to PyPI as `tetrak-translit`; the import package is
`tetrak_translit`; the command is `tetrak-translit`. MIT licensed, the
same as Tetrak itself.

## Hard rules

### The engine is script-agnostic; a script is a package of data

`engine.py` reads a `Scheme` and the `Script` it belongs to, and nothing
else. A script lives in its own package (`hy/`, `ka/`) exporting `SCRIPT`,
`SCHEMES`, `fold_token` and `variant`, and is listed in `registry.py`.
Nothing above the registry names a script. Adding one is documented in
`docs/adding-a-script.md`; if adding a script needs a change to the
engine, the engine is wrong, not the script.

### Display and finding are different jobs

The schemes in `src/tetrak_translit/<script>/` render a script for a
reader. `fold()` produces a key for matching. Never make a scheme "more
matchable" (merging `եւ` and `և` at display time, say) and never make the
fold "more readable". ALA-LC writes *Erevan* for `Երևան` and *Erewan* for
`Երեւան` because catalogue records do; the fold is where they become one.

### Tables are written from the standards

Every table names the standard it was written from. Do not copy a table
from another implementation, whatever its licence; do not take anything
from a non-commercially-licensed source. A change to a mapping cites the
standard and bumps that scheme's `version`.

### The fold test sets are the published claim

`tests/data/<script>_fold_cases.tsv` is what we say folds together, per
script. Latin input to `fold()` must name its script, because the rules
differ (Armenian merges b/p, Georgian must not); never add a default. Every case must
keep passing; a new fold rule arrives with its cases; a gap that cannot be
closed without breaking a case is written up in `docs/fold.md` under known
gaps, not forced. A change to what the fold returns for an existing case
is a breaking change (`!` in the commit type).

### No runtime dependencies

`dependencies = []` in `pyproject.toml` is a feature. Standard library
only.

## Skills: the knowledge this file does not repeat

Four Markdown guides under `.claude/skills/<name>/SKILL.md` carry the
domain knowledge and the workflows. They are plain Markdown with a short
YAML header: **Claude Code loads them by name on demand; any other agent,
and any person, can simply read the files.** Open the matching one before
the work rather than reconstructing it:

- **`tetrak-translit-romanisation`** — what transliteration is and is not, the
  families of standards and who uses which, reversible against lossy, the
  display/finding split, and the Unicode mechanics (apostrophes, combining
  marks, normalisation, detection by character name) every table and fold
  rule depends on. Read for any question about romanisation, and before
  touching a table or the engine.
- **`tetrak-translit-armenian`** — the script, the two orthographies and the
  tells `detect()` uses, Eastern against Western pronunciation, the five
  schemes side by side, the fold's rules in order and its known gaps.
- **`tetrak-translit-georgian`** — Mkhedruli and Mtavruli, the scripts the
  library does not handle, the aspirate/ejective pairs and the apostrophe that
  runs the opposite way between ALA-LC and the national system (which ISO
  9984:2026 now follows), the schemes, the fold.
- **`tetrak-translit-extending`** — the workflows: correct a table, add a
  scheme, add a script (with Syriac design notes in its `references/`),
  extend a fold with its cases first; the hardcoded tests that go stale, the
  checks, and which commit type cuts which version. Its `scripts/probe.py`
  renders a name through every scheme and traces a fold rule by rule, and
  runs with the project's interpreter from the repository root.

## Layout

| Path | What |
|---|---|
| `src/tetrak_translit/script.py` | The `Script` and `Scheme` dataclasses: the data everything runs over |
| `src/tetrak_translit/engine.py` | Script to Latin and back, over any `Scheme` |
| `src/tetrak_translit/latin.py` | The cleaning and finishing every fold shares |
| `src/tetrak_translit/registry.py` | The registered script packages; scheme resolution |
| `src/tetrak_translit/detect.py` | Generic script detection; asks the script package for its variant |
| `src/tetrak_translit/transliterate.py` | Public transliteration API over the registry and engine |
| `src/tetrak_translit/fold.py` | Dispatches each token to its script's fold |
| `src/tetrak_translit/hy/` | Armenian: descriptor, six tables, orthography detector, fold |
| `src/tetrak_translit/ka/` | Georgian: descriptor, three tables, fold |
| `src/tetrak_translit/cli.py` | `tetrak-translit`, argparse |
| `tests/` | pytest; `tests/data/<script>_fold_cases.tsv` are the fold test sets |
| `docs/` | Sphinx (furo, MyST), published to GitHub Pages at each release |
| `.claude/skills/` | The four guides above; plain Markdown, readable by any tool |

## Checks

```bash
ruff check src tests docs && ruff format --check src tests docs
mypy
pytest --cov
uv lock --check
sphinx-build -W -b html docs docs/_build/html
```

All must pass before a commit; the lefthook hooks run most of them. The
Ruff rule set is declared in `pyproject.toml` — never rely on defaults.

## Conventions

- British English; sentence case for headings; first person plural in docs
  (this is a collaborative project).
- Conventional Commits, enforced by `.githooks/commit-msg`; pull request
  titles must be conventional too (`pr-title.yml`). `fix` → patch, `feat`
  → minor, `!` → major. Tooling commits use `chore(release):` or
  `chore(changelog):` so the changelog parser skips them.
- Releases, tags, the changelog and PyPI publication are automated by
  `release.yml` on every push to `main`. Never do any of them by hand.
- `cliff.toml` and `.githooks/commit-msg` are byte-for-byte copies of the
  templates in `scattercode/release-pipelines`; CI checks they have not
  drifted. Change them there, not here.
- Docstrings are Google style and are the API reference: Sphinx builds
  with `-W`, so a broken cross-reference fails the build.

## Related repositories

- [tetrak](https://github.com/scattercode/tetrak) — the OCR pipeline; will
  grow a `tetrak-ocr transliterate` command over this package.
- [tetrak-easyocr-armenian](https://github.com/scattercode/tetrak-easyocr-armenian)
  — the Armenian recogniser, whose `fold_script` this package's fold
  generalises.
- [tetrak-hy-trainer](https://github.com/scattercode/tetrak-hy-trainer) —
  whose `orthography` module measured the classical/reformed tells.
