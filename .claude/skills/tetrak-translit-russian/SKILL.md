---
name: tetrak-translit-russian
description: Russian as tetrak-translit handles it — the 33-letter Cyrillic alphabet and the Unicode ranges the ru package claims, the 1918 reform and the four letters it removed (і ѣ ѳ ѵ) with the final hard sign, the pre-reform/reformed/indeterminate tells detect() uses, why other Cyrillic languages are detected as ru and what that costs, ALA-LC 2012 letter by letter (the U+0361 tie, the prime signs, capitals in a tie, the final hard sign kept since 2012) and BGN/PCGN 1947 (ye after vowels and signs, the middle dot), ISO 9 and why it is not a table yet, the fold's rules in order and its known gaps. Load this whenever Russian or other Cyrillic text, a Russian name or place, a Russian scheme key (ala_lc or bgn_pcgn for Russian), the ru/ package or ru_fold_cases.tsv comes up — including "how is Tchaikovsky written in ALA-LC", "why does Michail not fold to Михаил", "is this pre-reform", or anything about -sky/-skii/-skij surnames.
---

# Russian

The third script, and the first with case and a two-orthography history that
changed letters rather than their distribution. Russian names reach a catalogue
in more Latin spellings than Armenian or Georgian ones: library, map,
scholarly, ISO, English, German and French. The tables in
`src/tetrak_translit/ru/` are the authority on individual letters.

## The script

- **33 letters**, `а`–`я` with `ё`, U+0430–U+044F and U+0451, upper case
  U+0410–U+042F and U+0401. Cased: the engine carries capitals across.
- **`Script.ranges`** is the whole Cyrillic block and the Cyrillic Supplement,
  `(0x0400, 0x0481), (0x048A, 0x052F)`, less the thousands sign and the Church
  Slavonic combining marks U+0482–U+0489. `unicode_name` is `cyrillic`, so
  `get_script("cyrillic")` finds `ru`.
- **Other Cyrillic languages are detected as `ru`.** They share the letters, and
  no registered script can claim them separately while the ranges must not
  overlap (`test_script_ranges_do_not_overlap`). Their own letters (Ukrainian
  `є ї ґ`, Serbian `ђ љ њ`) are in range but not in any table, so they pass
  through a rendering unchanged; the fold strips their diacritics and keeps
  going. A second Cyrillic language as its own package would need the engine
  to let two scripts share ranges: a change to the engine first, in its own
  pull request.
- **Church Slavonic** letters and marks are outside the claim. ALA-LC has a
  separate Church Slavic table for them.

## The 1918 reform

Decreed in 1917 and enforced from 1918, it removed four letters and one habit:

| Removed | Replaced by | ALA-LC 2012 |
|---|---|---|
| `і` (decimal i) | `и` | *ī* |
| `ѣ` (yat) | `е` | *i͡e* |
| `ѳ` (fita) | `ф` | *ḟ* |
| `ѵ` (izhitsa) | `и` | *ẏ* |
| `ъ` closing a word after a hard consonant | nothing | *ʺ* |

They are `Script.archaic`. It also changed spellings without changing letters
— `-аго`/`-яго` to `-ого`/`-его`, `-ыя`/`-ія` to `-ые`/`-ие`, `без-` to `бес-`
before a voiceless consonant — and the fold does not take those (a declared
gap). Émigré presses kept the old spelling for decades, so pre-reform is not
the same as pre-revolutionary.

`variant()` is `ru.orthography.orthography`:

- **`pre-reform`** on any of the four letters, or `ъ` closing a word.
- **`reformed`** on a word of three or more letters ending in a lowercase hard
  consonant with no `ъ`, not followed by a full stop (`Пушкин`). The
  exclusions are for abbreviations (`г.`, `стр.`), short words and acronyms in
  capitals (`СССР`), which ended bare under both spellings.
- **`indeterminate`** otherwise: `Москва`, `Толстой`, `Гоголь`.

