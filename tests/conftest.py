"""Shared fixtures: the fold test set, read once."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import pytest

FOLD_CASES = Path(__file__).parent / "data" / "fold_cases.tsv"


@pytest.fixture(scope="session")
def fold_groups() -> dict[str, list[tuple[str, str]]]:
    """Group name to its (form, note) rows, in file order."""
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with FOLD_CASES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            groups[row["group"]].append((row["form"], row["note"]))
    return dict(groups)
