---
name: tetrak-translit-romanisation
description: Background knowledge for any work on tetrak-translit that touches romanisation — what transliteration is and is not, the families of standards (library ALA-LC, international ISO, geographic BGN/PCGN and national systems, scholarly transcriptions) and who uses which, reversible against lossy tables and why the library refuses to guess, the display-against-finding split behind transliterate() and fold(), the Unicode mechanics every table and fold rule depends on (the apostrophe and modifier-letter family, combining marks, NFC/NFKD, case, detection by character name) and how Script and Scheme model all of it. Load this before answering any question about romanisation or a scheme, reviewing or writing a table, choosing a scheme for a catalogue or an index, designing or debugging a fold, or explaining the library to a user — even when the question seems to be about one letter. Load the per-script skill (tetrak-translit-armenian, tetrak-translit-georgian) alongside it for the letters themselves.
---

# Romanisation, as tetrak-translit understands it

The library does three jobs — detect, transliterate, fold — and the mistakes
people make with it are nearly all conceptual rather than technical: treating
a romanisation as a translation, expecting a lossy table to reverse, or
showing a fold key to a reader. This skill is the background that prevents
those mistakes. The letters of each script are in the per-script skills; the
workflows for changing anything are in `tetrak-translit-extending`.

## Three words that are not interchangeable

- **Transliteration** maps letters to letters. The same word, a different
  alphabet. Done strictly it is reversible: ISO 9985 and ISO 9984 are built so
  that every Latin rendering goes back to exactly one letter.
- **Transcription** maps sounds to letters. BGN/PCGN, the Georgian national
  system and the Western Armenian pronunciation spelling lean this way: *Yerevan*
  with its initial *ye* is how the word sounds, not a letter-for-letter
  rendering of `Երևան`. Transcriptions read well and reverse badly.
- **Translation** changes the words. Out of scope entirely, and the commonest
  misunderstanding in conversation: *George* is a translation of `გიორგი`, not
  a romanisation, and the library is right not to fold it.

Library people say *romanization*; linguists say *transliteration* or
*transcription*; the docs here say *romanisation* (British spelling) for the
general act and *scheme* for one table. Keep to that.

## The families of schemes, and who uses which

| Family | Here | Designed for | Marks | Reversible |
|---|---|---|---|---|
| Library | `hy/ala_lc`, `ka/ala_lc` | Catalogue records, authority headings, WorldCat | `ʻ` U+02BB, a few macrons and dots | no |
| International | `hy/iso_9985` (and `hy/iso_9985_1996`), `ka/iso_9984` | Data exchange: one letter per letter | Diacritics, plain apostrophe | yes |
| Geographic | `hy/bgn_pcgn`, `ka/national` | Maps, signs, passports, English readers | Apostrophe, no diacritics | no |
| Scholarly | `hy/hubschmann_meillet` | Linguistics, critical editions, the *Revue des Études Arméniennes* | Háčeks, `ʿ` U+02BF | yes |
| Practice | `hy/western` | How diaspora names were actually spelled | None | no |

Choosing one for a user:

- A library catalogue, a MARC record, a WorldCat or Library of Congress
  heading: **ALA-LC**, which is why it is the library's default scheme.
- A place name on a map or in English prose, a passport, a road sign:
  **BGN/PCGN** for Armenian, the **national system** for Georgian.
- Storing a Latin form that must round-trip, or exchanging data between
  systems: an **ISO** scheme. Nobody reads *Sowrb* for pleasure.
- A linguistics paper, a critical edition, Armenian studies:
  **Hübschmann-Meillet**.
- A diaspora surname as its bearer writes it: **Western**, with the warning
  that it is a practice and not a standard, so real spellings vary around it.

The same name therefore has several correct romanisations, and the
library's position is that none of them is *the* right one. A catalogue that
holds *Erevan* is not wrong because an atlas holds *Yerevan*.

## Reversible and lossy

A table reverses when every rendering is distinct and the inverse can be read
off longest-match-first without ambiguity. Three things break that:

- **Digraph collisions.** ALA-LC Armenian renders `ծ` as `ts`, but `տ`+`ս` is
  also `ts`; `ձ` and `դ`+`զ` are both `dz`; `խ` and `կ`+`հ` are both `kh`.
  Georgian ALA-LC has the same problem with `dz`, `zh`, `gh`, `sh`, `kh`.
- **Positional rules.** BGN/PCGN writes `ե` as `ye` at the start of a word and
  `e` elsewhere; reading `e` back cannot know which letter it was.
- **Merged letters.** The Western spelling writes `p` for both `բ` and `փ`.

The `reversible` flag on a `Scheme` is a **tested claim**:
`test_reversible_schemes_are_one_to_one` checks that every rendering is
distinct, and `TestToScript` round-trips the whole alphabet and a set of
words. Setting the flag on a table that fails those is caught, but setting
it on a table that passes them while having a positional rule is not, so
think before claiming it.

Where a scheme is lossy the library **refuses to reverse** rather than
guess, and the error message points at `fold()`. That is a design decision,
not a limitation to work around: a wrong guess written into a catalogue
field is silent corruption, while a refusal is a visible one. The reversible
schemes exist precisely so that there is a lossless path when one is needed.

