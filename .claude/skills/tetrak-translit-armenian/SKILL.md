---
name: tetrak-translit-armenian
description: Armenian as tetrak-translit handles it — the 38-letter alphabet and its Unicode ranges, the ու digraph and the և ligature, the classical (pre-1922, diaspora) and reformed (Soviet and post-Soviet) orthographies and the tells detect() uses to separate them, Eastern against Western pronunciation and the consonant swap that gives Hagop/Yakob and Boghosian/Poghosyan, the five schemes (ALA-LC, ISO 9985 in its 2026 and 1996 editions, BGN/PCGN, Hübschmann-Meillet, Western) letter by letter where they differ, the fold's rules in order and its known gaps, and the traps (ligatures, apostrophes, lookalikes). Load this whenever Armenian text, an Armenian name or place, an Armenian scheme key, the hy/ package, hy_fold_cases.tsv or the orthography detector comes up — including questions like "how is X romanised", "why does Y not fold with Z", "is this classical or reformed", or anything about -ian/-yan surnames.
---

# Armenian

The script the library was built for, and the harder of the two it handles:
two orthographies in daily use, two pronunciation traditions that romanise
the same name opposite ways, and five schemes in the wild. The tables in
`src/tetrak_translit/hy/` are the authority on individual letters; this skill
is the understanding behind them.

## The script

- **38 letters**: Mashtots' 36 (`ա`–`ք`) plus `օ` and `ֆ`, added in the
  Middle Ages. Cased. Lowercase `ա`–`ֆ` is U+0561–U+0586, uppercase
  U+0531–U+0556. `Script.ranges` is `(0x0531, 0x0556), (0x0560, 0x0588)`.
- **`ու`** is a digraph for /u/ and every scheme renders it as a unit
  (`u`, or `ow` in ISO 9985).
- **`և`** (U+0587) is the ligature of `ե` and `ւ`, lowercase only: `.upper()`
  gives the two letters `ԵՒ`. Reformed print sets the ligature; classical
  print mostly sets `եւ` as two letters but some classical presses set the
  ligature too, which is why it is a typographic habit and not an orthography
  tell on its own.
- **`ւ`** (U+0582) is a letter in classical orthography (`նաւ`, `իւր`,
  `հաւատք`) and only ever the second half of `ու` in reformed. That is the
  single most useful fact in this skill.
- **Punctuation is outside the ranges**: `՝ ՞ ՜ ՛ ՚` (U+055A–U+055F), the
  full stop `։` (U+0589), the hyphen `֊` (U+058A). Five of them are written
  *inside* a word and are the script's `marks`: the apostrophe `՚`
  (`կ՚ուզէ`), the abbreviation mark `՟` and the stress marks `՛ ՜ ՞`, set over
  the stressed vowel (`կարդացե՞լ`). A word does not end at a mark, so
  capitals and word-initial rules see through it. What a mark becomes is
  each scheme's `punctuation` (see "Punctuation" below); unmapped marks pass
  through where they stand (`k՚uzē`).
- **Presentation-form ligatures** `ﬓ ﬔ ﬕ ﬖ ﬗ` (U+FB13–U+FB17, for `մն մե մի
  վն մխ`) are detected as Armenian by name but are outside the ranges, so
  they are **not rendered**. NFKC would decompose them; the engine uses NFC.
  Known gap; see the romanisation skill.

## Two orthographies

The **1922 Soviet reform** (adjusted in 1940) changed no letters, only where
they appear. **Classical** (traditional, Mashtotsian) orthography is
everything printed before it and everything the diaspora has printed since;
**reformed** is Soviet and post-Soviet Armenia. Orthography is not dialect:
Western Armenian is written in classical orthography, but so is the Eastern
Armenian of Iran, and Soviet editions of Western authors were reset in
reformed spelling.

What the library normalises when it folds classical towards reformed
(`hy/fold.py`, `_ORTHOGRAPHY`):

