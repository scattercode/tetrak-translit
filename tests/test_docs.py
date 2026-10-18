"""The examples in the README and the guide run, so they cannot drift.

Every ``>>>`` line in a ``python`` fence of the Markdown pages is run as a
doctest. Plain ``--doctest-glob`` cannot do this: it reads the closing
fence as expected output. The fences are stripped here and the package is
imported as ``tt``, which is how every page introduces it.
"""

from __future__ import annotations

import doctest
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def examples(page: Path) -> str:
    blocks = [block for block in FENCE.findall(page.read_text(encoding="utf-8")) if ">>>" in block]
    return "\n".join(blocks)


@pytest.mark.parametrize("page", [page for page in PAGES if examples(page)], ids=lambda p: p.name)
def test_the_examples_on_the_page_hold(page: Path) -> None:
    source = ">>> import tetrak_translit as tt\n" + examples(page)
    test = doctest.DocTestParser().get_doctest(source, {}, page.name, str(page), 0)
    runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
    report: list[str] = []
    runner.run(test, out=report.append)
    assert runner.failures == 0, "".join(report)
    assert runner.tries > 0


def test_the_pages_with_examples_are_the_ones_expected() -> None:
    """A page that loses its examples should be noticed, not silently skipped."""
    assert {page.name for page in PAGES if examples(page)} == {
        "README.md",
        "fold.md",
        "index.md",
        "usage.md",
    }
