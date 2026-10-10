# The romanisation schemes

Each scheme is a versioned table written from its published standard.
They are for **display**: rendering a script for a reader in the form a
catalogue, a citation, a map or a passport would use. For matching across
them, use [the fold](fold.md).

`tetrak-translit schemes` prints every scheme with its current version.

## Armenian

| Id | Scheme | Standard | Where you meet it | Reversible |
|---|---|---|---|---|
| `hy/ala_lc` | ALA-LC | ALA-LC Romanization Tables, Armenian (2011) | Library catalogues: Koha, WorldCat, the Library of Congress | no |
| `hy/iso_9985` | ISO 9985 | ISO 9985:1996 | Data exchange; one letter per letter | yes |
| `hy/bgn_pcgn` | BGN/PCGN | BGN/PCGN 1981 System | Maps and place names: *Yerevan*, *Gyumri* | no |
| `hy/hubschmann_meillet` | Hübschmann-Meillet | Hübschmann (1897), Meillet (1913) | Linguistics and classical Armenian scholarship | yes |
| `hy/western` | Western Armenian pronunciation | Common practice, not a standard | Diaspora names: *Hagop*, *Kevork*, *Boghosian* | no |

The same name five ways:

| Armenian | `ala_lc` | `iso_9985` | `bgn_pcgn` | `hubschmann_meillet` | `western` |
|---|---|---|---|---|---|
| Երևան | Erevan | Erewan | Yerevan | Erewan | Yerevan |
| Երեւան (classical) | Erewan | Erewan | Yerevan | Erewan | Yerevan |
| Յակոբ | Yakob | Yakob | Yakob | Yakob | Hagop |
| Գէորգ (classical) | Gēorg | Gēorg | Georg | Gēorg | Kevork |
| Պօղոսեան (classical) | Pōghosean | Pòġosean | Poghosean | Pōłosean | Boghosian |
| Չարենց | Chʻarentsʻ | Čarenc' | Ch'arents' | Čʿarencʿ | Charents |
| Ոսկան | Oskan | Oskan | Voskan | Oskan | Vosgan |

### ALA-LC

The Library of Congress table has no positional rules: `ե` is `e` and
`ո` is `o` in every position, which is why the Library of Congress writes
*Erevan* and *Oskan* where BGN/PCGN writes *Yerevan* and *Voskan*.
Aspiration is marked with the modifier letter turned comma `ʻ` (U+02BB),
the character catalogue records actually carry. The ligature `և` is `ev`
but the letter `ւ` is `w`, so a classical-orthography imprint spelling
the city `Երեւան` romanises as *Erewan*: a real distinction in catalogue
records, not an error, and one the fold equates. Lossy: `ts` is `ծ` or
`տ`+`ս`, `dz` is `ձ` or `դ`+`զ`, `kh` is `խ` or `կ`+`հ`, and so on.

### ISO 9985

The international standard, designed to reverse: every letter is
distinct, by diacritic where the plain letters run out. Aspiration is a
plain apostrophe; `ճ` is `č` with a dot below and `չ` is plain `č`; `ը`
is `ë`, `օ` is `ò`, `ու` is `ow`. Any apostrophe-like character (`'`,
`’`, `ʻ`, `ʿ`) is accepted on input when reversing.

### BGN/PCGN

The system behind the English spellings of Armenian place names. It is
the only Armenian standard here with positional rules: `ե` is `ye` and
`ո` is `vo` at the start of a word, and `և` is `yev` there and `ev`
elsewhere. `ռ` is `rr`, `ը` is `y`. Written for reformed orthography; a
classical spelling goes through it letter by letter without the Western
sound values. Lossy: the same digraph ambiguity as ALA-LC, and `y` is
both `ը` and `յ`.

### Hübschmann-Meillet

The transcription of Armenian studies, from Hübschmann's *Armenische
Grammatik* and Meillet's *Altarmenisches Elementarbuch*, as the *Revue des
Études Arméniennes* uses it: `x` for `խ`, `ł` for `ղ`, `c` for `ծ`, `j`
for `ձ`, and the aspirates marked with `ʿ` (U+02BF). One letter per
letter, so it reverses. `ու` is `u`, which would clash with `ո`+`ւ`, but
reformed orthography never writes a free `ւ` after `ո` and the classical
digraph is the same two letters.

