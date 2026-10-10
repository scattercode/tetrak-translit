# tetrak-translit

Detect, transliterate and fold Armenian text. A dependency-free Python
library and command-line tool for the problem every Armenian catalogue has:
the same name exists in Armenian script in two orthographies and in four or
five Latin spellings, and no stock search engine treats them as one word.

```python
>>> import tetrak_translit as tt
>>> tt.detect("Երեւան").orthography
'classical'
>>> tt.transliterate("Երևան", "ala_lc")
'Erevan'
>>> tt.fold("Boghossian") == tt.fold("Պօղոսեան") == tt.fold("Poghosyan")
True
```

Three functions for three jobs. [Detection](usage.md#detection) says which
script and orthography a string is in. [Transliteration](schemes.md)
renders Armenian in a named romanisation scheme, for display, and reads the
reversible ones back. [The fold](fold.md) maps every spelling onto one
index form, for finding. The schemes and the fold are different tools for
different jobs, and this documentation keeps saying so because conflating
them is the commonest mistake in cross-script search.

```{toctree}
:caption: Guide
:maxdepth: 1

installation
usage
schemes
fold
```

```{toctree}
:caption: Reference
:maxdepth: 1

cli
api
```

Built as part of [Tetrak](https://tetrak.dev/), a local-first OCR pipeline
for archival material. Source, issues and the changelog are on
[GitHub](https://github.com/scattercode/tetrak-translit).
