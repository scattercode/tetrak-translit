"""The canonical fold: the published test set, and the rules behind it."""

from __future__ import annotations

from pathlib import Path

import pytest

from tetrak_translit import fold, fold_token, transliterate
from tetrak_translit.schemes import SCHEMES

FOLD_CASES = Path(__file__).parent / "data" / "fold_cases.tsv"


class TestPublishedCases:
    def test_the_set_is_not_trivial(self, fold_groups: dict[str, list[tuple[str, str]]]) -> None:
        assert len(fold_groups) >= 20
        assert all(len(forms) >= 2 for forms in fold_groups.values())

    def test_every_group_folds_to_one_key(
        self, fold_groups: dict[str, list[tuple[str, str]]]
    ) -> None:
        """The whole set in one assertion, so a failure names every miss at once."""
        misses = []
        for group, forms in fold_groups.items():
            keys = {form: fold(form) for form, _ in forms}
            if len(set(keys.values())) != 1:
                misses.append((group, keys))
        assert not misses, f"{len(misses)} of {len(fold_groups)} groups do not fold together"

    def test_different_names_stay_different(
        self, fold_groups: dict[str, list[tuple[str, str]]]
    ) -> None:
        """A fold that mapped everything to one key would pass the test above."""
        keys = {group: fold(forms[0][0]) for group, forms in fold_groups.items()}
        assert len(set(keys.values())) == len(keys)

    def test_the_file_is_well_formed(self) -> None:
        lines = FOLD_CASES.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "group\tform\tnote"
        for line in lines[1:]:
            assert line.count("\t") == 2, line


class TestAllSchemesFoldToTheArmenian:
    """What the engine renders, the fold must take back -- for every scheme."""

    @pytest.mark.parametrize("key", list(SCHEMES))
    @pytest.mark.parametrize(
        "text",
        [
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
    )
    def test_rendering_folds_like_its_source(self, key: str, text: str) -> None:
        assert fold(transliterate(text, key)) == fold(text)


class TestSchemeHint:
    def test_a_reversible_scheme_hint_resolves_j(self) -> None:
        """ISO 9985 j is ձ; without the hint it would fold as ALA-LC's ջ."""
        assert fold("Jowkn", scheme="iso_9985") == fold("Ձուկն")
        assert fold("Jowkn") != fold("Ձուկն")

    def test_a_lossy_scheme_hint_is_ignored(self) -> None:
        assert fold("Yerevan", scheme="bgn_pcgn") == fold("Yerevan")

    def test_a_hint_is_ignored_for_armenian_input(self) -> None:
        assert fold("Երևան", scheme="iso_9985") == fold("Երևան")


class TestKey:
    def test_is_lowercase_ascii(self) -> None:
        for text in ("Պօղոսեան", "Chʻarentsʻ", "Čʿarencʿ", "ԵՐԵՎԱՆ"):
            key = fold(text)
            assert key == key.lower()
            assert key.isascii() and key.isalnum()

    def test_tokens_are_joined_with_single_spaces(self) -> None:
        assert fold("  Մեսրոպ   Մաշտոց \n") == "mesrop mashtoc"

    def test_punctuation_only_tokens_vanish(self) -> None:
        assert fold("— Երևան —") == "erevan"
        assert fold("…") == ""
        assert fold_token("…") == ""

    def test_digits_survive(self) -> None:
        assert fold("Երկեր, հատոր 2") == "erker hator 2"

    def test_is_idempotent(self) -> None:
        for text in ("Պօղոսեան", "Boghossian", "Չարենց", "Yerevan"):
            assert fold(fold(text)) == fold(text)

    def test_does_not_claim_the_known_gaps(self) -> None:
        """Documented in docs/fold.md. If one of these starts passing, move it
        into the test set and out of the gaps."""
        assert fold("Megerdich") != fold("Մկրտիչ")
        assert fold("Khachaturian") != fold("Խաչատրյան")
