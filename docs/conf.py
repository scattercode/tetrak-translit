"""Sphinx configuration for the tetrak-translit user guide and reference.

Published to GitHub Pages by .github/workflows/sphinx-docs.yml at each
release, so what it describes is the version on PyPI.
"""

from __future__ import annotations

project = "tetrak-translit"
copyright = "2026, Stephen Masters, Yvette Mankerian"
author = "Stephen Masters, Yvette Mankerian"

try:
    from tetrak_translit._version import version as release
except ImportError:  # a bare checkout, not yet built with hatch-vcs
    release = "0.0.0"

# hatch-vcs derives `release` from git describe, so on a commit that is not
# exactly a tag it carries PEP 440 build metadata ("0.2.0.dev2+g9f4085a79").
# The segment after "+" is a commit hash: noise in a browser tab. Stripped
# for display only; the ".devN" stays, as the honest signal that a build
# came from an untagged commit.
version = release.split("+", 1)[0]
html_title = f"{project} {version} documentation"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxarg.ext",
    "myst_parser",
]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
myst_heading_anchors = 3
root_doc = "index"

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/scattercode/tetrak-translit",
    "source_branch": "main",
    "source_directory": "docs/",
}
