"""Transliteration in both directions, for both scripts."""

from __future__ import annotations

import pytest

from tetrak_translit import (
    SCHEMES,
    NotReversibleError,
    UnknownSchemeError,
    UnknownScriptError,
    hy,
    ka,
    to_armenian,
    to_latin,
    to_script,
    transliterate,
)


class TestArmenianToLatin:
    @pytest.mark.parametrize(
        ("text", "scheme", "expected"),
        [
            ("Երևան", "ala_lc", "Erevan"),
            ("Երեւան", "ala_lc", "Erewan"),
            ("Երևան", "bgn_pcgn", "Yerevan"),
            ("Երևան", "iso_9985", "Erewan"),
            ("Երևան", "hubschmann_meillet", "Erewan"),
            ("Երևան", "western", "Yerevan"),
            ("Յակոբ", "ala_lc", "Yakob"),
            ("Յակոբ", "western", "Hagop"),
            ("Գէորգ", "ala_lc", "Gēorg"),
            ("Գէորգ", "western", "Kevork"),
            ("Պօղոսեան", "western", "Boghosian"),
            ("Ոսկան", "ala_lc", "Oskan"),
            ("Ոսկան", "bgn_pcgn", "Voskan"),
            ("Չարենց", "ala_lc", "Chʻarentsʻ"),
            ("Չարենց", "iso_9985", "Č'arenc'"),
            ("Չարենց", "iso_9985_1996", "Čarenc'"),
            # The four letters the 2026 edition changed.
            ("Ծիծեռնակ", "iso_9985", "Ciceṙnak"),
            ("Ծիծեռնակ", "iso_9985_1996", "Çiçeṙnak"),
            ("Ճաշ", "iso_9985", "Čaš"),
            ("Ճաշ", "iso_9985_1996", "Č̣aš"),
            ("Պօղոսեան", "iso_9985", "Pōġosean"),
            ("Պօղոսեան", "iso_9985_1996", "Pòġosean"),
            ("Չարենց", "hubschmann_meillet", "Čʿarencʿ"),
            ("Չարենց", "bgn_pcgn", "Ch'arents'"),
            ("Սուրբ", "iso_9985", "Sowrb"),
            ("Սուրբ", "ala_lc", "Surb"),
            ("Ռուբէն", "bgn_pcgn", "Rruben"),
            ("Ազգ և հայրենիք", "bgn_pcgn", "Azg yev hayrenik'"),
            ("Ազգ և հայրենիք", "ala_lc", "Azg ev hayrenikʻ"),
        ],
    )
    def test_known_forms(self, text: str, scheme: str, expected: str) -> None:
        assert transliterate(text, scheme) == expected

    def test_default_scheme_is_ala_lc_of_the_text_s_script(self) -> None:
        assert transliterate("Երևան") == "Erevan"
        assert transliterate("თბილისი") == "tʻbilisi"

    def test_capitals_carry_across(self) -> None:
        assert transliterate("ԵՐԵՎԱՆ", "bgn_pcgn") == "YEREVAN"
        assert transliterate("Թ", "ala_lc") == "Tʻ"
        assert transliterate("ԹԹ", "ala_lc") == "TʻTʻ"

    def test_other_scripts_pass_through(self) -> None:
        line = "Charents, Eghishe, 1897-1937. Երկեր / Yerevan, 1985."
        assert (
            transliterate(line, "ala_lc") == "Charents, Eghishe, 1897-1937. Erker / Yerevan, 1985."
        )
        assert transliterate("Երևան და თბილისი", "hy/ala_lc") == "Erevan და თბილისი"
        assert transliterate("Երևան და თბილისი", "ka/ala_lc") == "Երևան da tʻbilisi"

    def test_punctuation_inside_a_word_is_kept(self) -> None:
        assert transliterate("Սայաթ-Նովա", "ala_lc") == "Sayatʻ-Nova"
        assert transliterate("«Երկեր»", "ala_lc") == "«Erker»"

    def test_scheme_objects_and_forgiving_keys(self) -> None:
        assert transliterate("Երևան", hy.ALA_LC) == "Erevan"
        assert transliterate("Երևան", "ISO 9985") == "Erewan"
        assert transliterate("Երևան", "hy/ala-lc") == "Erevan"

    def test_errors(self) -> None:
        with pytest.raises(UnknownSchemeError, match="known schemes"):
            transliterate("Երևան", "wade-giles")
        with pytest.raises(UnknownScriptError):
            transliterate("Երևան", "ala_lc", script="syr")
        with pytest.raises(UnknownScriptError):
            transliterate("Erewan", "iso_9985", to="greek")


