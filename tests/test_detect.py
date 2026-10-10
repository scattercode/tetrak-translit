"""Script and variant detection."""

from __future__ import annotations

import pytest

from tetrak_translit import detect, orthography
from tetrak_translit.hy.orthography import markers


class TestScript:
    @pytest.mark.parametrize(
        ("text", "script", "key"),
        [
            ("Երևան", "armenian", "hy"),
            ("თბილისი", "georgian", "ka"),
            ("ᲗᲑᲘᲚᲘᲡᲘ", "georgian", "ka"),
            ("Yerevan", "latin", None),
            ("Ереван", "cyrillic", None),
            ("Erevan (Երևան)", "mixed", "hy"),
            ("Երևան და თბილისი", "mixed", None),
            ("1922 — ...", "none", None),
            ("", "none", None),
        ],
    )
    def test_script_and_key(self, text: str, script: str, key: str | None) -> None:
        found = detect(text)
        assert (found.script, found.key) == (script, key)

    def test_mixed_reports_the_dominant_script(self) -> None:
        found = detect("Հայաստանի Հանրապետություն, Republic of Armenia")
        assert found.script == "mixed"
        assert found.dominant == "armenian"
        assert found.letters["armenian"] > found.letters["latin"]

    def test_non_registered_scripts_have_no_orthography(self) -> None:
        assert detect("Yerevan").orthography is None
        assert detect("").orthography is None
        assert orthography("Yerevan") is None

    def test_georgian_has_no_orthography(self) -> None:
        assert detect("თბილისი").orthography is None

    def test_diacritics_do_not_change_the_script(self) -> None:
        assert detect("Chʻarentsʻ Ēǰmiacin Tʻbilisi").script == "latin"

    def test_as_dict_is_json_shaped(self) -> None:
        view = detect("Երեւան").as_dict()
        assert view["script"] == "armenian"
        assert view["key"] == "hy"
        assert view["orthography"] == "classical"


class TestArmenianOrthography:
    @pytest.mark.parametrize(
        "text",
        [
            "Երեւան",  # two-letter եւ
            "իւր",  # free ւ
            "հաւատք",
            "Ազգ եւ հայրենիք",
            "Պօղոսեան",  # classical եա
            "Գէորգ",  # inner է
            "ՍԷՐ",  # inner է after a capital
            "Հայկական տպագրութիւն և գրքարուեստ",  # a classical press that sets the ligature
        ],
    )
    def test_classical(self, text: str) -> None:
        assert detect(text).orthography == "classical"

    @pytest.mark.parametrize(
        "text",
        [
            "Երևան",  # the ligature
            "Պողոսյան",  # medial յ after a consonant
            "Ավետիքյան",
            "Ազգ և հայրենիք",
        ],
    )
    def test_reformed(self, text: str) -> None:
        assert detect(text).orthography == "reformed"

    @pytest.mark.parametrize("text", ["Արմեն", "հայ", "Հայաստան", "ԵՐԵՎԱՆ", "ու"])
    def test_indeterminate_when_both_orthographies_spell_it_the_same(self, text: str) -> None:
        assert detect(text).orthography == "indeterminate"

    def test_a_free_yiwn_outranks_the_ligature(self) -> None:
        """A classical press setting և is still classical; the trainer measured
        Հայկական տպագրութիւն at 2 ligatures to 22 two-letter forms."""
        assert detect("տպագրութիւն և").orthography == "classical"

    def test_ou_is_not_a_free_yiwn(self) -> None:
        assert markers("Սուրբ").free_yiwn == 0
        assert markers("Ուրարտու").free_yiwn == 0

    def test_final_y_is_reported_but_does_not_decide(self) -> None:
        assert markers("ծառայ").final_y == 1
        assert detect("ծառայ").orthography == "indeterminate"
