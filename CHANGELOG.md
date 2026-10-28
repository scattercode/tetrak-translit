# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.3.0] - 2026-10-28

### Changed

- A Rule condition for the end of a word

## [4.2.0] - 2026-10-28

### Added

- Add Russian, with pre-reform spelling, ALA-LC and BGN/PCGN
- Add the tetrak-translit-russian skill

### Changed

- Bump ruff from 0.17.0 to 0.17.1

## [4.1.0] - 2026-10-22

### Changed

- Report the romanisation marks a Latin value carries
- Take certifi 2026.10.19 for GHSA-6q48-6c7w-9gw2

## [4.0.0] - 2026-10-19

### Changed

- Fold an initial հե, յե and ե onto one key

## [3.5.0] - 2026-10-18

### Changed

- Call the library stable
- Fold initial յե as հե and Western ds as ts, and freeze the Georgian basis
- Say Georgian on PyPI, test on Python 3.14, lint with RUF, type-check tests
- Run the guide's examples as tests

### Fixed

- Keep quotation marks on read-back, and harden the engine and registry

## [3.4.0] - 2026-10-18

### Changed

- Fold ye and vo after a hyphen or bracket as word-initial glides
- Keep BGN/PCGN y for ը after classical իւ at the end of a word
- Drop the intonation marks inside a word before folding
- Render a digraph whole when a mark is set inside it

### Fixed

- Declare the romanisation variants met in catalogue data

## [3.3.0] - 2026-10-18

### Changed

- Fold hay- compounds, Յ initials and the Western ivo glide

## [3.2.0] - 2026-10-16

### Changed

- Fold BGN/PCGN y for ը with the other schemes' vowel

## [3.1.0] - 2026-10-13

### Changed

- Record that a table or fold-rule change is never a patch
- Record the ISO 9984:2026 middle-dot defect in the skill
- Read Latin j as ձ when the text shows ISO 9985 or Hübschmann-Meillet

## [3.0.2] - 2026-10-13

### Changed

- Declare the իւր/հուր over-merge as a known gap

### Fixed

- Fold the classical իւ in Latin input as Armenian does

## [3.0.1] - 2026-10-12

### Fixed

- Render and fold Armenian presentation ligatures as their letters

## [3.0.0] - 2026-10-12

### Changed

- Keep marks inside words, and let a scheme map punctuation
- Romanise punctuation under ISO 9985:2026 (Table 2)
- Fold through a frozen copy of the 2011 ALA-LC table
- Follow the ALA-LC 2022 Armenian table, punctuation included

## [2.0.0] - 2026-10-12

### Changed

- Push the release commit as the scattercode-release App
- Follow ISO 9985:2026 and keep the 1996 table as iso_9985_1996
- Say that ISO 9984 has a second edition we have not checked
- Follow ISO 9984:2026 and keep the 1996 table as iso_9984_1996

### Fixed

- Read back capitals that have no precomposed form

## [1.0.0] - 2026-10-12

### Added

- Add agent skills and move the house rules to AGENTS.md

### Changed

- Let a dispatched release run past the skipped release job
- Describe the use case without naming a partner project
- Start the thin CLAUDE.md with a heading
- Fold Thoumanian, Hovannes and Ovanes onto their names

### Fixed

- Fix the release smoke test and allow republishing an existing tag

## [0.2.0] - 2026-10-10

### Changed

- Restructure around script packages and add Georgian

## [0.1.0] - 2026-10-10

### Added

- Add the Sphinx user guide and reference

### Changed

- Scaffold the repository with the workspace tooling
- Detect, transliterate and fold Armenian text

