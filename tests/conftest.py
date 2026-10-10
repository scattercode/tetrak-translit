"""Shared fixtures: the fold test sets, one per script, read once."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import pytest

DATA = Path(__file__).parent / "data"

#: Script key to its fold-cases file.
FOLD_CASES = {path.name.split("_", 1)[0]: path for path in sorted(DATA.glob("*_fold_cases.tsv"))}


def read_groups(path: Path) -> dict[str, list[tuple[str, str]]]:
    """Group name to its (form, note) rows, in file order."""
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            groups[row["group"]].append((row["form"], row["note"]))
    return dict(groups)


@pytest.fixture(scope="session")
def fold_groups() -> dict[str, dict[str, list[tuple[str, str]]]]:
    """Script key to its groups."""
    return {script: read_groups(path) for script, path in FOLD_CASES.items()}
