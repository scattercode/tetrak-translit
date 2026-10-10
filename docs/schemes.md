# The romanisation schemes

Five schemes, each a versioned table written from its published standard.
They are for **display**: rendering Armenian for a reader in the form a
catalogue, a citation, a map or a passport would use. For matching across
them, use [the fold](fold.md).

| Key | Scheme | Standard | Where you meet it | Reversible |
|---|---|---|---|---|
| `ala_lc` | ALA-LC | ALA-LC Romanization Tables, Armenian (2011) | Library catalogues: Koha, WorldCat, the Library of Congress | no |
| `iso_9985` | ISO 9985 | ISO 9985:1996 | Data exchange; one letter per letter | yes |
| `bgn_pcgn` | BGN/PCGN | BGN/PCGN 1981 System | Maps and place names: *Yerevan*, *Gyumri* | no |
| `hubschmann_meillet` | Hübschmann-Meillet | Hübschmann (1897), Meillet (1913) | Linguistics and classical Armenian scholarship | yes |
| `western` | Western Armenian pronunciation | Common practice, not a standard | Diaspora names: *Hagop*, *Kevork*, *Boghosian* | no |

`tetrak-translit schemes` prints the same table with each scheme's
current version.

## The same name five ways

| Armenian | `ala_lc` | `iso_9985` | `bgn_pcgn` | `hubschmann_meillet` | `western` |
|---|---|---|---|---|---|
| Երևան | Erevan | Erewan | Yerevan | Erewan | Yerevan |
| Երեւան (classical) | Erewan | Erewan | Yerevan | Erewan | Yerevan |
| Յակոբ | Yakob | Yakob | Yakob | Yakob | Hagop |
| Գէորգ (classical) | Gēorg | Gēorg | Georg | Gēorg | Kevork |
| Պօղոսեան (classical) | Pōghosean | Pòġosean | Poghosean | Pōłosean | Boghosian |
| Չարենց | Chʻarentsʻ | Čarenc' | Ch'arents' | Čʿarencʿ | Charents |
| Ոսկան | Oskan | Oskan | Voskan | Oskan | Vosgan |

## What each one loses

A scheme is *reversible* when every Latin rendering maps back to exactly
one Armenian letter. Only two are:

- **ISO 9985** was designed for it: every letter is distinct, by diacritic
  where the plain letters run out. The cost is readability (`ու` is `ow`,
  `խ` is `x`, `ձ` is `j`).
- **Hübschmann-Meillet** is one letter per letter too, with Czech-style
  háčeks. `ու` is `u`, which would clash with `ո`+`ւ` — but reformed
  orthography never writes a free `ւ` after `ո`, and the classical
  digraph is the same two letters, so it reverses exactly.

The other three are lossy and `transliterate(..., to="armenian")` refuses
them rather than guess:

- **ALA-LC**: `ts` is `ծ` or `տ`+`ս`, `dz` is `ձ` or `դ`+`զ`, `kh` is `խ`
  or `կ`+`հ`, and so on for `ch`, `sh`, `zh`, `gh`.
- **BGN/PCGN**: the same digraph ambiguity, plus `y` is both `ը` and `յ`.
- **Western**: never meant to be reversed. It cannot say whether a *p* is
  `բ` or `փ`.

## Notes on each

### ALA-LC

The Library of Congress table has no positional rules: `ե` is `e` and
`ո` is `o` in every position, which is why the Library of Congress writes
*Erevan* and *Oskan* where BGN/PCGN writes *Yerevan* and *Voskan*.
Aspiration is marked with the modifier letter turned comma `ʻ` (U+02BB),
the character catalogue records actually carry. The ligature `և` is `ev`
but the letter `ւ` is `w`, so a classical-orthography imprint spelling
the city `Երեւան` romanises as *Erewan*: a real distinction in catalogue
records, not an error, and one the fold equates.

### ISO 9985

The international standard. Aspiration is a plain apostrophe; `ճ` is `č`
with a dot below and `չ` is plain `č`; `ը` is `ë` and `օ` is `ò`. Any
apostrophe-like character (`'`, `’`, `ʻ`, `ʿ`) is accepted on input when
reversing.

### BGN/PCGN

The system behind the English spellings of Armenian place names. It is
the only standard here with positional rules: `ե` is `ye` and `ո` is
`vo` at the start of a word, and `և` is `yev` there and `ev` elsewhere.
`ռ` is `rr`, `ը` is `y`. Written for reformed orthography; a classical
spelling goes through it letter by letter without the Western sound
values.

### Hübschmann-Meillet

The transcription of Armenian studies, from Hübschmann's *Armenische
Grammatik* and Meillet's *Altarmenisches Elementarbuch*, as the *Revue des
Études Arméniennes* uses it: `x` for `խ`, `ł` for `ղ`, `c` for `ծ`, `j`
for `ձ`, and the aspirates marked with `ʿ` (U+02BF).

### Western Armenian pronunciation

Not a standard but the practice: how names were spelled by sound in
Istanbul, Beirut, Aleppo, Paris and Los Angeles. Western Armenian swapped
the stops, so `բ` is *p* and `պ` is *b*, `գ` is *k* and `կ` is *g*, `դ`
is *t* and `տ` is *d*, and the affricates likewise. Word-initial `յ` is
*h* (*Hagop*), `ո` after a vowel is *vo* (*Kevork*), and the classical
digraphs `եա` and `իւ` are *ia* and *iu* (*Vartanian*, *Harutiun*). `ը`
is written *e*; many real spellings omit it (*Mkrtich*), which no table
can predict.

## Versioning

Each scheme carries its own `version`, separate from the package's. A
change to a mapping bumps it, so a stored string can say which table
produced it. Every table names the standard it was written from, and a
pull request changing one must cite the standard too; nothing is ever
copied from another implementation.