class TestWesternPositionalRules:
    def test_initial_y_is_h_but_medial_y_is_y(self) -> None:
        assert transliterate("Յարութիւն", "western") == "Harutiun"
        assert transliterate("Հայաստան", "western") == "Hayasdan"

    def test_o_after_a_vowel_is_vo(self) -> None:
        assert transliterate("Գէորգ", "western") == "Kevork"
        assert transliterate("Պօղոս", "western") == "Boghos"

    def test_classical_ea_is_ia(self) -> None:
        assert transliterate("Վարդանեան", "western") == "Vartanian"


# ISO 9984:2026 Table 4: each letter's example, as the standard prints it
# (with the optional initial capital).
ISO_9984_2026_EXAMPLES = [
    ("ამბროლაური", "Ambrolauri"),
    ("ბათუმი", "Batumi"),
    ("გორი", "Gori"),
    ("დუშეთი", "Dusheti"),
    ("ერგე", "Erge"),
    ("ვანი", "Vani"),
    ("ზუგდიდი", "Zugdidi"),
    ("თბილისი", "Tbilisi"),
    ("ონი", "Oni"),
    ("კასპი", "K'asp'i"),
    ("ლაგოდეხი", "Lagodekhi"),
    ("მარნეული", "Marneuli"),
    ("ნინოწმინდა", "Ninots'minda"),
    ("ოზურგეთი", "Ozurgeti"),
    ("პანტნარი", "P'ant'nari"),
    ("ჟანივრი", "Zhanivri"),
    ("რუსთავი", "Rustavi"),
    ("სენაკი", "Senak'i"),
    ("სამტრედია", "Samt'redia"),
    ("ქუთაისი", "Kutaisi"),
    ("ფოთი", "Poti"),
    ("ქობულეთი", "Kobuleti"),
    ("ღრმაღელე", "Ghrmaghele"),
    ("ყუმისთავი", "Q'umistavi"),
    ("შხარა", "Shkhara"),
    ("ჩუნეში", "Chuneshi"),
    ("ცაგერი", "Tsageri"),
    ("ძეძილეთი", "Dzedzileti"),
    ("წალკა", "Ts'alk'a"),
    ("აჭარა", "Ach'ara"),
    ("ხაშური", "Khashuri"),
    ("ჯვარი", "Jvari"),
    ("ჰეღო", "Hegho"),
]


class TestIso9984Edition2026:
    @pytest.mark.parametrize(("text", "expected"), ISO_9984_2026_EXAMPLES)
    def test_the_standards_examples(self, text: str, expected: str) -> None:
        rendered = transliterate(text, "ka/iso_9984")
        assert rendered[:1].upper() + rendered[1:] == expected
        assert to_script(expected, "ka/iso_9984") == text

    @pytest.mark.parametrize(
        ("text", "expected"),
        [("ზჰ", "z·h"), ("გჰ", "g·h"), ("სჰ", "s·h"), ("ქჰ", "k·h"), ("თს", "t·s"), ("დზ", "d·z")],
    )
    def test_a_middle_dot_keeps_two_letters_from_reading_as_a_digraph(
        self, text: str, expected: str
    ) -> None:
        assert transliterate(text, "ka/iso_9984") == expected
        assert to_script(expected, "ka/iso_9984") == text
        assert to_script(expected.replace("·", ""), "ka/iso_9984") != text

    def test_the_separator_survives_capitals(self) -> None:
        assert transliterate("ᲖᲰ", "ka/iso_9984") == "Z·H"

    def test_the_apostrophe_marks_the_ejective(self) -> None:
        assert transliterate("ტ", "ka/iso_9984") == "t'"
        assert transliterate("თ", "ka/iso_9984") == "t"

    def test_the_historical_letters_of_table_5(self) -> None:
        assert transliterate("ჱჲჳჴჵჶჷჸჹჺჼჽჾჿ", "ka/iso_9984") == "ēywẖōfȳʔĝʕⁿæʸʷ"
        assert to_script("ēywẖōfȳʔĝʕⁿæʸʷ", "ka/iso_9984") == "ჱჲჳჴჵჶჷჸჹჺჼჽჾჿ"

    def test_sequences_the_standards_list_leaves_ambiguous(self) -> None:
        """dzh and tsh read two ways; reading back takes the digraph first."""
        assert transliterate("დჟ", "ka/iso_9984") == transliterate("ძჰ", "ka/iso_9984")
        assert transliterate("თშ", "ka/iso_9984") == transliterate("ცჰ", "ka/iso_9984")
        assert to_script("dzh", "ka/iso_9984") == "ძჰ"
        assert to_script("tsh", "ka/iso_9984") == "ცჰ"


