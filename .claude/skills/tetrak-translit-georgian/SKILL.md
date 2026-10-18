---
name: tetrak-translit-georgian
description: Georgian as tetrak-translit handles it — the 33-letter caseless Mkhedruli alphabet and its Unicode ranges, Mtavruli capitals, the five archaic letters, the Asomtavruli and Nuskhuri scripts the library deliberately does not handle, the aspirate/ejective consonant pairs and the apostrophe that ALA-LC and ISO 9984:1996 put on the aspirate but the national system and ISO 9984:2026 put on the ejective, the schemes letter by letter (ISO 9984 in both editions, and the 2026 edition's middle dot), the fold's rules and known gaps, and why Georgian must never merge b with p. Load this whenever Georgian text, a Georgian name or place, a Georgian scheme key (ala_lc for Georgian, iso_9984, national), the ka/ package or ka_fold_cases.tsv comes up — including "how is Tbilisi written in ALA-LC", "why does Kazbegi fold to ყაზბეგი", or any question about the apostrophe in a Georgian romanisation.
---

# Georgian

The simpler of the two scripts, and the one to copy when adding a third: one
orthography, no case, no pronunciation tradition that swaps consonants. What
varies between spellings is almost entirely how the aspirate/ejective
distinction is marked, and the three systems disagree about it in a way that
confuses everyone. The tables in `src/tetrak_translit/ka/` are the authority on
individual letters.

## The script

- **Mkhedruli**, the modern script: **33 letters**, `ა`–`ჰ`, U+10D0–U+10F0,
  **no case**. A Georgian rendering is lowercase and a catalogue capitalises
  proper names by its own convention; the library does not guess.
- **Mtavruli** (U+1C90–U+1CBF, added in Unicode 11, 2018) are the capital
  forms used for emphasis and all-capitals headings. Python lowercases them to
  Mkhedruli, and the engine renders them as capitals (`ᲗᲑᲘᲚᲘᲡᲘ` → *TBILISI*).
  `Script.ranges` covers both blocks: `(0x10D0, 0x10FF), (0x1C90, 0x1CBF)`.
- **Five archaic letters** `ჱ ჲ ჳ ჴ ჵ` (he, hie, vie, qar, hoe) appear in older
  texts. ALA-LC and ISO 9984 define them (`ē y w ẖ ō`); the national system
  does not, and passes them through unchanged. The fold maps them onto the
  modern letters that replaced them (`ე ი ვ ხ ო`), so `ჴელი` and `ხელი` are
  one key.
- **Other letters in the block** (`ჶ ჷ ჸ ჹ ჺ`, for Mingrelian, Svan, Abkhaz
  and Ossetian) are inside the ranges but not in the alphabet or the tables,
  so they pass through a rendering unchanged (`ჶა` → `ჶa`).
- **Asomtavruli** (U+10A0–U+10C5) and **Nuskhuri** (U+2D00–U+2D25), the
  ecclesiastical scripts, are outside the ranges and **not handled**:
  `detect()` names them `georgian` (their Unicode names begin with GEORGIAN)
  but gives no `key`, and the engine passes them through. Python's `.lower()`
  maps Asomtavruli to Nuskhuri, not to Mkhedruli, so lowercasing does not
  rescue them. Khutsuri-era material needs a conversion step before this
  library sees it.

`variant()` returns `None`: Georgian has one orthography, so a `Detection` for
Georgian text has `orthography=None`.

## The consonants that drive everything

Georgian has pairs of **aspirated** and **ejective** stops and affricates:

| Aspirated | Ejective | Voiced |
|---|---|---|
| `თ` t | `ტ` t' | `დ` d |
| `ფ` p | `პ` p' | `ბ` b |
| `ქ` k | `კ` k' | `გ` g |
| `ჩ` ch | `ჭ` ch' | `ჯ` j |
| `ც` ts | `წ` ts' | `ძ` dz |
| | `ყ` q' (uvular, no aspirated partner) | |

(The marks in that table follow the national system.) The voiced series
never swaps with either of the others — unlike Armenian — which is why the
Georgian fold keeps `b`, `d`, `g` apart from `p`, `t`, `k` and why
`fold("Batumi", script="hy")` would give `patumi` and never find `ბათუმი`.

### The apostrophe runs the opposite way

**ALA-LC and ISO 9984:1996 mark the aspirate** (`tʻbilisi`, `kʻutʻaisi`,
`t'bilisi`) and leave the ejective plain. **The national system marks the
ejective** (`ts'ereteli`, `ch'avch'avadze`, `q'azbegi`) and leaves the
aspirate plain (*Tbilisi*, *Kutaisi*). **ISO 9984:2026 changed sides**: it is
built on the national system, so the plain key `iso_9984` now puts the
apostrophe on the ejective, and `t'` means `თ` under `iso_9984_1996` but `ტ`
under `iso_9984`. The same apostrophe on the same word
therefore means opposite letters in the two traditions:

| Georgian | ALA-LC | ISO 9984:1996 | National and ISO 9984:2026 |
|---|---|---|---|
| თბილისი | tʻbilisi | t'bilisi | tbilisi |
| წერეთელი | tseretʻeli | ceret'eli | ts'ereteli |
| ჭავჭავაძე | chavchavadze | čavčavaje | ch'avch'avadze |

The library-and-ISO convention comes from the older scholarly habit of
marking the aspirate with a spiritus; the national system was written for
English readers, for whom a plain *t* is already aspirated, so it marks the
sound they do not have. When a user reports that "the apostrophe is on the
wrong letter", it is almost always this. The fold's answer is to strip the
mark and merge each pair, so neither tradition has to be guessed.

## The schemes

| Id | Standard | Met in | Apostrophe on | Reversible |
|---|---|---|---|---|
| `ka/ala_lc` | ALA-LC Romanization Tables, Georgian (2011) | Library catalogues; the default | aspirate, `ʻ` U+02BB | no |
| `ka/iso_9984` | ISO 9984:2026 | Data exchange | ejective, `'` | yes |
| `ka/iso_9984_1996` | ISO 9984:1996, superseded | Data made under the first edition | aspirate, `'` | yes |
| `ka/national` | Georgian national system (2002), adopted by BGN/PCGN 2009 | Road signs, passports, maps | ejective, `'` | no |

Where they differ (letters not listed render the same everywhere):

| | `ala_lc` | `iso_9984_1996` | `national` | `iso_9984` (2026) |
|---|---|---|---|---|
| `თ` `ფ` `ქ` | tʻ pʻ kʻ | t' p' k' | t p k | t p k |
| `ტ` `პ` `კ` | t p k | t p k | t' p' k' | t' p' k' |
| `ჩ` / `ჭ` | chʻ / ch | č' / č | ch / ch' | ch / ch' |
| `ც` / `წ` | tsʻ / ts | c' / c | ts / ts' | ts / ts' |
| `ყ` | q | q | q' | q' |
| `ჟ` | zh | ž | zh | zh |
| `შ` | sh | š | sh | sh |
| `ღ` | gh | ḡ | gh | gh |
| `ხ` | kh | x | kh | kh |
| `ძ` | dz | j | dz | dz |
| `ჯ` | j | ǰ | j | j |
| `ჱ ჲ ჳ ჴ ჵ` | ē y w ẖ ō | ē y w ẖ ō | not defined; pass through | ē y w ẖ ō |
| `ჶ` | — | f | — | f |
| `ჷ ჸ ჹ ჺ ჼ ჽ ჾ ჿ` | — | — | — | ȳ ʔ ĝ ʕ ⁿ æ ʸ ʷ |
| between `გზსქ` and `ჰ`, `თ` and `ს`, `დ` and `ზ` | nothing | nothing | nothing | `·` (U+00B7) |

The same name four ways (`iso_9984`, the 2026 edition, is the national
spelling for all of these):

| Georgian | `ala_lc` | `iso_9984_1996` | `national` and `iso_9984` |
|---|---|---|---|
| ქუთაისი | kʻutʻaisi | k'ut'aisi | kutaisi |
| მცხეთა | mtsʻkhetʻa | mc'xet'a | mtskheta |
| ყაზბეგი | qazbegi | qazbegi | q'azbegi |
| ჯავახიშვილი | javakhishvili | ǰavaxišvili | javakhishvili |

Per scheme:

- **ALA-LC** is lossy because `dz`, `zh`, `gh`, `sh` and `kh` can each be one
  letter or two (`ძ` or `დ`+`ზ`, and so on).
- **ISO 9984** (`iso_9984`, the 2026 edition) is the national system made
  reversible: a middle dot separates the letter pairs the standard lists
  (`z·h` is `ზჰ`, not `ჟ`), and `read()` skips it. The list misses two
  sequences, `dzh` (`ძჰ` or `დჟ`) and `tsh` (`ცჰ` or `თშ`); reading back
  takes the first, and a test pins that. Its Table 4 example for every
  letter is a test in `tests/test_transliterate.py`. Choose it for
  round-tripping, but see the defect below: it is reversible except for
  those two sequences.

### The defect in ISO 9984:2026

The standard claims full reversibility, and **it is not reversible as
published**. Its middle-dot list (4.2) leaves out `დ` before `ჟ` and `თ`
before `შ`, so `dzh` and `tsh` each read back two ways:

| Latin | Reading 1 | Reading 2 |
|---|---|---|
| `dzh` | `ძ` + `ჰ` | `დ` + `ჟ` |
| `tsh` | `ც` + `ჰ` | `თ` + `შ` |

Neither pair in reading 1 is listed, so `ძჰ` and `ცჰ` get no dot. Reading
2 is `d` + `zh` and `t` + `sh`, which are not listed either.

This was found with an exhaustive check of every two- and three-letter
Georgian sequence: render it, read it back, compare. Those are the only two
collisions. **Adding the pairs `დჟ` and `თშ` to the list fixes both**, and
with them the check comes back clean. Stephen reported this to BSI on
2026-10-12.

What the library does about it:

- **It follows the standard as published.** `separate` in
  `ka/iso_9984.py` holds only the standard's pairs. Don't add `დჟ` and `თშ`
  on our own initiative: output would then differ from what a conforming
  implementation writes.
- **Reading back takes the first reading** (`ძჰ`, `ცჰ`), and
  `test_sequences_the_standards_list_leaves_ambiguous` pins that, so a
  change in behaviour can't slip through unnoticed.
- `reversible=True` stays, because that is what the standard claims. The
  module docstring and `docs/schemes.md` name the two exceptions.
- **When an amendment or corrigendum is published**, add the pairs it
  gives to `separate`, and bump the scheme `version`. Change the pinned
  test to round-trip `დჟ` and `თშ`, then update this section, the
  docstring and `docs/schemes.md`. Rendering `დჟ` and `თშ` changes (a dot
  appears), so the commit is `feat(ka)!` with a `BREAKING CHANGE`
  footer. `fold()` is not affected, because it never sees the dot.
- **ISO 9984:1996** (`iso_9984_1996`) is one letter per letter with háčeks:
  `j` is `ძ` and `ǰ` is `ჯ`; `c` is `წ` and `c'` is `ც`; `x` is `ხ`. Kept for
  data made under it.
- **The national system** is what Georgia itself uses: no diacritics,
  apostrophe on the ejective. It is the spelling on signs and in passports
  and the one English prose has settled on (*Tbilisi*, *Kutaisi*, *Batumi*).
  Lossy for the same digraph reasons as ALA-LC.

## The fold (`ka/fold.py`)

1. **Georgian input** is lowercased, its archaic letters translated onto the
   modern ones and `ჶ` onto the `f` ISO 9984 writes for it, and rendered
   through **ALA-LC** -- the 2011 table frozen in the module as `_BASIS`, as
   the Armenian fold does, so that a new edition of `ka/ala_lc` never moves a
   key.
2. **`clean()`**: the `_LETTERS` map (`ž`→`zh`, `š`→`sh`, `č`→`ch`, `ǰ`→`j`,
   `ḡ`→`gh`, `ẖ`→`kh`, `x`→`kh`) runs before NFKD strips the remaining
   diacritics, and every apostrophe-like mark is removed — which is the step
   that merges each aspirate with its ejective whichever system marked which.
3. **The `_LATIN` rules**: `ch` is protected as `\x01` while `dz` → `j` and
   `ts` → `c`, then restored; `q` → `k` (so *Kazbegi*, the common English form,
   finds `ყაზბეგი`); `y` → `i`; `w` → `v`; then `FINISH` (ASCII letters and
   digits only, doubled letters collapsed).

Consequences worth knowing: the fold merges `ძ` with `ჯ` (both reach `j`) and
`ც` with `წ` (both reach `c`), as well as each aspirate with its ejective.
That is coarser than a Georgian speaker would like and exactly as coarse as
cross-system matching needs. Sample keys: `თბილისი`/*Tʻbilisi*/*T'bilisi*
→ `tbilisi`; `ჭავჭავაძე`/*Čavčavaje*/*Ch'avch'avadze* → `chavchavaje`;
`მცხეთა` → `mckheta`.

### Known gaps (declared in `test_does_not_claim_the_known_gaps` and `docs/fold.md`)

- **Russian-mediated forms**: *Tiflis* for `თბილისი`, *Kutais* for `ქუთაისი`.
- **Translated names**: *George* for `გიორგი`.
- **ISO 9984:2026's phonetic letters beyond `ჶ`** (`ჷ` to `ჿ`) fold to nothing
  on the script side; outside the claim.

## The test data

`tests/data/ka_fold_cases.tsv` holds eighteen groups: the cities (Tbilisi
with its Mtavruli and all-capitals forms, Kutaisi, Batumi, Mtskheta), the
writers and politicians (Rustaveli, Chavchavadze, Tsereteli, Javakhishvili,
Zhordania, Gamsakhurdia), the words that exercise one letter each (`ღვინო`
for `ღ`, `ძველი` for `ძ`, `ქართული` for the aspirates), Qazbegi with its
English *Kazbegi*, and an archaic/modern pair. Each form is noted with the
scheme it belongs to.

## Traps

- **The apostrophe direction**, above. Check which system a Latin form came
  from before deciding a table is wrong.
- **"Fixing" ISO 9984:2026's dot list**: `dzh` and `tsh` reading back as
  `ძჰ` and `ცჰ` is the standard's defect, not ours. Leave `separate` alone
  until an amendment is published (see the defect section above).
- **ISO `x` and `j`**: `x` is `ხ` (not a *ks*), `j` is `ძ` (not `ჯ`). Both are
  mapped in `_LETTERS` so the fold is unaffected, but a reader will trip.
- **Case**: `transliterate("თბილისი", "national")` is `tbilisi`, lowercase, and
  that is correct; only a Mtavruli source renders in capitals. Reading Latin
  back drops capitals because the script has none (`T'BILISI` → `თბილისი`).
- **Asomtavruli and Nuskhuri** are detected but not rendered or folded, and
  lowercasing moves between them rather than to Mkhedruli.
- **`fold("Tbilisi")` with no `script=` raises**, like any Latin input. Pass
  `script="ka"`. There is no default and there must not be one.