| Classical | Reformed | Example |
|---|---|---|
| `եւ` | `և` | `Երեւան` / `Երևան` |
| `է` inside a word | `ե` | `սէր` / `սեր`, `Գէորգ` / `Գևորգ` |
| `եա` | `յա` | `Պօղոսեան` / `Պողոսյան`, the `-ean`/`-yan` of surnames |
| `իւ` | `յու` | `իւր` / `յուր` |
| `եո` | `եվո` | `Գէորգ` → *Gevorg* |
| final `յ` after a vowel | dropped | `ծառայ` / `ծառա` |

A classical `աւ` that reformed spelling writes `օ` is **not** normalised;
the fold reads `ւ` as *v* and this is a documented gap.

### How `detect()` decides (`hy/orthography.py`)

A single name is too short to measure a rate, so the verdict is on
**presence**, in this order:

1. A **free `ւ`** — one not preceded by `ո` — or a classical **`եա`/`եօ`
   digraph**, or an **`է` after another letter**: `classical`. A two-letter
   `եւ` always contains a free `ւ`, so it counts.
2. Otherwise a **`յ` between a consonant and a vowel** (`Պողոսյան`) or the
   **ligature `և`**: `reformed`.
3. Otherwise `indeterminate`: `Արմեն`, `հայ`, `Հայաստան` read the same under
   both, and the function says so rather than guess.

The tells came from tetrak-hy-trainer's `orthography` module, measured for
Tetrak brief 014 on 2026-10-08 across whole works: free `ւ` runs at about
17–21 per thousand letters on classical pages and under 1 on reformed ones,
with nothing in between, so one is enough. Two markers that look useful and
are not: the `եւ`/`և` habit (per press, 21 classical indexes to 16 in the
census), and a final `յ` after a vowel, which is classical in `ծառայ` but
reformed in `հայ` and `թեյ`; `markers()` reports it and `orthography()`
ignores it. A free `ւ` outranks a ligature, so a classical press that sets
`և` is still called classical.

## Two pronunciations

Eastern Armenian keeps a three-way stop series: voiced, voiceless, aspirated.
**Western Armenian collapsed it to two and swapped the voicing**, so a name
spelled by ear in Istanbul, Beirut, Aleppo, Paris or Los Angeles romanises the
opposite way from the same name in a Yerevan catalogue:

| Letters | Eastern (ALA-LC) | Western | Example |
|---|---|---|---|
| `բ` / `պ` / `փ` | b / p / pʻ | p / b / p | `Պօղոսեան` *Poghosean* / *Boghosian* |
| `գ` / `կ` / `ք` | g / k / kʻ | k / g / k | `Գէորգ` *Gēorg* / *Kevork*; `Կոմիտաս` *Komitas* / *Gomidas* |
| `դ` / `տ` / `թ` | d / t / tʻ | t / d / t | `Վարդան` *Vardan* / *Vartan*; `Տիգրան` *Tigran* / *Dikran* |
| `ձ` / `ծ` / `ց` | dz / ts / tsʻ | ts / dz / ts | `Մաշտոց` *Mashtotsʻ* / *Mashdots* |
| `ջ` / `ճ` / `չ` | j / ch / chʻ | ch / j / ch | |

Three more Western habits the `western` table encodes: word-initial `յ` is
*h* (`Յակոբ` *Hagop*, `Յարութիւն` *Harutiun*); `ո` after a vowel is *vo*
(`Գէորգ` *Kevork*); and the classical digraphs `եա` and `իւ` are *ia* and
*iu*, which is where the surname ending *-ian* comes from (`Վարդանեան`
*Vartanian*) against the reformed *-yan* (`Վարդանյան` *Vardanyan*). `ը` is
written *e* and many real spellings drop it, which no table can predict.

The fold's reason for merging `b`/`p`, `d`/`t`, `g`/`k`, `dz`/`ts` and
`j`/`ch` is this table: without the merge no Western spelling would ever find
an Eastern record.

