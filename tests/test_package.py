"""Packaging discipline: what pyproject.toml promises, the tree keeps."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import tetrak_translit

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_no_runtime_dependencies() -> None:
    """The one promise the README makes about installation."""
    assert re.search(r"^dependencies = \[\]$", PYPROJECT, re.MULTILINE)


def test_mit_licensed() -> None:
    assert 'license = "MIT"' in PYPROJECT
    assert (ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License")


def test_typed() -> None:
    assert (ROOT / "src" / "tetrak_translit" / "py.typed").exists()
    assert '"Typing :: Typed"' in PYPROJECT


def test_public_api_is_exported() -> None:
    for name in ("detect", "transliterate", "fold", "schemes", "scripts", "__version__"):
        assert name in tetrak_translit.__all__
        assert hasattr(tetrak_translit, name)


def test_only_the_standard_library_is_imported() -> None:
    """Checked on the source, not the environment, so a stray import fails here
    rather than in a user's bare interpreter."""
    package = ROOT / "src" / "tetrak_translit"
    allowed = {"argparse", "collections", "dataclasses", "json", "re", "sys", "unicodedata"}
    for module in package.rglob("*.py"):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = [node.module or ""]
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                assert top in allowed or top in {"tetrak_translit", "__future__"}, (
                    f"{module.name} imports {top}"
                )
