"""The canonical fold: the published test sets, and the rules behind them."""

from __future__ import annotations

from typing import ClassVar

import pytest
from conftest import FOLD_CASES

from tetrak_translit import (
    SCHEMES,
    Scheme,
    ScriptRequiredError,
    UnknownSchemeError,
    fold,
    fold_token,
    transliterate,
)

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
    """What the engine renders, the fold must take back -- for every scheme,
    for every script form in the published test sets."""

    #: Renderings the fold is known not to take back, each a declared gap in
    #: docs/fold.md: text to the schemes whose rendering of it misses.
    KNOWN: ClassVar[dict[str, frozenset[str]]] = {
        # Hübschmann-Meillet's bare j for ձ, with no mark in the word to
        # show the scheme.
        "Ձուկն": frozenset({"hy/hubschmann_meillet"}),
    }

    @pytest.mark.parametrize("scheme", SCHEMES.values(), ids=lambda s: s.id)
    def test_rendering_folds_like_its_source(
        self, fold_groups: dict[str, Groups], scheme: Scheme
    ) -> None:
        key = scheme.script.key
        misses = []
        for forms in fold_groups[key].values():
            for text, _ in forms:
                if not scheme.script.has_letters(text) or scheme.id in self.KNOWN.get(text, ()):
                    continue
                rendered = transliterate(text, scheme)
                if fold(rendered, script=key) != fold(text):
                    misses.append((text, rendered))
        assert not misses

    def test_the_known_misses_still_miss(self) -> None:
        """If one starts folding, take it out of KNOWN and out of the gaps."""
        for text, scheme_ids in self.KNOWN.items():
            for scheme_id in scheme_ids:
                key = scheme_id.partition("/")[0]
                assert fold(transliterate(text, scheme_id), script=key) != fold(text), scheme_id


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
        """ISO 9985 j is ձ; with no hint and no ISO mark in the text it would
        fold as ALA-LC's ջ."""
        assert fold("Jayn", scheme="iso_9985") == fold("Ձայն")
        assert fold("Jayn", script="hy") != fold("Ձայն")

    def test_a_reversible_scheme_hint_works_for_georgian(self) -> None:
        assert fold("Mc'xet'a", scheme="ka/iso_9984_1996") == fold("მცხეთა")
        assert fold("Mtskheta", scheme="ka/iso_9984") == fold("მცხეთა")

    def test_separators_are_gone_before_the_digraphs_are_merged(self) -> None:
        """ISO 9984:2026's middle dot and ALA-LC 2022's soft sign."""
        for latin, georgian in (("t·s", "თს"), ("d·z", "დზ"), ("z·h", "ზჰ")):
            assert fold(latin, script="ka") == fold(georgian)
        assert fold("krtʹser", script="hy") == fold("կրտսեր")

    def test_a_presentation_ligature_is_not_dropped(self) -> None:
        """ﬕայն (only) once folded to the key of այն (that)."""
        assert fold("ﬕայն") == fold("միայն") != fold("այն")

    def test_a_lossy_scheme_hint_is_ignored(self) -> None:
        assert fold("Yerevan", scheme="bgn_pcgn") == fold("Yerevan", script="hy")

    def test_a_hint_is_ignored_for_script_input(self) -> None:
        assert fold("Երևան", scheme="iso_9985") == fold("Երևան")

    def test_a_classical_initial_ye_needs_no_hint(self) -> None:
        """Yesu is Յեսու under ISO 9985 and Հեսու under the reform: one key either way."""
        assert fold("Yesu", scheme="iso_9985") == fold("Յեսու") == fold("Հեսու")
        assert fold("Yesu", script="hy") == fold("Յեսու") == fold("Esu", script="hy")

    def test_a_hint_reaches_the_latin_tokens_of_a_mixed_line(self) -> None:
        """Token by token: the Armenian is folded as it is, the Latin read back."""
        assert fold("Ձայն Jayn", scheme="iso_9985") == "cayn cayn"
        assert fold("Jayn Ձայն 1985", scheme="iso_9985") == "cayn cayn 1985"

    def test_a_hint_for_another_script_names_that_script(self) -> None:
        with pytest.raises(UnknownSchemeError, match="for Georgian \\(ka\\); its schemes"):
            fold("x", script="ka", scheme="iso_9985")

    def test_the_georgian_f_folds_with_its_iso_rendering(self) -> None:
        """ჶ is f in ISO 9984 and undefined in ALA-LC; the fold takes ISO's side."""
        assert fold("ჶილმი") == fold("filmi", script="ka") == "filmi"
        assert fold(transliterate("ჶილმი", "ka/iso_9984"), script="ka") == fold("ჶილმი")


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
        # German spellings: z is զ in every scheme, j is ջ, tsch is տ+շ.
        assert fold("Eriwan", script="hy") != fold("Երևան")
        assert fold("Jerewan", script="hy") != fold("Երևան")
        assert fold("Tscharenz", script="hy") != fold("Չարենց")
        assert fold("Chatschaturjan", script="hy") != fold("Խաչատրյան")
        assert fold("Tiflis", script="ka") != fold("თბილისი")
        assert fold("George", script="ka") != fold("გიორგი")

    def test_declares_the_known_over_merges(self) -> None:
        """Different words that share a key, documented in docs/fold.md. If one
        of these starts failing, move the pair into the different-names test
        and out of the gaps."""
        # իւր (his) and հուր (fire): initial y becomes h.
        assert fold("իւր") == fold("հուր")
        assert fold("iwr", script="hy") == fold("Hur", script="hy")
        # The initials Յ. and Հ.: the lone initial goes the way of the glide.
        assert fold("Յ.") == fold("Հ.")
        assert fold("Ḥ.", script="hy") == fold("H.", script="hy") == fold("Յ.")
        # ivo is io for every input: a real v between i and o goes too.
        assert fold("Livorno", script="hy") == fold("Լիվոռնո") == fold("Liorno", script="hy")
        # An initial հե shares a key with an initial ե, since a Latin ye is
        # both the classical յե and BGN/PCGN's initial ե.
        assert fold("Հեթում") == fold("Hetum", script="hy") == fold("Etum", script="hy")
