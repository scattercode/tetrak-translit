# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repository is

**tetrak-translit** is a dependency-free Python library and CLI that
detects the script and orthography of a string, transliterates Armenian to
and from five named Latin schemes, and folds any spelling onto one
canonical index form for cross-script search. It was specified in Tetrak's
brief 015 (product zone, private) as part 3 of the Armenian heritage
aggregator work, and is a separate repository rather than a fourth
`tetrak` package because its audience — catalogue and search developers —
will never install an OCR tool.

Published to PyPI as `tetrak-translit`; the import package is
`tetrak_translit`; the command is `tetrak-translit`. MIT licensed, the
same as Tetrak itself.

## Hard rules

### Display and finding are different jobs

The schemes in `src/tetrak_translit/schemes/` render Armenian for a
reader. `fold()` produces a key for matching. Never make a scheme "more
matchable" (merging `եւ` and `և` at display time, say) and never make the
fold "more readable". ALA-LC writes *Erevan* for `Երևան` and *Erewan* for
`Երեւան` because catalogue records do; the fold is where they become one.

### Tables are written from the standards

Every table names the standard it was written from. Do not copy a table
from another implementation, whatever its licence; do not take anything
from a non-commercially-licensed source. A change to a mapping cites the
standard and bumps that scheme's `version`.

### The fold test set is the published claim

`tests/data/fold_cases.tsv` is what we say folds together. Every case must
keep passing; a new fold rule arrives with its cases; a gap that cannot be
closed without breaking a case is written up in `docs/fold.md` under known
gaps, not forced. A change to what the fold returns for an existing case
is a breaking change (`!` in the commit type).

### No runtime dependencies

`dependencies = []` in `pyproject.toml` is a feature. Standard library
only.

## Layout

| Path | What |
|---|---|
| `src/tetrak_translit/detect.py` | Script and orthography detection |
| `src/tetrak_translit/schemes/` | One module per romanisation table, plus the `Scheme` dataclass |
| `src/tetrak_translit/transliterate.py` | The engine over the tables, both directions |
| `src/tetrak_translit/fold.py` | The canonical fold |
| `src/tetrak_translit/cli.py` | `tetrak-translit`, argparse |
| `tests/` | pytest; `tests/data/fold_cases.tsv` is the fold test set |
| `docs/` | Sphinx (furo, MyST), published to GitHub Pages at each release |

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