Reading Latin back normalises every apostrophe-like character to the
scheme's own mark first (`engine.APOSTROPHES`), because people type `'` or
`’` for `ʻ` and the library should not punish them for it.

## Display and finding

This is the idea the whole package is built around. **Schemes are for
display**: a rendering a reader sees in a catalogue, a caption, a citation.
**The fold is for finding**: a key that says which spellings are the same
word, so that an index built from one spelling is found by a query typed in
another.

Cross-script name matching has no gold standard to score against — the LREC
2020 survey of 445 languages and 37 scripts concluded that intrinsic
evaluation of transliteration is often inappropriate for exactly that reason
— so the fold does not pretend to produce a *correct* spelling. It produces a
deliberately coarse ASCII skeleton (`poghosian`, `erevan`, `chavchavaje`)
that nobody should ever read. Properties a fold must have:

- **Coarse on purpose.** It merges what readers would want kept apart, because
  the point is that *Hagop* and *Yakob* land in the same place.
- **Lowercase ASCII**, so a plain whitespace tokeniser indexes it.
- **Idempotent**: folding a key gives the key.
- **Token-wise**: a title folds to a sequence of keys, joined by single spaces.
- **Never displayed.** Index the folded field; show the original.

Design principles when writing or changing one:

- **Merge what spellings confuse; keep apart what the script keeps apart.**
  Armenian merges *b* with *p* because Eastern and Western spellings swap them.
  Georgian must not, because `ბ` and `პ` are different letters that never swap,
  and *Batumi* folded under Armenian rules would never find `ბათუმი`. This is
  why each script owns its fold and why Latin input must name its script.
- **The two sides meet at ALA-LC.** Script input is pre-normalised (Armenian
  across the 1922 reform, Georgian archaic letters onto modern ones) and then
  rendered through ALA-LC, so that the script and its catalogue romanisation
  reach the Latin rules by the same road and one rule set serves every
  scheme. `TestAllSchemesFoldToTheirScript` checks that every scheme's output
  folds like its source.
- **The case set is the claim.** `tests/data/<script>_fold_cases.tsv` lists
  groups that must fold together; a second test checks that different groups
  stay different. The second test is the one that catches over-merging, which
  is the fold's natural failure mode.
- **A gap you cannot close is declared, not forced.** It becomes a test
  asserting the inequality and an entry in `docs/fold.md`.

Where the fold is used: at **index time and query time with the same
function**, typically a `*_fold` copy of each title and name field plus a
query parser that folds the user's input. In Solr or Elasticsearch terms it is
a token filter, not a char filter, because it works token by token. An index
holding both Armenian and Georgian material folds a Latin query under each
script and searches for either key.

## Unicode mechanics everything depends on

### The apostrophe family

| Character | Code point | Category | Used for |
|---|---|---|---|
| `'` | U+0027 | Po | ISO 9985, ISO 9984, BGN/PCGN aspiration; the national system's ejective; what users type |
| `’` | U+2019 | Pf | What word processors turn `'` into |
| `ʻ` | U+02BB modifier letter turned comma | Lm | ALA-LC aspiration, Armenian and Georgian; the character catalogue records carry |
| `ʿ` | U+02BF modifier letter left half ring | Lm | Hübschmann-Meillet aspiration |
| `ʼ` | U+02BC modifier letter apostrophe | Lm | Seen in the wild for any of the above |

Two consequences in the code. `detect()` excludes category **Lm**: modifier
letters are `isalpha()` and their Unicode names begin with "MODIFIER", so
without the exclusion `Chʻarentsʻ` would count as mixed Latin and "modifier"
script. And `latin.clean()` strips every member of `engine.APOSTROPHES`, which
is what makes the Georgian fold merge each aspirate with its ejective
regardless of which system put the mark where.

### Combining marks and normalisation

- The engine normalises input to **NFC** for rendering. Some renderings have
  no precomposed form: ISO 9985:1996 writes `ճ` as `č̣`, which is `č` plus
  U+0323 combining dot below, two code points even in NFC; and the capital of
  `ǰ` is `J̌`, J plus U+030C combining caron, because Unicode has no
  precomposed capital. `read()` therefore works in **NFD**: it decomposes
  both the table and the input, matches longest-first, refuses a match that
  would end in the middle of a character (a following combining mark), and
  returns NFC. Tables can be written in either form.
- `latin.clean()` applies the script's `_LETTERS` map **before** NFKD
  decomposition strips the combining marks. The order matters: `ž` must
  become `zh` before the háček is removed, or it becomes `z`. Any new
  diacritic-bearing letter a scheme introduces needs a `_LETTERS` entry in
  that script's fold, or it folds to the bare letter and the scheme's output
  stops folding like its source.
- NFKC is **not** applied, so compatibility characters survive. Armenian has
  five presentation-form ligatures at U+FB13–U+FB17 (`ﬓ ﬔ ﬕ ﬖ ﬗ`, for `մն
  մե մի վն մխ`): their Unicode names begin with "ARMENIAN", so `detect()`
  reports Armenian, but they lie outside `Script.ranges` and pass through
  `transliterate()` unrendered (`ﬔր` renders as `ﬔr`). Known gap, found
  2026-10-10, not yet addressed; a fix would NFKC-normalise or add the range.