A pre-reform tell wins over a reformed one in the same string, as Armenian's
classical tells do.

## The schemes

| Id | Standard | Reversible |
|---|---|---|
| `ru/ala_lc` | ALA-LC Romanization Tables, Russian, **2012 version** | no |
| `ru/bgn_pcgn` | BGN/PCGN 1947 System, the June 2019 printing | no |

Both keys exist for Armenian too, so a bare `ala_lc` or `bgn_pcgn` is ambiguous
unless the text is Cyrillic or `script="ru"` is given. Adding `ru/bgn_pcgn`
made the bare `bgn_pcgn` ambiguous for Latin-only input, as `ka/ala_lc` did
for `ala_lc`.

### ALA-LC 2012

Source: <https://www.loc.gov/catdir/cpso/romanization/russian.pdf>. Earlier
versions 2011 and 1997 are linked from it.

- **The tie** over `ц` *t͡s*, `ю` *i͡u*, `я` *i͡a* and `ѣ` *i͡e* is the combining
  double inverted breve **U+0361**, between the two letters. That is the MARC
  mapping since MARBI proposal 2004-08; records older than that carry the
  halves **U+FE20** (after the first letter) and **U+FE21** (after the second).
  Both are combining marks, so the fold strips either.
- **Capitals in a tie**: both letters, as the table's upper-case column gives
  them — *T͡Svetaeva*, *I͡Uriĭ*. The table does this with `Rule(..., capital=True)`
  because the engine's default capitalises only the first character.
- **Signs**: soft `ь` is the modifier prime `ʹ` (U+02B9), hard `ъ` the double
  prime `ʺ` (U+02BA). Neither is in `engine.APOSTROPHES`; the fold's `FINISH`
  strips them as non-alphanumerics.
- **The final hard sign** is romanised since 2012. The 2011 table's Note 2
  ("disregarded in romanization when found at the end of a word") was removed
  in the 2012 revision, so records made before 2012 write *vi͡estnik* where
  the current table writes *vi͡estnikʺ*. The fold takes both.
- `й` *ĭ*, `э` *ė*, `ё` *ë*, `ы` *y*.
- Lossy: without the tie *ts* is `ц` or `тс`; *shch* is `щ` or `шч`.

### BGN/PCGN 1947

Source: *Romanization of Russian*, the BGN/PCGN 1947 System, NGA GEOnet
Names Server documents, "checked for validity and accuracy – June 2019".

- `е` is *ye* initially, after a vowel and after `й`, `ъ`, `ь` (Note 1); `ё`
  likewise *yë* (Note 2). The engine's `initial` and `after_vowel` maps cover
  the first two; the three signs are rendered as digraphs (`ье` → *’ye*,
  `йе` → *yye*), since the engine's positional rules look only at vowels.
- Signs: `ь` *’* (U+2019, Note 5), `ъ` *”* (U+201D).
- **Note 3's middle dot** is applied through `separator`/`separate`: `тс`
  *t·s*, `шч` *sh·ch*, `й` or `ы` before `а у ы э` (*y·a*), a vowel before `ы`
  (*·y*), and a consonant other than `й` before `э` (*m·er*). The note says
  "may"; we apply it because it is the table's only way to keep those
  sequences distinct.
- No pre-1918 letters: they pass through unrendered (`вѣра` → *vѣra*). The
  fold still takes such a rendering back, because a token with a Cyrillic
  letter in it is rendered through the fold's basis whole.

### ISO 9, and why it is not a table yet

ISO 9:1995 (with Amendment 1:2024) is the current edition; a third edition
(ISO/DIS 9) was approved for registration as a final draft in July 2026 and
had not been published at 27 October 2026. Its tables cover modern Slavic
languages, older Slavic orthographies and non-Slavic languages. We do not have
the text, and a table must be written from the standard itself, not from GOST
7.79 System A (which reproduces it) or from Wikipedia. When the text is bought
(from BSI in the UK), write `ru/iso_9` from the current edition and keep the
other as `ru/iso_9_1995` if both are needed, as for ISO 9985 and ISO 9984.
ISO 9 is one-to-one, so it will be the first reversible Russian scheme. The
fold already takes its spellings: `â` *ia*, `û` *iu*, `ŝ` *shch*, `c` *ts*,
`h` *kh*.

