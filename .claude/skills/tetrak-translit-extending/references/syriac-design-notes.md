# Syriac: design questions to settle before writing a table

Syriac is the next script planned. It is unlike Armenian and Georgian in two
ways that the engine has not had to face — it is written right to left and it
is normally **unvocalised** — and `docs/adding-a-script.md` already says the
fold for such a script must be designed before its tables. These notes are
that design's starting point: the facts that are settled, and the questions
that are not. Nothing here is a decision.

## What is settled

- **Unicode.** The Syriac block is U+0700–U+074F: punctuation U+0700–U+070D,
  the abbreviation mark U+070F (a format character), letters U+0710–U+072F,
  points and other combining marks U+0730–U+074A, and the Garshuni letters
  U+074D–U+074F used when Arabic or Persian is written in Syriac script. The
  Syriac Supplement block U+0860–U+086A holds letters for Malayalam
  Garshuni. The three script styles — Estrangela, Serto (West Syriac),
  Madnhaya (East Syriac) — share one encoding and differ only in the font,
  so detection cannot tell them apart and should not try.
- **`unicode_name`** is `syriac` (every letter's name begins with SYRIAC
  LETTER). **Key**: `syr` is the ISO 639-2 code for Syriac and the obvious
  choice; `syc` is Classical Syriac in ISO 639-3 and `Syrc` the ISO 15924
  script code. The convention in this package is the ISO 639 code of the
  language the script is used for.
- **Caseless**, so `cased=False`.
- **22 consonants** (ܐ ܒ ܓ ܕ ܗ ܘ ܙ ܚ ܛ ܝ ܟ ܠ ܡ ܢ ܣ ܥ ܦ ܨ ܩ ܪ ܫ ܬ), plus
  the dotless `ܖ` (dalath-rish) and a few letters used for other languages.
  Contextual forms (initial, medial, final) are the font's business, not the
  encoding's; the engine never sees them.
- **A standard exists on the library side**: ALA-LC publishes a Syriac
  romanisation table. ISO has none for Syriac. Scholarly practice (the
  conventions of the *Comprehensive Aramaic Lexicon*, of Nöldeke's grammar,
  of the various text editions) varies.

## What is not settled

1. **Vowels.** The points at U+0730–U+074A carry two vowel systems — Eastern,
   with dots, and Western, with small Greek letters — and most running text
   carries neither. A transliteration of unvocalised text cannot write vowels
   it has not been given, and the table has to be honest about that: a
   rendering of `ܡܠܟܐ` is *mlkʾ* (or whatever the chosen scheme writes for
   consonants only), not *malkā*, unless the points are there. Decide whether
   the scheme renders points when present and skips them when absent, and
   whether that counts as one scheme or two. The engine's `letters` map is
   per code point, so points can be mapped like letters; `reversible` for a
   pointed text is plausible, for an unpointed one meaningless.
2. **The matres lectionis.** `ܐ`, `ܘ` and `ܝ` are consonants that also stand
   for long vowels. A consonant-only rendering writes them as consonants
   (*ʾ*, *w*, *y*); a reader's rendering writes vowels. The fold must merge
   the two, which means the Latin side of the fold has to know that *w* and
   *o*/*u* can be the same letter.
3. **Spirantisation.** Rukkakha and qushshaya (U+0741, U+0742) mark whether
   `ܒ ܓ ܕ ܟ ܦ ܬ` are plosive or fricative. A scheme that renders *b*/*ḇ*,
   *k*/*ḵ* and so on from the marks is more informative; the fold should
   certainly merge them.
4. **The consonantal fold.** The present folds are built for scripts where
   the vowels are letters. A Syriac fold has to drop vowels on the **Latin**
   side too, or an ALA-LC *Malkā* will never match the script's `ܡܠܟܐ`.
   Design questions: which Latin vowels are dropped (all? only those not
   carrying a mater?); whether `ʾ` and `ʿ` survive as consonants or go with
   the apostrophes; how doubled consonants (gemination is not marked in the
   script) are treated. `latin.clean()` and `FINISH` can be reused; the rules
   between them will be new in kind.
5. **Names across scripts.** Syriac material in catalogues is also recorded
   in Arabic, Hebrew and Greek script forms, and in several Latin spellings
   drawn from each. The fold's remit — which spellings of one name in one
   script's romanisations should match — needs stating before the test set
   can be written, or the case set will grow without a boundary.
6. **Garshuni.** Arabic in Syriac letters is Syriac to `detect()` and
   nonsense to a Syriac table. Probably out of scope, and the docs should say
   so, as the Georgian package says for Asomtavruli and Nuskhuri.
7. **Direction.** The engine works in logical order, and Unicode text is
   stored in logical order, so right-to-left is not an engine problem. It is
   a display problem for the callers who put a Latin rendering beside a
   Syriac transcript, and worth a sentence in the docs.

## Where to start

Settle 1, 2 and 4 on paper with a dozen names — Ephrem, Aphrahat, Jacob of
Serugh, Bar Hebraeus, Edessa, Nisibis, Tur Abdin — written as the ALA-LC
table gives them pointed and unpointed, and decide what the key for each
should be. That is the case set in embryo, and it answers whether the
engine's `Script`/`Scheme` model holds or whether points need a construct of
their own. If the engine must change to admit Syriac, that is its own pull
request first, as `CONTRIBUTING.md` requires.