## The five schemes

| Id | Standard | Met in | Aspiration mark | Reversible |
|---|---|---|---|---|
| `hy/ala_lc` | ALA-LC Romanization Tables, Armenian (2011) | Library catalogues; the default | `ʻ` U+02BB | no |
| `hy/iso_9985` | ISO 9985:2026 | Data exchange | `'` | yes |
| `hy/iso_9985_1996` | ISO 9985:1996, superseded | Data made under the first edition | `'` | yes |
| `hy/bgn_pcgn` | BGN/PCGN 1981 | Maps and place names | `'` | no |
| `hy/hubschmann_meillet` | Hübschmann 1897, Meillet 1913 | Linguistics, classical scholarship | `ʿ` U+02BF | yes |
| `hy/western` | Common practice, not a standard | Diaspora names | none | no |

Where they differ (the letters not listed render the same everywhere):

| | `ala_lc` | `iso_9985` | `bgn_pcgn` | `hubschmann_meillet` | `western` |
|---|---|---|---|---|---|
| `է` | ē | ē | e | ē | e |
| `ը` | ě | ë | y | ə | e |
| `թ` | tʻ | t' | t' | tʿ | t |
| `ժ` | zh | ž | zh | ž | zh |
| `խ` | kh | x | kh | x | kh |
| `ծ` | ts | c | ts | c | dz |
| `ձ` | dz | j | dz | j | ts |
| `ղ` | gh | ġ | gh | ł | gh |
| `ճ` | ch | č | ch | č | j |
| `չ` | chʻ | č' | ch' | čʿ | ch |
| `ջ` | j | ǰ | j | ǰ | ch |
| `ռ` | ṙ | ṙ | rr | ṙ | r |
| `ց` | tsʻ | c' | ts' | cʿ | ts |
| `ւ` | w | w | w | w | v |
| `փ` | pʻ | p' | p' | pʿ | p |
| `ք` | kʻ | k' | k' | kʿ | k |
| `օ` | ō | ō | o | ō | o |
| `ու` | u | ow | u | u | u |
| `և` | ev | ew | ev; *yev* initially | ew | ev; *yev* initially |
| `բ գ դ` / `պ կ տ` | b g d / p k t | same | same | same | **p k t / b g d** |
| initial `ե`, `ո` | e, o | e, o | **ye, vo** | e, o | **ye, vo** (`ո` also after a vowel) |
| initial `յ` | y | y | y | y | **h** |
| `եա`, `իւ` | letter by letter | same | same | same | **ia, iu** |

The same name five ways, from `docs/schemes.md`:

| Armenian | `ala_lc` | `iso_9985` | `bgn_pcgn` | `hubschmann_meillet` | `western` |
|---|---|---|---|---|---|
| Երևան | Erevan | Erewan | Yerevan | Erewan | Yerevan |
| Երեւան (classical) | Erewan | Erewan | Yerevan | Erewan | Yerevan |
| Յակոբ | Yakob | Yakob | Yakob | Yakob | Hagop |
| Գէորգ (classical) | Gēorg | Gēorg | Georg | Gēorg | Kevork |
| Պօղոսեան (classical) | Pōghosean | Pōġosean | Poghosean | Pōłosean | Boghosian |
| Չարենց | Chʻarentsʻ | Č'arenc' | Ch'arents' | Čʿarencʿ | Charents |
| Ոսկան | Oskan | Oskan | Voskan | Oskan | Vosgan |

Things worth knowing per scheme:

- **ALA-LC has no positional rules**: `ե` is `e` and `ո` is `o` everywhere,
  which is why the Library of Congress heading is *Erevan* and the atlas says
  *Yerevan*. `և` is `ev` but `ւ` is `w`, so a classical imprint's `Երեւան` is
  *Erewan* — a real distinction in catalogue records, not an error, and the
  fold is where the two become one. Never make the scheme "fix" it.
