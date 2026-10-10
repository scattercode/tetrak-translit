# Contributing

Thanks for your interest in tetrak-translit. This document covers how we
work in this repository — the checks, the commit style, and the automation
they feed. It applies to us as much as to anyone sending a pull request.

## Before you start

Two constraints shape what we can accept:

- **Tables are written from the standards, never copied.** Romanisation
  tables are facts, but a copied file is still a copied file. Every table
  in `src/tetrak_translit/<script>/` names the published standard it was
  written from, and a change to one must cite the standard too. Nothing
  from a non-commercially-licensed transliteration source can be accepted,
  whatever its licence says about tables.
- **The folds are published claims.** `tests/data/<script>_fold_cases.tsv`
  is the set of spellings we say fold together for each script. A change
  to a fold's rules must keep every existing case passing, and a new
  capability must arrive with its cases. A gap that cannot be closed is
  documented in `docs/fold.md`, not papered over with a rule that breaks
  something else.
- **A new script is a package, not an engine change.** See
  `docs/adding-a-script.md`. If the engine has to change to admit a
  script, raise that as its own pull request first.

If you work with a coding agent — Claude Code, Codex, Cursor, Gemini CLI or
another — point it at `AGENTS.md`, which carries the repository's rules in
the form such tools read, and at the guides under `.claude/skills/`, which
are plain Markdown any tool or person can open. The rules there are the
same as here, stated for an agent.

## Getting set up

```bash
uv venv .venv && source .venv/bin/activate
uv pip install -e '.[dev,apidocs]'
```

(`python -m venv` and `pip` work too.) Then activate the git hooks — one of:

```bash
lefthook install                          # if you have lefthook (brew install lefthook)
git config core.hooksPath .githooks       # dependency-free fallback (commit-msg only)
```

The lefthook hooks run Ruff and the lockfile check before each commit, the
test suite and mypy before each push, and the Conventional Commits check on
every commit message.

## The checks

Everything the hooks and CI run, runnable by hand:

```bash
ruff check src tests docs
ruff format --check src tests docs
mypy
pytest --cov
uv lock --check                           # the lockfile matches pyproject.toml
sphinx-build -W -b html docs docs/_build/html
```

All of these must pass before a pull request can merge. The Ruff rule set
is declared explicitly in `pyproject.toml`; do not fall back to defaults.
Coverage must stay at or above the floor in `pyproject.toml`.

## Dependencies and the lockfile

The package has no runtime dependencies, and that is deliberate: it goes
into search sidecars, catalogue scripts and OCR pipelines alike. Keep it
that way. The development and documentation tooling is pinned in
`uv.lock` so that security scanning (Trivy in CI, Dependabot) sees real
resolved versions rather than ranges. After any change to an extra:

```bash
uv lock
```

and commit `uv.lock` alongside `pyproject.toml`. CI fails on a stale lock.

## Commit style

Commits follow [Conventional Commits](https://www.conventionalcommits.org/),
enforced by the shared hook in `.githooks/`:

```
<type>[(scope)][!]: <description>
```

- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
  `build`, `ci`, `chore`, `revert`.
- The description is non-empty, has no trailing full stop, and the header is
  100 characters or fewer (72 or fewer preferred).

This is load-bearing, not cosmetic: the release automation computes the next
semantic version from the commit types (`fix` → patch, `feat` → minor,
`!` → major) and generates `CHANGELOG.md` from the messages. Write the
message for the changelog reader. Pull requests are squash-merged, so the
PR title must be a Conventional Commit too; a workflow checks it.

A change to a scheme table is at least a `fix`, and bumps that table's
`version`; a change that alters what the fold returns for an existing
case is a breaking change and takes a `!`.

## Releases and the changelog

Releases are fully automated — never perform one by hand:

- Every push to `main` runs `release.yml`, which computes the next version
  from the commit history, updates `CHANGELOG.md`, tags, publishes a GitHub
  Release, builds the wheel, publishes it to PyPI with a Trusted Publisher,
  and then deploys the documentation for that tag.
- Never edit `CHANGELOG.md` manually and never create tags or Releases —
  fix the commit messages (or `cliff.toml`) instead.
- The package version comes from the git tag via `hatch-vcs`; there is no
  version literal to bump.

## Conventions

- British English throughout; sentence case for headings.
- Docs are written in the first person plural — this is a collaborative
  project.
- The audience is librarians' developers, search engineers and Armenian
  studies tooling, most of whom will never hear of Tetrak; write the
  README, the docs and the error messages for them.
- A scheme's docstring says what the standard is, where the scheme is met
  in the wild, and what it loses. Keep all three current.

## Security

Please report suspected vulnerabilities privately — see
[SECURITY.md](SECURITY.md), not the issue tracker.
