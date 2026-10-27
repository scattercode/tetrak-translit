"""Script and variant detection."""

from __future__ import annotations

import pytest

from tetrak_translit import detect, orthography
from tetrak_translit.detect import romanisations
from tetrak_translit.hy.orthography import markers
from tetrak_translit.ru.orthography import orthography as russian_orthography


class TestScript:
    @pytest.mark.parametrize(
        ("text", "script", "key"),
        [
            ("Երևան", "armenian", "hy"),
            ("თბილისი", "georgian", "ka"),
            ("ᲗᲑᲘᲚᲘᲡᲘ", "georgian", "ka"),
            ("Yerevan", "latin", None),
            ("Ереван", "cyrillic", "ru"),
            ("Erevan (Երևան)", "mixed", "hy"),
            ("Երևան და თბილისი", "mixed", None),
            ("Українська мова", "cyrillic", "ru"),
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


class TestRussianOrthography:
    @pytest.mark.parametrize(
        "text",
        [
            "Русскій вѣстникъ",
            "Ѳеодоръ",  # fita
            "мѵро",  # izhitsa
            "Миръ",  # the final hard sign alone
            "РОССІЯ",  # capitals
            "Пушкинъ и Москва",  # one tell is enough
        ],
    )
    def test_pre_reform(self, text: str) -> None:
        assert detect(text).orthography == "pre-reform"

    @pytest.mark.parametrize(
        "text",
        [
            "Пушкин",  # a final consonant with no hard sign
            "Екатеринбург",
            "Подъезд",  # a hard sign inside a word is modern too
            "Русский вестник",
        ],
    )
    def test_reformed(self, text: str) -> None:
        assert detect(text).orthography == "reformed"

    def test_no_cyrillic_has_no_orthography(self) -> None:
        assert russian_orthography("Moskva") is None

    @pytest.mark.parametrize(
        "text",
        [
            "Москва",  # ends in a vowel
            "Толстой",  # ends in й, which both spellings write bare
            "Гоголь",
            "СССР",  # an acronym in capitals
            "г.",  # an abbreviation
            "стр. 5",
            "от",  # too short to say
        ],
    )
    def test_indeterminate_when_both_spellings_agree(self, text: str) -> None:
        assert detect(text).orthography == "indeterminate"


class TestRomanisationMarks:
    @pytest.mark.parametrize(
        ("text", "mark"),
        [
            ("Patmutʻiwn", "aspirate"),  # ALA-LC's ʻ
            ("Patmut'yun", "aspirate"),  # a plain apostrophe
            ("Hayotsʼ", "aspirate"),  # ʼ at the end of a word
            ("Chʻarentsʻ", "aspirate"),
            ("Bacʻ", "aspirate"),  # c after a letter
            ("Kʻnar", "aspirate"),
            ("Patmut̕iwn", "combining-comma"),
            ("Keankʻi mĕ", "e-breve"),
            ("Ṙubēn", "r-dot"),
            ("Gēorg", "long-vowel"),
            ("Ōhanean", "long-vowel"),
            ("Ġazaros", "caron-or-dot"),
            ("Čamčean", "caron-or-dot"),
            ("Łazar", "scholarly"),
            ("Pʿarpecʿi", "scholarly"),
            ("Tschamtschean", "german"),
        ],
    )
    def test_each_mark(self, text: str, mark: str) -> None:
        (found,) = detect(text).romanisations
        assert found.key == "hy"
        assert mark in found.marks

    @pytest.mark.parametrize(
        "text",
        [
            "The Armenian's history",  # English 's
            "Histoire de l’Arménie",  # French elision after l
            "jusqu’au bout",
            "c'est la vie",  # French c', not after a letter
            "A school for scholars",  # not German sch
            "Republic of Armenia",
            "Erker",  # a romanisation with no marks shows nothing
        ],
    )
    def test_ordinary_spelling_carries_no_marks(self, text: str) -> None:
        assert detect(text).romanisations == ()

    def test_distinctive_marks_say_so(self) -> None:
        (found,) = detect("Keankʻi mĕ").romanisations
        assert found.marks == ("aspirate", "e-breve")
        assert found.distinctive

    def test_shared_marks_are_reported_but_not_distinctive(self) -> None:
        """The scholarly ł and the German tsch are evidence, but Polish and
        German use them too."""
        for text in ("Łazar", "Tschamtschean"):
            (found,) = detect(text).romanisations
            assert not found.distinctive

    def test_marks_come_most_distinctive_first(self) -> None:
        (found,) = detect("Ṙubēn").romanisations
        assert found.marks == ("r-dot", "long-vowel")

    def test_decomposed_input_is_read_as_composed(self) -> None:
        assert detect("Keank'i mĕ").romanisations[0].marks == ("aspirate", "e-breve")

    def test_only_text_with_latin_letters_is_read(self) -> None:
        assert detect("Պատմութիւն").romanisations == ()
        assert detect("თბილისი").romanisations == ()
        assert detect("").romanisations == ()

    def test_mixed_text_reports_the_romanisation_beside_the_script(self) -> None:
        found = detect("Patmutʻiwn = Պատմութիւն")
        assert found.script == "mixed"
        assert found.key == "hy"
        assert [r.key for r in found.romanisations] == ["hy"]

    def test_romanisations_reads_any_text(self) -> None:
        assert [r.marks for r in romanisations("Kʻnar")] == [("aspirate",)]

    def test_as_dict(self) -> None:
        view = detect("Keankʻi mĕ").as_dict()
        assert view["romanisations"] == [
            {"key": "hy", "marks": ["aspirate", "e-breve"], "distinctive": True}
        ]
        assert detect("Yerevan").as_dict()["romanisations"] == []