- **Case** is handled per character. A cased script capitalises a rendering
  when its source letter was a capital, and a whole word in capitals renders
  in capitals. A caseless script (Georgian Mkhedruli) ignores Latin capitals
  when reading back. Python lowercases Georgian Mtavruli to Mkhedruli (good)
  and Asomtavruli to **Nuskhuri**, not Mkhedruli (a trap: neither is in the
  Georgian ranges, so both pass through unrendered).

### Detection by character name, membership by range

Two mechanisms, and both must agree for a script to work. `detect()` reads
the first word of each letter's Unicode name (`unicodedata.name(c)`) and so
can name *any* script — Cyrillic, Greek, Hebrew — without a table. Only a
registered script then gets a `key` and a `variant`, and registration is by
`Script.ranges`, which `Script.is_letter()` checks. A letter whose name says
"ARMENIAN" but whose code point is outside the ranges is detected and not
rendered; that is the ligature gap above. `test_script_ranges_do_not_overlap`
guards the other direction.

`mixed` means letters from more than one script; `dominant` is the one with
the most letters; `key` is set only when exactly one registered script is
present. Digits, punctuation and modifier letters are ignored throughout.

## How the library models it

Two frozen dataclasses in `script.py` carry all the data, and `engine.py` is
the only code that reads them:

- **`Script`**: `key` (`hy`), `name`, `unicode_name` (the detection word),
  `letters` (the lowercase alphabet, every one of which every scheme must
  render), `archaic`, `digraphs` (units every scheme must render whole),
  `vowels` (for after-vowel rules), `ranges`, `cased`.
- **`Scheme`**: `script`, `key`, `name`, `version` (the table's own, bumped on
  any mapping change), `standard` (what it was written from), `reversible`,
  `letters`, `digraphs`, `initial`, `after_vowel`, `notes`. The constructor
  refuses a table that misses a letter, renders a letter outside the script,
  omits a required digraph, or puts a positional rule on an undefined unit.

`engine.render()` walks each word longest-unit-first (so a two-letter digraph
is taken whole), applies `initial` at position 0 and `after_vowel` after a
vowel, carries case across, and passes everything outside the script through
untouched, so a whole catalogue line can go in. `engine.read()` inverts a
reversible table longest-Latin-first after normalising apostrophes.
`fold()` dispatches each whitespace token to the fold of the script whose
letters it contains, or to the script named by `script=`, and raises
`ScriptRequiredError` for Latin with no script — a default would silently
apply the wrong rules, so there is none and there must never be one.

`registry.get_scheme()` resolves a key in this order: a qualified id
(`ka/ala_lc`), then `script=`, then the one registered script whose letters
occur in the text, then the one script that has a scheme of that key
(`national`, `western`); a key several scripts define with nothing to choose
between them raises an error that names the choices rather than guessing.

## Where the standards are, and the rule about copying

Every table names the standard it was written from, and a change cites it:

- **ALA-LC Romanization Tables** — Library of Congress, published free per
  language at loc.gov (Armenian and Georgian both approved 2011).
- **ISO 9985:2026** (Armenian, second edition; replaced ISO 9985:1996, which
  `hy/iso_9985_1996` keeps) and **ISO 9984:1996** (Georgian; replaced by
  ISO 9984:2026, which the table has not yet been checked against) — ISO,
  paid. ISO sells them directly for less than national bodies do.
- **BGN/PCGN** — the US Board on Geographic Names and the UK Permanent
  Committee on Geographical Names publish the agreed systems free (Armenian
  1981; the Georgian national system of 2002 as adopted in 2009).
- **Hübschmann-Meillet** — Hübschmann's *Armenische Grammatik* (1897), Meillet's
  *Altarmenisches Elementarbuch* (1913), as the *Revue des Études Arméniennes*
  applies it.

Romanisation tables are facts, but a copied file is still a copied file:
**never copy a table from another implementation**, whatever its licence,
and take nothing from a non-commercially-licensed source. Write from the
standard, name it in `standard=`, bump the scheme's `version` when a mapping
changes (Tetrak brief 015).

## Talking to the people who use this

The audience is catalogue developers, search engineers and Armenian or
Georgian studies tooling, most of whom will never hear of Tetrak. Terms they
use and what they map to here:

- *Romanization*, *transliteration table*: a `Scheme`.
- *MARC 880 / linked alternate graphic representation*: the record holds the
  script and the romanisation side by side; both are display forms, and
  neither is the fold.
- *Authority heading*: the one spelling the catalogue standardises on, almost
  always ALA-LC. The fold does not replace authority control; it finds
  records that authority control never reached.
- *Analysis chain*, *token filter*, *index-time and query-time*: where `fold()`
  goes, called identically on both sides.
- *No runtime dependencies*: a feature, because the package runs inside their
  search sidecars and catalogue scripts and must drag nothing in.
