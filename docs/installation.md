# Installation

```bash
pip install tetrak-translit
```

Python 3.10 or later. There are no runtime dependencies: the package is
standard library only, so it can go into a search sidecar, a catalogue
script or an OCR pipeline without bringing anything with it.

The install provides the `tetrak_translit` import package and the
`tetrak-translit` command.

```bash
tetrak-translit --version
tetrak-translit schemes
```

## From source

```bash
git clone https://github.com/scattercode/tetrak-translit
cd tetrak-translit
uv venv .venv && source .venv/bin/activate
uv pip install -e '.[dev,apidocs]'
pytest
```

See `CONTRIBUTING.md` in the repository for the checks and the commit
style.
