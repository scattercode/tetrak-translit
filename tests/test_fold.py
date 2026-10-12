"""The canonical fold: the published test sets, and the rules behind them."""

from __future__ import annotations

import pytest
from conftest import FOLD_CASES

from tetrak_translit import SCHEMES, ScriptRequiredError, fold, fold_token, transliterate

Groups = dict[str, list[tuple[str, str]]]


def test_there_is_a_test_set_for_every_script() -> None:
    assert set(FOLD_CASES) == {"hy", "ka"}


@pytest.mark.parametrize("script", list(FOLD_CASES))
class TestPublishedCases:
    def test_the_set_is_not_trivial(self, fold_groups: dict[str, Groups], script: str) -> None:
        groups = fold_groups[script]
        assert len(groups) >= 15
        assert all(len(forms) >= 2 for forms in groups.values())

    def test_every_group_folds_to_one_key(
        self, fold_groups: dict[str, Groups], script: str
    ) -> None:
        """The whole set in one assertion, so a failure names every miss at once."""
        misses = []
        for group, forms in fold_groups[script].items():
            keys = {form: fold(form, script=script) for form, _ in forms}
            if len(set(keys.values())) != 1:
                misses.append((group, keys))
        assert not misses, (
            f"{len(misses)} of {len(fold_groups[script])} groups do not fold together"
        )

    def test_different_names_stay_different(
        self, fold_groups: dict[str, Groups], script: str
    ) -> None:
        """A fold that mapped everything to one key would pass the test above."""
        keys = {
            group: fold(forms[0][0], script=script) for group, forms in fold_groups[script].items()
        }
        assert len(set(keys.values())) == len(keys)

    def test_the_file_is_well_formed(self, script: str) -> None:
        lines = FOLD_CASES[script].read_text(encoding="utf-8").splitlines()
        assert lines[0] == "group\tform\tnote"
        for line in lines[1:]:
            assert line.count("\t") == 2, line


class TestAllSchemesFoldToTheirScript:
    """What the engine renders, the fold must take back -- for every scheme."""

    SAMPLES = {
        "hy": [
            "Երևան",
            "Երեւան",
            "Յակոբ",
            "Գևորգ",
            "Պողոսյան",
            "Պօղոսեան",
            "Չարենց",
            "Մեսրոպ Մաշտոց",
            "Սուրբ Էջմիածին",
            "Խաչատրյան",
            "Հովհաննես",
            "Ժամանակ",
            "Շուշի",
            "Եղիշե",
            "Վարդանեան",
        ],
        "ka": [
            "თბილისი",
            "ქუთაისი",
            "ბათუმი",
            "მცხეთა",
            "ჭავჭავაძე",
            "წერეთელი",
            "ჯავახიშვილი",
            "ჟორდანია",
            "ყაზბეგი",
            "ღვინო",
            "შოთა რუსთაველი",
            "ძველი",
            "ხელი",
        ],
    }

    @pytest.mark.parametrize("scheme", SCHEMES.values(), ids=lambda s: s.id)
    def test_rendering_folds_like_its_source(self, scheme) -> None:  # type: ignore[no-untyped-def]
        key = scheme.script.key
        for text in self.SAMPLES[key]:
            assert fold(transliterate(text, scheme), script=key) == fold(text), (scheme.id, text)


class TestScriptArgument:
    def test_latin_needs_a_script(self) -> None:
        with pytest.raises(ScriptRequiredError, match="script='hy'"):
            fold("Boghossian")
        with pytest.raises(ScriptRequiredError):
            fold_token("Tbilisi")

    def test_script_text_needs_none(self) -> None:
        assert fold("Պօղոսեան") == "poghosian"
        assert fold("თბილისი") == "tbilisi"

    def test_the_script_only_governs_latin_tokens(self) -> None:
        """Armenian folds as Armenian even under script='ka', and the reverse."""
        assert fold("Պօղոսեան", script="ka") == fold("Պօղոսեան")
        assert fold("თბილისი", script="hy") == fold("თბილისი")

    def test_the_same_latin_folds_differently_per_script(self) -> None:
        """Armenian merges b with p; Georgian keeps them apart."""
        assert fold("Batumi", script="hy") == "patumi"
        assert fold("Batumi", script="ka") == "batumi"

    def test_a_mixed_line_folds_each_token_by_its_own_script(self) -> None:
        assert fold("Երևան და თბილისი", script="ka") == "erevan da tbilisi"


class TestSchemeHint:
    def test_a_reversible_scheme_hint_resolves_armenian_j(self) -> None:
        """ISO 9985 j is ձ; without the hint it would fold as ALA-LC's ջ."""
        assert fold("Jowkn", scheme="iso_9985") == fold("Ձուկն")
        assert fold("Jowkn", script="hy") != fold("Ձուկն")

    def test_a_reversible_scheme_hint_works_for_georgian(self) -> None:
        assert fold("Mc'xet'a", scheme="ka/iso_9984_1996") == fold("მცხეთა")
        assert fold("Mtskheta", scheme="ka/iso_9984") == fold("მცხეთა")

    def test_a_lossy_scheme_hint_is_ignored(self) -> None:
        assert fold("Yerevan", scheme="bgn_pcgn") == fold("Yerevan", script="hy")

    def test_a_hint_is_ignored_for_script_input(self) -> None:
        assert fold("Երևան", scheme="iso_9985") == fold("Երևան")


class TestKey:
    def test_is_lowercase_ascii(self) -> None:
        for text in ("Պօղոսեան", "Chʻarentsʻ", "Čʿarencʿ", "ԵՐԵՎԱՆ", "ჭავჭავაძე", "Čavčavaje"):
            key = fold(text, script="hy" if "č" in text.lower() and "ǰ" not in text else "ka")
            assert key == key.lower()
            assert key.isascii() and key.isalnum()

    def test_tokens_are_joined_with_single_spaces(self) -> None:
        assert fold("  Մեսրոպ   Մաշտոց \n") == "mesrop mashtoc"
        assert fold(" შოთა  რუსთაველი ") == "shota rustaveli"

    def test_punctuation_only_tokens_vanish(self) -> None:
        assert fold("— Երևան —", script="hy") == "erevan"
        assert fold("…", script="hy") == ""

    def test_digits_survive(self) -> None:
        assert fold("Երկեր, հատոր 2", script="hy") == "erker hator 2"

    def test_is_idempotent(self) -> None:
        for text, script in (("Պօղոսեան", "hy"), ("Boghossian", "hy"), ("ჭავჭავაძე", "ka")):
            assert fold(fold(text, script=script), script=script) == fold(text, script=script)

    def test_does_not_claim_the_known_gaps(self) -> None:
        """Documented in docs/fold.md. If one of these starts passing, move it
        into the test set and out of the gaps."""
        assert fold("Megerdich", script="hy") != fold("Մկրտիչ")
        assert fold("Khachaturian", script="hy") != fold("Խաչատրյան")
        assert fold("Akop", script="hy") != fold("Հակոբ")
        assert fold("Arutyunyan", script="hy") != fold("Հարությունյան")
        assert fold("Tiflis", script="ka") != fold("თბილისი")
        assert fold("George", script="ka") != fold("გიორგი")
