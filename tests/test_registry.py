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
from tetrak_translit.registry import PACKAGES, scripts_in


def test_two_scripts_in_order() -> None:
    assert [script.key for script in scripts()] == ["hy", "ka"]


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
def test_every_letter_is_in_the_ranges(package) -> None:  # type: ignore[no-untyped-def]
    script = package.script
    for letter in script.letters + script.archaic:
        assert script.is_letter(letter), f"{script.key}: {letter!r} is outside the ranges"
        assert letter == letter.lower()


def test_qualified_ids_are_unique_and_prefixed() -> None:
    for scheme_id, scheme in SCHEMES.items():
        assert scheme_id == f"{scheme.script.key}/{scheme.key}"


class TestGetScript:
    @pytest.mark.parametrize("name", ["hy", "HY", "Armenian", "armenian"])
    def test_by_key_or_name(self, name: str) -> None:
        assert get_script(name).script.key == "hy"

    def test_by_object(self) -> None:
        script = get_script("ka").script
        assert get_script(script).script is script

    def test_unknown(self) -> None:
        with pytest.raises(UnknownScriptError, match="known scripts"):
            get_script("syr")


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

    def test_a_unique_key_needs_nothing(self) -> None:
        assert get_scheme("national").id == "ka/national"
        assert get_scheme("western").id == "hy/western"

    def test_an_ambiguous_key_names_the_choices(self) -> None:
        with pytest.raises(UnknownSchemeError, match="hy/ala_lc, ka/ala_lc"):
            get_scheme("ala_lc")
        with pytest.raises(UnknownSchemeError, match="hy/ala_lc, ka/ala_lc"):
            get_scheme("ala_lc", text="Tbilisi")

    def test_unknown(self) -> None:
        with pytest.raises(UnknownSchemeError, match="known schemes"):
            get_scheme("wade_giles")
        with pytest.raises(UnknownSchemeError):
            get_scheme("western", "ka")


def test_schemes_lists_all_or_one_script() -> None:
    assert [s.id for s in schemes()] == list(SCHEMES)
    assert [s.key for s in schemes("ka")] == ["ala_lc", "iso_9984", "national"]


def test_scripts_in() -> None:
    assert [p.script.key for p in scripts_in("Երևան და თბილისი")] == ["hy", "ka"]
    assert scripts_in("Tbilisi") == []
