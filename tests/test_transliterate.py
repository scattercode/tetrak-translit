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
            ("Չարենց", "iso_9985", "Čarenc'"),
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


class TestGeorgianToLatin:
    @pytest.mark.parametrize(
        ("text", "scheme", "expected"),
        [
            ("თბილისი", "ala_lc", "tʻbilisi"),
            ("თბილისი", "iso_9984", "t'bilisi"),
            ("თბილისი", "national", "tbilisi"),
            ("ქუთაისი", "ala_lc", "kʻutʻaisi"),
            ("ქუთაისი", "national", "kutaisi"),
            ("ჭავჭავაძე", "ala_lc", "chavchavadze"),
            ("ჭავჭავაძე", "iso_9984", "čavčavaje"),
            ("ჭავჭავაძე", "national", "ch'avch'avadze"),
            ("წერეთელი", "ala_lc", "tseretʻeli"),
            ("წერეთელი", "iso_9984", "ceret'eli"),
            ("წერეთელი", "national", "ts'ereteli"),
            ("მცხეთა", "ala_lc", "mtsʻkhetʻa"),
            ("მცხეთა", "iso_9984", "mc'xet'a"),
            ("მცხეთა", "national", "mtskheta"),
            ("ჯავახიშვილი", "iso_9984", "ǰavaxišvili"),
            ("ღვინო", "iso_9984", "ḡvino"),
            ("ყაზბეგი", "national", "q'azbegi"),
            ("ჴელი", "ala_lc", "ẖeli"),  # archaic
            ("ჴელი", "iso_9984", "ẖeli"),
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
            ("hy/hubschmann_meillet", "Խաչատրյան"),
            ("hy/hubschmann_meillet", "Մեսրոպ Մաշտոց"),
            ("ka/iso_9984", "თბილისი"),
            ("ka/iso_9984", "ჭავჭავაძე"),
            ("ka/iso_9984", "მცხეთა"),
            ("ka/iso_9984", "ჴელი"),
        ],
    )
    def test_round_trips_words(self, scheme: str, text: str) -> None:
        assert to_script(to_latin(text, scheme), scheme) == text

    def test_the_two_letter_ew_comes_back_as_the_ligature(self) -> None:
        """Same letters, one typographic form; documented, not a bug."""
        assert to_armenian(to_latin("Երեւան", "iso_9985"), "iso_9985") == "Երևան"

    def test_any_apostrophe_marks_aspiration(self) -> None:
        for mark in ("'", "’", "ʻ", "ʿ"):
            assert to_armenian(f"Čarenc{mark}", "iso_9985") == "Չարենց"
            assert to_script(f"T{mark}bilisi", "iso_9984") == "თბილისი"

    def test_capitals_with_no_precomposed_form_read_back(self) -> None:
        """Capital ǰ is J and a combining caron; Unicode has no single character."""
        assert to_armenian("J̌owr", "iso_9985") == "Ջուր"
        assert to_script("J̌avaxišvili", "iso_9984") == "ჯავახიშვილი"

    def test_a_match_does_not_split_a_character(self) -> None:
        assert to_armenian("é", "iso_9985") == "é"

    def test_latin_capitals_are_dropped_for_a_caseless_script(self) -> None:
        assert to_script("T'bilisi", "ka/iso_9984") == "თბილისი"
        assert to_script("T'BILISI", ka.ISO_9984) == "თბილისი"

    def test_non_scheme_characters_pass_through(self) -> None:
        assert to_armenian("Erewan, 1985.", "iso_9985") == "Երևան, 1985."

    def test_the_to_argument_names_the_script(self) -> None:
        assert transliterate("Erewan", "iso_9985", to="armenian") == "Երևան"
        assert transliterate("Erewan", "iso_9985", to="hy") == "Երևան"
        assert transliterate("T'bilisi", "iso_9984", to="script") == "თბილისი"
        assert transliterate("T'bilisi", "iso_9984", to="Georgian") == "თბილისი"

    def test_lossy_schemes_refuse(self) -> None:
        for key in ("hy/ala_lc", "bgn_pcgn", "western", "ka/ala_lc", "national"):
            with pytest.raises(NotReversibleError, match="not reversible"):
                transliterate("Erevan", key, to="script")

    def test_reading_back_needs_the_script_settled(self) -> None:
        with pytest.raises(UnknownSchemeError, match="say which"):
            transliterate("Tbilisi", "ala_lc", to="script")