- **ISO 9985** is the one to choose for round-tripping; its oddities (`ow`,
  `x`, `j` for `ձ`, `ō`) exist to keep it one-to-one. `iso_9985` is the
  second edition (2026), which writes every aspirated/unaspirated pair as
  plain/apostrophe (`c`/`c'` for `ծ`/`ց`, `č`/`č'` for `ճ`/`չ`).
  `iso_9985_1996` is the superseded first edition, kept for data made under
  it: `ծ` `ç`, `ճ` `č̣` (two code points, no precomposed form), `չ` `č`, `օ`
  `ò`. The ISO column above is the 2026 edition. Both fold to the same keys.
- **BGN/PCGN** is the only standard here with positional rules and was written
  for reformed Eastern Armenian; a classical spelling goes through it letter by
  letter. `y` is both `ը` and `յ`, so it is lossy twice over.
- **Hübschmann-Meillet** renders `ու` as `u`, which would clash with `ո`+`ւ`,
  but reformed orthography never writes a free `ւ` after `ո` and the classical
  digraph is the same two letters, so it reverses exactly. Note `j` is `ձ` and
  `ǰ` is `ջ`, the reverse of the library convention.
- **Western** is a practice. It is the only scheme whose stop letters are
  swapped and the only one with an `after_vowel` rule. It can never be
  reversed because it cannot say whether a *p* is `բ` or `փ`.

## The fold (`hy/fold.py`)

Order of operations for one token:

1. **Armenian input** is lowercased, normalised classical → reformed by the
   `_ORTHOGRAPHY` rules above, and rendered through **ALA-LC**.
2. **`clean()`**: the `_LETTERS` map runs first (`ž`→`zh`, `š`→`sh`, `č`→`ch`,
   `ǰ`→`j`, `ġ`/`ł`→`gh`, `ç`→`c`, `ə`→`e`, `x`→`kh`), then NFKD strips the
   remaining diacritics and every apostrophe-like mark goes.
3. **The `_LATIN` rules, in this order**, each for a reason:

   | Rule | Why |
   |---|---|
   | `th` → `t`; `ph` → `p` | Older English and French aspirates: *Thoumanian*, *Thoros* |
   | `vh` → `v` | Popular *Hovannes* for *Hovhannes* |
   | `ow`, `ou`, `oo` → `u` | ISO `ow`, French-style *Sourp*, popular *Shooshi* |
   | `ew` → `ev`; `w` → `v` | ISO and Hübschmann-Meillet `և`, ALA-LC classical *Erewan*, ALA-LC `ւ` |
   | initial `yev` → `ev`, `ye` → `e`, `vo` → `o` | BGN/PCGN and Western glides |
   | initial `y` before a vowel → `h` | Western *Hagop* against *Yakob*; `Յովհաննէս` / `Հովհաննես` |
   | initial `ho` → `o` | Russian-mediated *Ovanes*, *Ovsep* (Russian has no *h*). Only before `o`: a general initial-*h* drop would merge `իւր` (his) with `ուր` (where), and it would change the keys of every *h*- name |
   | `dz` → `ts`; `ts`, `tz` → `c` | `ծ ձ ց` become one |
   | `j` → `ch` | `ջ ճ չ` become one (and the ISO `j` gap below) |
   | `gh` protected as `\x01`; `b`→`p`, `d`→`t`, `g`→`k`; restored | The Eastern/Western swap, without turning `gh` into `kh` |
   | `eo` → `evo` | *Gēorg* → *kevork* |
   | `ya`, `ea` → `ia`; `yo` → `io`; `yu`, `eu` → `iu` | *-yan*, *-ean*, *-ian*; *Harutiun* |
   | final `y` after a vowel dropped | The classical silent `յ` |
   | `FINISH`: non-alphanumerics removed, doubled letters collapsed | *Boghossian* |

   The `\x01` trick is the pattern to copy whenever a later rule would eat
   part of a digraph an earlier rule needs kept.