### Western Armenian pronunciation

Not a standard but the practice: how names were spelled by sound in
Istanbul, Beirut, Aleppo, Paris and Los Angeles. Western Armenian swapped
the stops, so `բ` is *p* and `պ` is *b*, `գ` is *k* and `կ` is *g*, `դ`
is *t* and `տ` is *d*, and the affricates likewise. Word-initial `յ` is
*h* (*Hagop*), `ո` after a vowel is *vo* (*Kevork*), and the classical
digraphs `եա` and `իւ` are *ia* and *iu* (*Vartanian*, *Harutiun*). `ը`
is written *e*; many real spellings omit it (*Mkrtich*), which no table
can predict. Never meant to be reversed: it cannot say whether a *p* is
`բ` or `փ`.

## Georgian

| Id | Scheme | Standard | Where you meet it | Reversible |
|---|---|---|---|---|
| `ka/ala_lc` | ALA-LC | ALA-LC Romanization Tables, Georgian (2011) | Library catalogues | no |
| `ka/iso_9984` | ISO 9984 | ISO 9984:1996 | Data exchange; one letter per letter | yes |
| `ka/national` | Georgian national system | Adopted 2002; BGN/PCGN 2009 | Road signs, passports, maps: *Tbilisi*, *Kutaisi* | no |

The same name three ways:

| Georgian | `ala_lc` | `iso_9984` | `national` |
|---|---|---|---|
| თბილისი | tʻbilisi | t'bilisi | tbilisi |
| ქუთაისი | kʻutʻaisi | k'ut'aisi | kutaisi |
| ჭავჭავაძე | chavchavadze | čavčavaje | ch'avch'avadze |
| წერეთელი | tseretʻeli | ceret'eli | ts'ereteli |
| მცხეთა | mtsʻkhetʻa | mc'xet'a | mtskheta |
| ყაზბეგი | qazbegi | qazbegi | q'azbegi |

Mkhedruli has no capitals, so a Georgian rendering is lowercase; a
catalogue capitalises proper names by its own convention. Mtavruli, the
capital forms Unicode added in 2018, renders as capitals.

### The apostrophe runs the opposite way

Georgian has pairs of aspirated and ejective consonants (`თ`/`ტ`,
`ფ`/`პ`, `ქ`/`კ`, `ჩ`/`ჭ`, `ც`/`წ`). ALA-LC and ISO 9984 mark the
**aspirate** with the apostrophe (`tʻbilisi`, `kʻutʻaisi`) and leave the
ejective plain. The national system marks the **ejective** (`ts'ereteli`,
`ch'avch'avadze`) and leaves the aspirate plain. The same apostrophe on
the same word therefore means opposite letters in the two systems, which
is the commonest source of confusion between them, and the reason the
fold strips the mark and merges each pair.

### ALA-LC

Aspirates with `ʻ` (U+02BB), ejectives plain. Defines the five archaic
letters (`ჱ ē`, `ჲ y`, `ჳ w`, `ჴ ẖ`, `ჵ ō`). Lossy: `dz`, `zh`, `gh`,
`sh` and `kh` can each be one letter or two.

### ISO 9984

One letter per letter, so it reverses: háčeks for the sibilants and
affricates (`ž š č ǰ`), `x` for `ხ`, `ḡ` for `ღ`, `j` for `ძ`, `c` for
`წ`, and a plain apostrophe on the aspirates. Defines the archaic letters
as ALA-LC does.

### The national system

The 2002 system of the Georgian State Department of Geodesy and
Cartography, adopted by BGN/PCGN in 2009: no diacritics, apostrophe on
the ejective. The spelling on signs, passports and maps. Does not define
the archaic letters, which pass through unchanged. Lossy.

## Versioning

Each scheme carries its own `version`, separate from the package's. A
change to a mapping bumps it, so a stored string can say which table
produced it. Every table names the standard it was written from, and a
pull request changing one must cite the standard too; nothing is ever
copied from another implementation.
