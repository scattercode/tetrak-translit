# tetrak-translit

Detect, transliterate and fold text in scripts that have several
romanisations. A dependency-free Python library and command-line tool for
the problem every catalogue of Armenian or Georgian material has: the
same name exists in its own script, sometimes in more than one
orthography, and in three or five Latin spellings, and no stock search
engine treats them as one word.

```python
>>> import tetrak_translit as tt
>>> tt.detect("Երեւան").orthography
'classical'
>>> tt.transliterate("Երևան", "ala_lc")
'Erevan'
>>> tt.transliterate("თბილისი", "national")
'tbilisi'
>>> tt.fold("Boghossian", script="hy") == tt.fold("Պօղոսեան") == tt.fold("Poghosyan", script="hy")
True
>>> tt.fold("Chavchavadze", script="ka") == tt.fold("ჭავჭავაძე") == tt.fold("Čavčavaje", script="ka")
True
```

Three functions for three jobs. [Detection](usage.md#detection) says which
script a string is in and, for Armenian, which orthography.
[Transliteration](schemes.md) renders a script in a named romanisation
scheme, for display, and reads the reversible ones back. [The
fold](fold.md) maps every spelling onto one index form, for finding. The
schemes and the fold are different tools for different jobs, and this
documentation keeps saying so because conflating them is the commonest
mistake in cross-script search.

Two scripts so far: **Armenian** and **Georgian**. Each is a package of
tables that one engine runs over, and [adding a script](adding-a-script.md)
is a matter of writing another such package.

```{toctree}
:caption: Guide
:maxdepth: 1

installation
usage
schemes
fold
adding-a-script
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
