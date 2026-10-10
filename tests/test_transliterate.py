"""Transliteration in both directions."""

from __future__ import annotations

import pytest

from tetrak_translit import (
    NotReversibleError,
    UnknownSchemeError,
    get_scheme,
    schemes,
    to_armenian,
    to_latin,
    transliterate,
)
from tetrak_translit.schemes import ARMENIAN_LOWERCASE, SCHEMES


class TestToLatin:
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

    def test_default_scheme_is_ala_lc(self) -> None:
        assert transliterate("Երևան") == "Erevan"

    def test_capitals_carry_across(self) -> None:
        assert transliterate("ԵՐԵՎԱՆ", "bgn_pcgn") == "YEREVAN"
        assert transliterate("Թ", "ala_lc") == "Tʻ"
        assert transliterate("ԹԹ", "ala_lc") == "TʻTʻ"

    def test_non_armenian_passes_through(self) -> None:
        line = "Charents, Eghishe, 1897-1937. Երկեր / Yerevan, 1985."
        assert (
            transliterate(line, "ala_lc") == "Charents, Eghishe, 1897-1937. Erker / Yerevan, 1985."
        )

    def test_punctuation_inside_armenian_is_kept(self) -> None:
        assert transliterate("Սայաթ-Նովա", "ala_lc") == "Sayatʻ-Nova"
        assert transliterate("«Երկեր»", "ala_lc") == "«Erker»"

    def test_scheme_keys_are_forgiving(self) -> None:
        assert get_scheme("ALA-LC") is SCHEMES["ala_lc"]
        assert get_scheme("iso 9985") is SCHEMES["iso_9985"]
        assert get_scheme(SCHEMES["western"]) is SCHEMES["western"]

    def test_unknown_scheme_names_the_known_ones(self) -> None:
        with pytest.raises(UnknownSchemeError, match="ala_lc"):
            transliterate("Երևան", "wade-giles")

    def test_schemes_lists_them_in_order(self) -> None:
        assert [scheme.key for scheme in schemes()] == list(SCHEMES)

    def test_bad_direction(self) -> None:
        with pytest.raises(ValueError, match="to must be"):
            transliterate("Երևան", "ala_lc", to="greek")


class TestWesternPositionalRules:
    def test_initial_y_is_h_but_medial_y_is_y(self) -> None:
        assert transliterate("Յարութիւն", "western") == "Harutiun"
        assert transliterate("Հայաստան", "western") == "Hayasdan"

    def test_o_after_a_vowel_is_vo(self) -> None:
        assert transliterate("Գէորգ", "western") == "Kevork"
        assert transliterate("Պօղոս", "western") == "Boghos"

    def test_classical_ea_is_ia(self) -> None:
        assert transliterate("Վարդանեան", "western") == "Vartanian"


class TestToArmenian:
    @pytest.mark.parametrize("key", [key for key, s in SCHEMES.items() if s.reversible])
    def test_round_trips_every_letter(self, key: str) -> None:
        alphabet = ARMENIAN_LOWERCASE + "ու" + "և"
        assert to_armenian(to_latin(alphabet, key), key) == alphabet

    @pytest.mark.parametrize("key", [key for key, s in SCHEMES.items() if s.reversible])
    @pytest.mark.parametrize(
        "text", ["Երևան", "Չարենց", "Խաչատրյան", "Մեսրոպ Մաշտոց", "Սուրբ Էջմիածին", "ՉԱՐԵՆՑ"]
    )
    def test_round_trips_words(self, key: str, text: str) -> None:
        assert to_armenian(to_latin(text, key), key) == text

    def test_the_two_letter_ew_comes_back_as_the_ligature(self) -> None:
        """Same letters, one typographic form; documented, not a bug."""
        assert to_armenian(to_latin("Երեւան", "iso_9985"), "iso_9985") == "Երևան"

    def test_any_apostrophe_marks_aspiration(self) -> None:
        for mark in ("'", "’", "ʻ", "ʿ"):
            assert to_armenian(f"Čarenc{mark}", "iso_9985") == "Չարենց"

    def test_non_scheme_characters_pass_through(self) -> None:
        assert to_armenian("Erewan, 1985.", "iso_9985") == "Երևան, 1985."

    def test_lossy_schemes_refuse(self) -> None:
        for key in ("ala_lc", "bgn_pcgn", "western"):
            with pytest.raises(NotReversibleError, match="not reversible"):
                transliterate("Erevan", key, to="armenian")