## The fold (`ru/fold.py`)

Cyrillic is rendered through `_BASIS`, a frozen copy of the ALA-LC 2012 table
**including the pre-reform letters**, so `ѣ` and `е` both reach *e* without a
separate orthography step. Then `clean()` with `_LETTERS` (`·` gone; `ž š č ŝ`
to digraphs; `â û` to *ia iu*), NFKD, and `_LATIN` in this order:

1. `schtsch`/`shtch` → *shch*; `tsch` → *ch*; `sch` → *sh*; `tch` → *ch*; `ou` → *u*.
2. `x` → *ks*; `w` → *v*; `j`, `y` → *i*.
3. `tz` → *ts*; `c` not before `h` → *ts*.
4. `h` not after `z k c s` → *kh*.
5. `i+e` → *e* (the glide ALA-LC never writes: *Yevgeniy*, *Vasilyev*).
6. `i+o` after a consonant → *e* (ALA-LC's *ë*: *Fyodor*, *Semyon*).
7. Closing `ff` → *v*. Then `FINISH`.

Order matters: *tsch* goes before *sch*, or *Tschaikowski* would become
*tshaikovski*; `j`/`y` → *i* goes before rule 5, so German *Jewgeni* and
BGN/PCGN *Yevgeniy* reach it.

### Known gaps (declared in `test_does_not_claim_the_known_gaps` and `docs/fold.md`)

- German *ch* for `х` (*Michail*, *Chruschtschow*) and *z* for `ц`
  (*Zwetajewa*); French *ch* for `ш` (*Pouchkine*) and *j* for `ж`.
- *Rachmaninoff* (English *ch* for `х`).
- English *c* for `к` (*Nicolai*, *Victor*): *c* is `ц` in ISO 9 and the
  scholarly spelling, which European library records use.
- Translated names (*Peter*, *Moscow*), and spelling changes of the reform
  (`Русскаго`/`Русского`).
- **Over-merge**: rule 5 merges names that differ by an *i*/*y* before *e*
  (`Майер` and `Маер`), declared in `test_declares_the_known_over_merges`.
- Armenian or Georgian names in Russian (`Хачатурян`) fold as Russian; joining
  them to the other script is a name authority's job.

## The test data

`tests/data/ru_fold_cases.tsv`: 23 groups — composers and writers
(*Chaikovskii*, *Dostoevskii*, *Tsvetaeva*, *Musorgskii*, *Shchedrin*),
places (*Ekaterinburg*, *Nizhnii*, *Rossiia*), given names (*Evgenii*, *Fedor*,
*Iurii*, *Aleksei*, *Natalia*, *Petr*) and pre-reform words (`вѣстникъ`,
`Ѳеодоръ`, `Пушкинъ`), each in Cyrillic, ALA-LC, BGN/PCGN and the popular,
German, French and scholarly forms that fold. Group names are the key's
ALA-LC-ish spelling, not the key itself.

## Traps

- **`ё` is often printed as `е`.** The fold takes them as one; the schemes do
  not guess, so `Федор` renders *Fedor* and `Фёдор` *Fëdor*.
- **Homoglyphs.** Cyrillic `а е о р с у х` look like Latin `a e o p c y x`. A
  token with one Cyrillic letter is a Cyrillic token to `fold()`; an OCR'd
  Latin word with a stray Cyrillic `о` gets the Russian rules.
- **A capital tie**: `transliterate("Ц", ...)` is *T͡S*, not *T͡s*; a word in
  capitals is upper-cased whole as usual.
- **The final hard sign** differs between the 2011 and 2012 tables; never
  "fix" `ru/ala_lc` to drop it.
