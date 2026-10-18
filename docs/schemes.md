# The romanisation schemes

Each scheme is a versioned table written from its published standard.
They are for **display**: rendering a script for a reader in the form a
catalogue, a citation, a map or a passport would use. For matching across
them, use [the fold](fold.md).

`tetrak-translit schemes` prints every scheme with its current version.

## Armenian

| Id | Scheme | Standard | Where you meet it | Reversible |
|---|---|---|---|---|
| `hy/ala_lc` | ALA-LC | ALA-LC Romanization Tables, Armenian (2022 version) | Library catalogues: Koha, WorldCat, the Library of Congress | no |
| `hy/iso_9985` | ISO 9985 | ISO 9985:2026 | Data exchange; one letter per letter | yes |
| `hy/iso_9985_1996` | ISO 9985:1996 | ISO 9985:1996, superseded | Data romanised under the first edition | yes |
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
| Պօղոսեան (classical) | Pōghosean | Pōġosean | Poghosean | Pōłosean | Boghosian |
| Չարենց | Chʻarentsʻ | Č'arenc' | Ch'arents' | Čʿarencʿ | Charents |
| Ոսկան | Oskan | Oskan | Voskan | Oskan | Vosgan |

### ALA-LC

Written from the 2022 version of the Library of Congress table. `ե` is
`e` and `ո` is `o` in every position, which is why the Library of
Congress writes *Erevan* and *Oskan* where BGN/PCGN writes *Yerevan* and
*Voskan*.
Aspiration is marked with the modifier letter turned comma `ʻ` (U+02BB),
the character catalogue records actually carry. The ligature `և` is `ev`
but the letter `ւ` is `w`, so a classical-orthography imprint spelling
the city `Երեւան` romanises as *Erewan*: a real distinction in catalogue
records, not an error, and one the fold equates. `ռ` is `ṛ`.

The 2022 table adds rules in its notes:

- **The soft sign** `ʹ` (U+02B9) goes between letters that would
  otherwise read as a digraph: `գհ` `gʹh`, `դզ` `dʹz`, `կհ` `kʹh`, `սհ`
  `sʹh`, `տս` `tʹs` (*patʹsparan*, *SSʹH*).
- **A lowercase `եվ` is `eʹv`.** Reformed spelling writes *ev* as `և`,
  so `ե` then `վ` is a compound (*oskeʹvaz*). The capitals `ԵՎ` and `Եվ`
  belong to the ligature and stay *EV*, *Ev*.
- **In classical orthography**, a word-initial `յ` is `ḥ` (*Ḥakob*), and
  `ե` at the start of a name and before a vowel is `y`. A name is taken
  to be a capitalised word; the start of a stem inside a compound is not
  detected. These rules need the orthography: pass
  `orthography="classical"` (or `--orthography classical`), or it is
  detected from the text. A lone `Յակոբ` has no tell, so without it the
  result is *Yakob*.

Lossy: the soft sign separates only the pairs the table lists, so `zh`
is still `ժ` or `զ`+`հ`, and an initial `y` may be `յ` or, in a
classical name, `ե`.

### ISO 9985

The international standard, designed to reverse: every letter is
distinct, by diacritic where the plain letters run out. `hy/iso_9985`
follows the second edition, ISO 9985:2026, which marks every aspirate the
same way: the unaspirated letter is plain and its aspirated partner takes
a plain apostrophe (U+0027), so `ծ`/`ց` are `c`/`c'` and `ճ`/`չ` are
`č`/`č'`, as `տ`/`թ` are `t`/`t'`. `ը` is `ë`, `օ` is `ō`, `ու` is `ow`.
Any apostrophe-like character (`'`, `’`, `ʻ`, `ʿ`) is accepted on input
when reversing.

Punctuation follows the standard's Table 2, each mark where it stands:

| Armenian | `։` | `՝` | `․` | `՞` | `՜` | `՛` | `֊` | `,` |
|---|---|---|---|---|---|---|---|---|
| ISO 9985 | `.` | `:` | `;` | `?` | `!` | `ˆ` | `-` | `,` |

The stress marks stay over their vowel, so `կարդացե՞լ` is `kardac'e?l`;
a mark set inside the `ու` digraph follows it, so `ելնելո՞ւ` is
`elnelow?`;
and reading back maps each Latin mark to its Armenian one: a full stop
in the Latin becomes `։`.

### ISO 9985:1996

The first edition, which the 2026 edition cancelled and replaced. It is
kept as `hy/iso_9985_1996` because data romanised under it stays in
catalogues and data sets, and only its own table reads that data back
into Armenian. It differs from the second edition in four letters: `ծ`
is `ç`, `ճ` is `č̣` (`č` with a dot below), `չ` is plain `č` and `օ` is
`ò`. The fold equates both editions, so either finds the other.

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

### Ligatures

The five presentation ligatures Unicode keeps for compatibility, `ﬓ ﬔ ﬕ
ﬖ ﬗ` (`մն մե մի վն մխ`), are typesetting, not spelling, and no standard
romanises them. Every scheme, and the fold, writes each out as its two
letters first: `ﬕայն` is *miayn* and folds with `միայն`.

### Punctuation

Each scheme does with Armenian punctuation what its standard says, and
nothing where the standard is silent:

| Mark | `ala_lc` | `iso_9985` | `iso_9985_1996`, `bgn_pcgn`, `hubschmann_meillet`, `western` |
|---|---|---|---|
| `։` full stop | `.` | `.` | unchanged |
| `՝` comma | unchanged | `:` | unchanged |
| `․` (U+2024) | unchanged | `;` | unchanged |
| `֊` hyphen | unchanged | `-` | unchanged |
| `« »` | `“ ”` | unchanged | unchanged |
| `՞` question | `?` at the end of the sentence | `?` where it stands | unchanged |
| `՜` exclamation | `!` at the end of the sentence | `!` where it stands | unchanged |
| `՛` emphasis | dropped | `ˆ` (U+02C6) where it stands | unchanged |

The stress marks `՞ ՜ ՛` are set over the stressed vowel, inside the
word, and a word does not end at them, so capitals and word-initial rules
see through them. ALA-LC writes a moved mark in place of the sentence's
`։`, or at the end of the line: `Ո՞վ է։` is *Ov ē?*. BGN/PCGN's
standard is for place names and says nothing about punctuation; we do
not have the text of ISO 9985:1996; Hübschmann-Meillet and the Western
spelling have no published rule.

## Georgian

| Id | Scheme | Standard | Where you meet it | Reversible |
|---|---|---|---|---|
| `ka/ala_lc` | ALA-LC | ALA-LC Romanization Tables, Georgian (2011) | Library catalogues | no |
| `ka/iso_9984` | ISO 9984 | ISO 9984:2026 | Data exchange; the national system made reversible | yes |
| `ka/iso_9984_1996` | ISO 9984:1996 | ISO 9984:1996, superseded | Data romanised under the first edition | yes |
| `ka/national` | Georgian national system | Adopted 2002; BGN/PCGN 2009 | Road signs, passports, maps: *Tbilisi*, *Kutaisi* | no |

The same name four ways:

| Georgian | `ala_lc` | `iso_9984` | `iso_9984_1996` | `national` |
|---|---|---|---|---|
| თბილისი | tʻbilisi | tbilisi | t'bilisi | tbilisi |
| ქუთაისი | kʻutʻaisi | kutaisi | k'ut'aisi | kutaisi |
| ჭავჭავაძე | chavchavadze | ch'avch'avadze | čavčavaje | ch'avch'avadze |
| წერეთელი | tseretʻeli | ts'ereteli | ceret'eli | ts'ereteli |
| მცხეთა | mtsʻkhetʻa | mtskheta | mc'xet'a | mtskheta |
| ყაზბეგი | qazbegi | q'azbegi | qazbegi | q'azbegi |

Mkhedruli has no capitals, so a Georgian rendering is lowercase; a
catalogue capitalises proper names by its own convention. Mtavruli, the
capital forms Unicode added in 2018, renders as capitals.

### The apostrophe runs the opposite way

Georgian has pairs of aspirated and ejective consonants (`თ`/`ტ`,
`ფ`/`პ`, `ქ`/`კ`, `ჩ`/`ჭ`, `ც`/`წ`). ALA-LC and ISO 9984:1996 mark the
**aspirate** with the apostrophe (`tʻbilisi`, `kʻutʻaisi`) and leave the
ejective plain. The national system, and ISO 9984:2026 after it, mark the
**ejective** (`ts'ereteli`, `ch'avch'avadze`) and leave the aspirate
plain. The same apostrophe on
the same word therefore means opposite letters in the two systems, which
is the commonest source of confusion between them, and the reason the
fold strips the mark and merges each pair.

### ALA-LC

Aspirates with `ʻ` (U+02BB), ejectives plain. Defines the five archaic
letters (`ჱ ē`, `ჲ y`, `ჳ w`, `ჴ ẖ`, `ჵ ō`). Lossy: `dz`, `zh`, `gh`,
`sh` and `kh` can each be one letter or two.

### ISO 9984

`ka/iso_9984` follows the second edition, ISO 9984:2026, which is a
different system from the first. It is based on the national system:
the same digraphs (`zh sh ch ts dz kh gh`) and the apostrophe on the
ejective, so for most words it gives exactly the national spelling
(*Tbilisi*, *Ts'ereteli*). What makes it reversible is a middle dot
(U+00B7) between two letters that would otherwise read as a digraph:
`z·h` is `ზ` and `ჰ`, not `ჟ`. The standard lists the pairs (`გ`, `ზ`,
`ს` or `ქ` before `ჰ`; `თ` before `ს`; `დ` before `ზ`), and the dot is
skipped when reading back. Two sequences the list does not cover still
read two ways, `dzh` (`ძჰ` or `დჟ`) and `tsh` (`ცჰ` or `თშ`); reading
back takes the first of each. It also defines fourteen letters that
standard Georgian does not use, the five archaic letters as ALA-LC has
them among them.

### ISO 9984:1996

The first edition, which the 2026 edition cancelled and replaced. It is
kept as `ka/iso_9984_1996` because data romanised under it stays in
catalogues and data sets, and only its own table reads that data back.
One letter per letter: háčeks for the sibilants and affricates
(`ž š č ǰ`), `x` for `ხ`, `ḡ` for `ღ`, `j` for `ძ`, `c` for `წ`, and a
plain apostrophe on the **aspirates**, so its `t'` is `თ` where the
second edition's is `ტ`. Defines the archaic letters as ALA-LC does, and
`ჶ` as `f`. The fold equates both editions.

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
