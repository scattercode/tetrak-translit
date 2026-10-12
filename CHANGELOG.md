# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