class TestIso9985Punctuation:
    """ISO 9985:2026 Table 2: every mark where it stands."""

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("Դու կարդացե՞լ ես այս գիրքը։", "Dow kardac'e?l es ays girk'ë."),
            ("Այս ու՜մ եմ տեսնում։", "Ays ow!m em tesnowm."),
            ("Կարդա՛, գրի՛ր տարին բոլոր։", "Kardaˆ, griˆr tarin bolor."),
            ("Ա․ Բ․ Սարգսյան՝ հայ֊անգլերեն", "A; B; Sargsyan: hay-angleren"),
            ("ԿԱՐԴԱ՛", "KARDAˆ"),
        ],
    )
    def test_table_2(self, text: str, expected: str) -> None:
        assert transliterate(text, "iso_9985") == expected
        assert to_armenian(expected, "iso_9985") == text

    def test_the_first_edition_leaves_punctuation_alone(self) -> None:
        assert transliterate("Ո՞վ է։", "iso_9985_1996") == "O՞v ē։"


class TestMarksInsideAWord:
    """Armenian's stress marks sit over a vowel, inside the word."""

    def test_a_word_in_capitals_stays_in_capitals(self) -> None:
        assert transliterate("Ո՞Վ", "bgn_pcgn") == "VO՞V"

    def test_the_letter_after_a_mark_is_not_word_initial(self) -> None:
        # BGN/PCGN writes initial ե as ye; inside a word it is e.
        assert transliterate("կարդացե՞լ", "bgn_pcgn") == "kardats'e՞l"
        assert transliterate("Երե՞ւան", "bgn_pcgn").startswith("Yere")

    def test_a_scheme_without_punctuation_leaves_marks_where_they_stand(self) -> None:
        assert transliterate("ու՜մ", "hubschmann_meillet") == "u՜m"


class TestGeorgianToLatin:
    @pytest.mark.parametrize(
        ("text", "scheme", "expected"),
        [
            ("თბილისი", "ala_lc", "tʻbilisi"),
            ("თბილისი", "iso_9984_1996", "t'bilisi"),
            ("თბილისი", "national", "tbilisi"),
            ("ქუთაისი", "ala_lc", "kʻutʻaisi"),
            ("ქუთაისი", "national", "kutaisi"),
            ("ჭავჭავაძე", "ala_lc", "chavchavadze"),
            ("ჭავჭავაძე", "iso_9984_1996", "čavčavaje"),
            ("ჭავჭავაძე", "national", "ch'avch'avadze"),
            ("წერეთელი", "ala_lc", "tseretʻeli"),
            ("წერეთელი", "iso_9984_1996", "ceret'eli"),
            ("წერეთელი", "national", "ts'ereteli"),
            ("მცხეთა", "ala_lc", "mtsʻkhetʻa"),
            ("მცხეთა", "iso_9984_1996", "mc'xet'a"),
            ("მცხეთა", "national", "mtskheta"),
            ("ჯავახიშვილი", "iso_9984_1996", "ǰavaxišvili"),
            ("ღვინო", "iso_9984_1996", "ḡvino"),
            ("ყაზბეგი", "national", "q'azbegi"),
            ("ჴელი", "ala_lc", "ẖeli"),  # archaic
            ("ჴელი", "iso_9984_1996", "ẖeli"),
            ("ჶ", "iso_9984_1996", "f"),
        ],
    )
    def test_known_forms(self, text: str, scheme: str, expected: str) -> None:
        assert transliterate(text, scheme) == expected

    def test_mkhedruli_is_caseless_so_nothing_is_capitalised(self) -> None:
        assert transliterate("თბილისი", "national") == "tbilisi"

    def test_mtavruli_renders_as_capitals(self) -> None:
        assert transliterate("ᲗᲑᲘᲚᲘᲡᲘ", "national") == "TBILISI"
        assert transliterate("Თბილისი", "national") == "Tbilisi"

    def test_a_letter_the_scheme_does_not_define_passes_through(self) -> None:
        """The national system defines no archaic letters; ჴ is left as it is."""
        assert transliterate("ჴელი", "national") == "ჴeli"


