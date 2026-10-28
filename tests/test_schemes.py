"""Every table covers its alphabet, and says what it is."""

from __future__ import annotations

import pytest

from tetrak_translit import SCHEMES, Scheme, Script, hy, ka, ru, syr
from tetrak_translit.engine import render
from tetrak_translit.script import Rule


def test_armenian_has_thirty_eight_letters() -> None:
    assert len(hy.SCRIPT.letters) == 38
    assert hy.SCRIPT.letters[0] == "ա" and hy.SCRIPT.letters[-1] == "ֆ"


def test_georgian_has_thirty_three_letters_and_fourteen_others() -> None:
    assert len(ka.SCRIPT.letters) == 33
    assert ka.SCRIPT.letters[0] == "ა" and ka.SCRIPT.letters[-1] == "ჰ"
    assert ka.SCRIPT.archaic == "ჱჲჳჴჵჶჷჸჹჺჼჽჾჿ"
    assert not ka.SCRIPT.cased


def test_russian_has_thirty_three_letters_and_the_four_the_reform_removed() -> None:
    assert len(ru.SCRIPT.letters) == 33
    assert ru.SCRIPT.letters[0] == "а" and ru.SCRIPT.letters[-1] == "я"
    assert ru.SCRIPT.archaic == "іѣѳѵ"
    assert ru.SCRIPT.cased


def test_syriac_has_twenty_two_letters_and_sixteen_points() -> None:
    assert len(syr.SCRIPT.letters) == 22
    assert syr.SCRIPT.letters[0] == "ܐ" and syr.SCRIPT.letters[-1] == "ܬ"
    assert len(syr.descriptor.POINTS) == 16
    assert not syr.SCRIPT.cased


@pytest.mark.parametrize("scheme", SCHEMES.values(), ids=lambda s: s.id)
class TestEveryScheme:
    def test_covers_every_letter_and_digraph(self, scheme: Scheme) -> None:
        assert set(scheme.script.letters) <= set(scheme.letters)
        assert set(scheme.script.digraphs) <= set(scheme.digraphs)

    def test_renders_nothing_empty(self, scheme: Scheme) -> None:
        for unit, latin in {**scheme.letters, **scheme.digraphs, **scheme.initial}.items():
            assert latin, f"{scheme.id} renders {unit!r} as nothing"

    def test_is_described(self, scheme: Scheme) -> None:
        assert scheme.name and scheme.version and scheme.standard and scheme.notes
        assert scheme.key == scheme.key.lower()

    def test_renders_only_ascii_plus_marks(self, scheme: Scheme) -> None:
        """A rendering is Latin letters plus the scheme's marks: no stray script."""
        for latin in scheme.letters.values():
            assert all(not scheme.script.is_letter(c) for c in latin)


@pytest.mark.parametrize(
    "scheme", [s for s in SCHEMES.values() if s.reversible], ids=lambda s: s.id
)
def test_reversible_schemes_are_one_to_one(scheme: Scheme) -> None:
    renderings = (
        list(scheme.letters.values())
        + [scheme.digraphs[d] for d in scheme.script.digraphs]
        + [latin for latin in scheme.punctuation.values() if latin]
    )
    assert len(renderings) == len(set(renderings))


def test_lossy_schemes_are_declared_lossy() -> None:
    assert SCHEMES["hy/ala_lc"].reversible is False
    assert SCHEMES["hy/ala_lc"].letters["ժ"] == "zh"  # also զ + հ, which 2022 leaves unmarked
    assert SCHEMES["ka/ala_lc"].reversible is False
    assert SCHEMES["ka/ala_lc"].letters["ძ"] == "dz"  # also დ + ზ
    assert SCHEMES["ka/national"].reversible is False
    assert SCHEMES["ru/ala_lc"].reversible is False
    assert SCHEMES["ru/ala_lc"].letters["щ"] == "shch"  # also ш + ч
    assert SCHEMES["ru/bgn_pcgn"].reversible is False
    assert SCHEMES["syr/ala_lc"].reversible is False


def test_the_two_georgian_apostrophe_conventions_are_opposite() -> None:
    """ALA-LC marks the aspirate, the national system the ejective."""
    assert SCHEMES["ka/ala_lc"].letters["თ"].endswith("ʻ")
    assert SCHEMES["ka/ala_lc"].letters["ტ"] == "t"
    assert SCHEMES["ka/national"].letters["თ"] == "t"
    assert SCHEMES["ka/national"].letters["ტ"] == "t'"


class TestSchemeValidation:
    SCRIPT = Script("xx", "Test", "test", "ab", archaic="c", digraphs=("ab",), ranges=((97, 99),))

    def table(self, **overrides: object) -> dict[str, object]:
        base: dict[str, object] = dict(
            script=self.SCRIPT,
            key="t",
            name="T",
            version="0",
            standard="none",
            reversible=False,
            letters={"a": "a", "b": "b"},
            digraphs={"ab": "ab"},
        )
        return {**base, **overrides}

    def test_a_complete_table_is_accepted(self) -> None:
        Scheme(**self.table())  # type: ignore[arg-type]
        Scheme(**self.table(letters={"a": "a", "b": "b", "c": "c"}))  # type: ignore[arg-type]

    def test_a_missing_letter_is_refused(self) -> None:
        with pytest.raises(ValueError, match="missing"):
            Scheme(**self.table(letters={"a": "a"}))  # type: ignore[arg-type]

    def test_a_stray_key_is_refused(self) -> None:
        with pytest.raises(ValueError, match="outside the script"):
            Scheme(**self.table(letters={"a": "a", "b": "b", "q": "q"}))  # type: ignore[arg-type]

    def test_a_missing_digraph_is_refused(self) -> None:
        with pytest.raises(ValueError, match="does not render"):
            Scheme(**self.table(digraphs={}))  # type: ignore[arg-type]

    def test_a_positional_rule_on_an_unknown_unit_is_refused(self) -> None:
        with pytest.raises(ValueError, match="unknown units"):
            Scheme(**self.table(initial={"q": "q"}))  # type: ignore[arg-type]


class TestFinalRule:
    """A rule that holds only at the end of a word, as ALA-LC Syriac drops a
    final alaph that carries its vowel."""

    SCRIPT = Script("xx", "Test", "test", "abc", marks="!", ranges=((97, 99),))
    SCHEME = Scheme(
        script=SCRIPT,
        key="t",
        name="T",
        version="0",
        standard="none",
        reversible=False,
        letters={"a": "a", "b": "bʾ", "c": "c"},
        rules=(Rule("b", "b", final=True),),
    )

    def test_applies_only_at_the_end_of_a_word(self) -> None:
        assert render("bab cab", self.SCHEME) == "bʾab cab"

    def test_a_one_letter_word_is_initial_and_final(self) -> None:
        assert render("b", self.SCHEME) == "b"

    def test_a_mark_after_the_last_letter_does_not_stop_it(self) -> None:
        assert render("cab!", self.SCHEME) == "cab!"
        assert render("ca!b", self.SCHEME) == "ca!b"
        assert render("cb!a", self.SCHEME) == "cbʾ!a"
