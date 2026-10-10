"""Every table covers the alphabet, and says what it is."""

from __future__ import annotations

import pytest

from tetrak_translit.schemes import ARMENIAN_LOWERCASE, DIGRAPHS, SCHEMES, Scheme


def test_the_alphabet_has_thirty_eight_letters() -> None:
    assert len(ARMENIAN_LOWERCASE) == 38
    assert ARMENIAN_LOWERCASE[0] == "ա" and ARMENIAN_LOWERCASE[-1] == "ֆ"


@pytest.mark.parametrize("scheme", SCHEMES.values(), ids=lambda s: s.key)
class TestEveryScheme:
    def test_covers_every_letter_and_both_digraphs(self, scheme: Scheme) -> None:
        assert set(scheme.letters) == set(ARMENIAN_LOWERCASE)
        assert set(DIGRAPHS) <= set(scheme.digraphs)

    def test_renders_nothing_empty(self, scheme: Scheme) -> None:
        for unit, latin in {**scheme.letters, **scheme.digraphs, **scheme.initial}.items():
            assert latin, f"{scheme.key} renders {unit!r} as nothing"

    def test_is_described(self, scheme: Scheme) -> None:
        assert scheme.name and scheme.version and scheme.standard and scheme.notes
        assert scheme.key == scheme.key.lower()

    def test_positional_rules_only_name_known_units(self, scheme: Scheme) -> None:
        known = set(scheme.letters) | set(scheme.digraphs)
        assert set(scheme.initial) <= known
        assert set(scheme.after_vowel) <= known


class TestReversibleSchemesAreOneToOne:
    """A reversible table must not render two units the same way."""

    @pytest.mark.parametrize(
        "scheme", [s for s in SCHEMES.values() if s.reversible], ids=lambda s: s.key
    )
    def test_no_two_units_share_a_rendering(self, scheme: Scheme) -> None:
        renderings = list(scheme.letters.values()) + [scheme.digraphs["և"]]
        assert len(renderings) == len(set(renderings))

    def test_ala_lc_is_declared_lossy(self) -> None:
        assert SCHEMES["ala_lc"].reversible is False
        # The reason: ts is ծ, and also տ followed by ս.
        assert SCHEMES["ala_lc"].letters["ծ"] == "ts"


class TestSchemeValidation:
    def test_a_missing_letter_is_refused(self) -> None:
        letters = dict(SCHEMES["ala_lc"].letters)
        del letters["ֆ"]
        with pytest.raises(ValueError, match="missing"):
            Scheme("x", "X", "0", "none", False, letters, {"ու": "u", "և": "ev"})

    def test_a_stray_key_is_refused(self) -> None:
        letters = {**SCHEMES["ala_lc"].letters, "q": "q"}
        with pytest.raises(ValueError, match="non-Armenian"):
            Scheme("x", "X", "0", "none", False, letters, {"ու": "u", "և": "ev"})

    def test_a_missing_digraph_is_refused(self) -> None:
        with pytest.raises(ValueError, match="does not render"):
            Scheme("x", "X", "0", "none", False, SCHEMES["ala_lc"].letters, {"ու": "u"})