class TestToScript:
    @pytest.mark.parametrize(
        "scheme", [s for s in SCHEMES.values() if s.reversible], ids=lambda s: s.id
    )
    def test_round_trips_every_letter(self, scheme) -> None:  # type: ignore[no-untyped-def]
        alphabet = scheme.script.letters + "".join(scheme.script.digraphs)
        assert to_script(to_latin(alphabet, scheme), scheme) == alphabet

    @pytest.mark.parametrize(
        ("scheme", "text"),
        [
            ("hy/iso_9985", "Երևան"),
            ("hy/iso_9985", "Չարենց"),
            ("hy/iso_9985", "Սուրբ Էջմիածին"),
            ("hy/iso_9985", "ՉԱՐԵՆՑ"),
            ("hy/iso_9985", "Ճաշ Չարենց Ծիծեռնակ Օհան Ջուր"),
            ("hy/iso_9985_1996", "Ճաշ Չարենց Ծիծեռնակ Օհան Ջուր"),
            ("hy/hubschmann_meillet", "Խաչատրյան"),
            ("hy/hubschmann_meillet", "Մեսրոպ Մաշտոց"),
            ("ka/iso_9984_1996", "თბილისი"),
            ("ka/iso_9984_1996", "ჭავჭავაძე"),
            ("ka/iso_9984_1996", "მცხეთა"),
            ("ka/iso_9984_1996", "ჴელი"),
        ],
    )
    def test_round_trips_words(self, scheme: str, text: str) -> None:
        assert to_script(to_latin(text, scheme), scheme) == text

    def test_the_two_letter_ew_comes_back_as_the_ligature(self) -> None:
        """Same letters, one typographic form; documented, not a bug."""
        assert to_armenian(to_latin("Երեւան", "iso_9985"), "iso_9985") == "Երևան"

    def test_any_apostrophe_marks_aspiration(self) -> None:
        for mark in ("'", "’", "ʻ", "ʿ"):
            assert to_armenian(f"Č{mark}arenc{mark}", "iso_9985") == "Չարենց"
            assert to_armenian(f"Čarenc{mark}", "iso_9985_1996") == "Չարենց"
            assert to_script(f"T{mark}bilisi", "iso_9984_1996") == "თბილისი"

    def test_capitals_with_no_precomposed_form_read_back(self) -> None:
        """Capital ǰ is J and a combining caron; Unicode has no single character."""
        assert to_armenian("J̌owr", "iso_9985") == "Ջուր"
        assert to_script("J̌avaxišvili", "iso_9984_1996") == "ჯავახიშვილი"

    def test_a_match_does_not_split_a_character(self) -> None:
        assert to_armenian("é", "iso_9985") == "é"

    def test_latin_capitals_are_dropped_for_a_caseless_script(self) -> None:
        assert to_script("T'bilisi", "ka/iso_9984_1996") == "თბილისი"
        assert to_script("T'BILISI", ka.ISO_9984_1996) == "თბილისი"

    def test_non_scheme_characters_pass_through(self) -> None:
        assert to_armenian("Erewan, 1985.", "hubschmann_meillet") == "Երևան, 1985."

    def test_iso_9985_reads_its_punctuation_back(self) -> None:
        """Table 2 maps the full stop both ways, so a Latin one becomes ։."""
        assert to_armenian("Erewan, 1985.", "iso_9985") == "Երևան, 1985։"

    def test_the_to_argument_names_the_script(self) -> None:
        assert transliterate("Erewan", "iso_9985", to="armenian") == "Երևան"
        assert transliterate("Erewan", "iso_9985", to="hy") == "Երևան"
        assert transliterate("T'bilisi", "iso_9984_1996", to="script") == "თბილისი"
        assert transliterate("T'bilisi", "iso_9984_1996", to="Georgian") == "თბილისი"

    def test_lossy_schemes_refuse(self) -> None:
        for key in ("hy/ala_lc", "bgn_pcgn", "western", "ka/ala_lc", "national"):
            with pytest.raises(NotReversibleError, match="not reversible"):
                transliterate("Erevan", key, to="script")

    def test_reading_back_needs_the_script_settled(self) -> None:
        with pytest.raises(UnknownSchemeError, match="say which"):
            transliterate("Tbilisi", "ala_lc", to="script")