Sample keys: `Երևան`/*Yerevan*/*Erewan* → `erevan`; `Յակոբ`/*Hagop* →
`hakop`; `Պօղոսեան`/*Boghossian*/*Poghosyan* → `poghosian`;
`Հովհաննես`/*Hovannes*/*Ovanes* → `ovanes`; `Թումանյան`/*Thoumanian* →
`tumanian`; `Գէորգ`/*Kevork*
→ `kevork`; `Սուրբ`/*Sourp* → `surp`.

### Known gaps (declared in `test_does_not_claim_the_known_gaps` and `docs/fold.md`)

- **Popular spellings that insert an unwritten schwa**: *Megerdich* for
  `Մկրտիչ` (*Mkrtich* in every scheme).
- **Spellings that came through Russian**: *Khachaturian* has a *u* that
  `Խաչատրյան` does not. Initial *h* is restored only before `o`, so *Akop*
  and *Arutyunyan* still miss *Hakob* and *Harutyunyan*.
- **Classical `աւ` that reformed writes `օ`**: `աւր` and `օր` stay apart.
- **`j` with no scheme hint**: ALA-LC and BGN/PCGN `j` is `ջ`; ISO 9985 and
  Hübschmann-Meillet `j` is `ձ`. The heuristic reads it the library way.
  `fold("Jowkn", scheme="iso_9985")` reverses exactly first and gets it right.
- **BGN/PCGN `y` for `ը`** folds as the glide, not the schwa.

Before promising a user that two spellings fold together, run them: if the
pair is not in `tests/data/hy_fold_cases.tsv`, it is not claimed.

## Where the test data comes from

`tests/data/hy_fold_cases.tsv` holds about thirty groups: the cities
(Yerevan, Shushi), the saints and poets (Mesrop Mashtots, Charents, Sayat-Nova,
Komitas, Eghishe), the surnames in both orthographies and both pronunciations
(Poghosian, Vardanian, Avetikian, Khachatrian, Hovhannes, Hovsep, Tumanyan),
and the two
orthography pairs from Tetrak brief 014 (`Ազգ եւ հայրենիք` against `Ազգ և
հայրենիք`, `Աւետիքեան` against `Ավետիքյան`). Every form carries a note saying
which scheme or practice it is; keep that habit when adding.

## Do not confuse these with the fold

- **`tetrak_hy.fold_script`** (tetrak-easyocr-armenian) is a *homoglyph*
  fold on OCR output: it turns a Latin `h`, `o` or `:` that the recogniser
  emitted inside an Armenian word back into `հ`, `օ`, `։`. It makes text
  correct; this library's fold makes keys. The README's "generalises" means
  the idea of per-token script handling and the `եւ`/`և` equivalence, not the
  code.
- **`accuracy.normalise`** in Tetrak and the trainer equates `եւ` and `և`
  for scoring OCR engines. Same equivalence, different purpose.

## Traps

- **Lookalikes.** `Օ`/`O`, `Ո`/`П`, `ո`/`n`-ish shapes: OCR output and
  copy-pasted text can carry a Latin or Cyrillic letter inside an Armenian
  word. `detect()` will then say `mixed`, and the fold will split the token
  across scripts. Check `Detection.letters` when a result looks wrong.
- **The two apostrophes of ALA-LC and Hübschmann-Meillet** are different
  code points (`ʻ` U+02BB, `ʿ` U+02BF) and both differ from `'`. Any of them
  is accepted on input; only the scheme's own is produced.
- **`և` has no uppercase**; a word in capitals is `ԵՒ`, two letters, which the
  engine renders through the `ւ` letter rule, not the `և` digraph rule.
  `ԵՐԵՎԱՆ` is in the fold cases for this reason.
- **`ու` versus a free `ւ` after `ո`**: in reformed orthography the former is
  the only possibility; `_FREE_YIWN` uses a negative lookbehind for `ո` to tell
  them apart, so `Ուրարտու` has no free `ւ`.
