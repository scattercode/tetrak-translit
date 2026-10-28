"""The registry: every script package keeps the contract the engine relies on."""

from __future__ import annotations

import pytest

from tetrak_translit import (
    SCHEMES,
    UnknownSchemeError,
    UnknownScriptError,
    get_scheme,
    get_script,
    schemes,
    scripts,
)
from tetrak_translit.registry import PACKAGES, ScriptPackage, scripts_in


def test_four_scripts_in_order() -> None:
    assert [script.key for script in scripts()] == ["hy", "ka", "ru", "syr"]


def test_script_ranges_do_not_overlap() -> None:
    """A code point in two scripts would make detection depend on registry order."""
    seen: dict[int, str] = {}
    for package in PACKAGES.values():
        for low, high in package.script.ranges:
            for code in range(low, high + 1):
                assert code not in seen, (
                    f"U+{code:04X} is in {seen.get(code)} and {package.script.key}"
                )
                seen[code] = package.script.key


@pytest.mark.parametrize("package", PACKAGES.values(), ids=lambda p: p.script.key)
def test_every_letter_is_in_the_ranges(package: ScriptPackage) -> None:
    script = package.script
    for letter in script.letters + script.archaic:
        assert script.is_letter(letter), f"{script.key}: {letter!r} is outside the ranges"
        assert letter == letter.lower()


def test_syriac_signs_and_punctuation_are_not_letters() -> None:
    """The vowel points are units a scheme renders; rukkākā and the rest are marks."""
    script = PACKAGES["syr"].script
    assert script.is_letter("\u0710") and script.is_letter("\u073f")
    assert not script.is_letter("\u0742")  # rukkākā
    assert not script.is_letter("\u0700")  # end of paragraph
    assert "\u0742" in script.marks and "\u0308" in script.marks


def test_punctuation_inside_a_block_is_not_a_letter() -> None:
    """The Georgian paragraph separator sits between two runs of letters."""
    assert not PACKAGES["ka"].script.is_letter("\u10fb")
    assert PACKAGES["ka"].script.is_letter("\u10fa") and PACKAGES["ka"].script.is_letter("\u10fc")


def test_qualified_ids_are_unique_and_prefixed() -> None:
    for scheme_id, scheme in SCHEMES.items():
        assert scheme_id == f"{scheme.script.key}/{scheme.key}"


class TestGetScript:
    @pytest.mark.parametrize("name", ["hy", "HY", "Armenian", "armenian"])
    def test_by_key_or_name(self, name: str) -> None:
        assert get_script(name).script.key == "hy"

    @pytest.mark.parametrize("name", ["syr", "Syriac", "syriac"])
    def test_syriac_by_key_or_name(self, name: str) -> None:
        assert get_script(name).script.key == "syr"

    @pytest.mark.parametrize("name", ["ru", "Russian", "cyrillic"])
    def test_russian_by_key_name_or_unicode_name(self, name: str) -> None:
        assert get_script(name).script.key == "ru"

    def test_by_object(self) -> None:
        script = get_script("ka").script
        assert get_script(script).script is script

    def test_unknown(self) -> None:
        with pytest.raises(UnknownScriptError, match="known scripts"):
            get_script("cop")


class TestGetScheme:
    def test_qualified_key(self) -> None:
        assert get_scheme("ka/ala_lc").id == "ka/ala_lc"
        assert get_scheme("hy/ala_lc").id == "hy/ala_lc"

    def test_script_argument(self) -> None:
        assert get_scheme("ala_lc", "ka").id == "ka/ala_lc"
        assert get_scheme("ALA-LC", "Georgian").id == "ka/ala_lc"

    def test_text_settles_it(self) -> None:
        assert get_scheme("ala_lc", text="თბილისი").id == "ka/ala_lc"
        assert get_scheme("ala_lc", text="Երևան").id == "hy/ala_lc"
        assert get_scheme("bgn_pcgn", text="Екатеринбург").id == "ru/bgn_pcgn"
        assert get_scheme("ala_lc", text="ܟܬܒܐ").id == "syr/ala_lc"

    def test_a_unique_key_needs_nothing(self) -> None:
        assert get_scheme("national").id == "ka/national"
        assert get_scheme("western").id == "hy/western"

    def test_an_ambiguous_key_names_the_choices(self) -> None:
        with pytest.raises(UnknownSchemeError, match="hy/ala_lc, ka/ala_lc, ru/ala_lc, syr/ala_lc"):
            get_scheme("ala_lc")
        with pytest.raises(UnknownSchemeError, match="hy/bgn_pcgn, ru/bgn_pcgn"):
            get_scheme("bgn_pcgn")
        with pytest.raises(UnknownSchemeError, match="hy/ala_lc, ka/ala_lc"):
            get_scheme("ala_lc", text="Tbilisi")

    def test_unknown(self) -> None:
        with pytest.raises(UnknownSchemeError, match="known schemes"):
            get_scheme("wade_giles")

    def test_unknown_for_the_script_named_lists_that_scripts_schemes(self) -> None:
        with pytest.raises(UnknownSchemeError, match=r"for Georgian \(ka\); its schemes: ala_lc"):
            get_scheme("western", "ka")


def test_schemes_lists_all_or_one_script() -> None:
    assert [s.id for s in schemes()] == list(SCHEMES)
    assert [s.key for s in schemes("ka")] == ["ala_lc", "iso_9984", "iso_9984_1996", "national"]


def test_scripts_in() -> None:
    assert [p.script.key for p in scripts_in("Երևան და თბილისი")] == ["hy", "ka"]
    assert [p.script.key for p in scripts_in("Ереван, Երևան")] == ["hy", "ru"]
    assert scripts_in("Tbilisi") == []
