"""The command line, driven through main() rather than a subprocess."""

from __future__ import annotations

import io
import json

import pytest

from tetrak_translit.cli import main


def run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str, str]:
    status = main(list(argv))
    captured = capsys.readouterr()
    return status, captured.out, captured.err


class TestDetect:
    def test_plain(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "detect", "Երեւան", "Yerevan")
        assert status == 0
        assert out.splitlines() == ["armenian (classical)\tԵրեւան", "latin\tYerevan"]

    def test_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "detect", "--json", "Երևան")
        record = json.loads(out)
        assert status == 0
        assert record["text"] == "Երևան"
        assert record["orthography"] == "reformed"

    def test_reads_stdin_when_no_text_given(
        self, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("sys.stdin", io.StringIO("Երևան\nYerevan\n"))
        status, out, _ = run(capsys, "detect")
        assert status == 0
        assert len(out.splitlines()) == 2


class TestTransliterate:
    def test_default_scheme(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert run(capsys, "transliterate", "Երևան") == (0, "Erevan\n", "")

    def test_named_scheme_and_direction(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert run(capsys, "transliterate", "-s", "bgn_pcgn", "Երևան")[1] == "Yerevan\n"
        assert (
            run(capsys, "transliterate", "-s", "iso_9985", "--to", "armenian", "Erewan")[1]
            == "Երևան\n"
        )

    def test_unknown_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, err = run(capsys, "transliterate", "-s", "nope", "Երևան")
        assert status == 2 and out == "" and "unknown scheme" in err

    def test_irreversible_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "transliterate", "-s", "ala_lc", "--to", "armenian", "Erevan")
        assert status == 2 and "not reversible" in err


class TestFold:
    def test_folds_each_argument(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "fold", "Boghossian", "Պօղոսեան")
        assert status == 0
        assert out.splitlines() == ["poghosian", "poghosian"]

    def test_scheme_hint(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "fold", "-s", "iso_9985", "Jowkn")
        assert status == 0 and out.strip() == run(capsys, "fold", "Ձուկն")[1].strip()

    def test_unknown_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "fold", "-s", "nope", "x")
        assert status == 2 and "unknown scheme" in err


class TestSchemes:
    def test_lists_every_scheme(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "schemes")
        assert status == 0
        for key in ("ala_lc", "iso_9985", "bgn_pcgn", "hubschmann_meillet", "western"):
            assert key in out

    def test_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "schemes", "--json")
        rows = json.loads(out)
        assert status == 0
        assert {row["key"] for row in rows} >= {"ala_lc", "iso_9985"}
        assert all(
            {"name", "version", "standard", "reversible", "notes"} <= set(row) for row in rows
        )


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.startswith("tetrak-translit ")
