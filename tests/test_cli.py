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
        status, out, _ = run(capsys, "detect", "Երեւան", "Yerevan", "თბილისი")
        assert status == 0
        assert out.splitlines() == [
            "armenian (classical)\tԵրեւան",
            "latin\tYerevan",
            "georgian\tთბილისი",
        ]

    def test_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "detect", "--json", "Երևան")
        record = json.loads(out)
        assert status == 0
        assert record["text"] == "Երևան"
        assert record["key"] == "hy"
        assert record["orthography"] == "reformed"

    def test_reads_stdin_when_no_text_given(
        self, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("sys.stdin", io.StringIO("Երևան\nYerevan\n"))
        status, out, _ = run(capsys, "detect")
        assert status == 0
        assert len(out.splitlines()) == 2


class TestTransliterate:
    def test_default_scheme_follows_the_text(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert run(capsys, "transliterate", "Երևան") == (0, "Erevan\n", "")
        assert run(capsys, "transliterate", "თბილისი") == (0, "tʻbilisi\n", "")

    def test_named_scheme_and_direction(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert run(capsys, "transliterate", "-s", "bgn_pcgn", "Երևան")[1] == "Yerevan\n"
        assert run(capsys, "transliterate", "-s", "national", "თბილისი")[1] == "tbilisi\n"
        assert (
            run(capsys, "transliterate", "-s", "iso_9985", "--to", "armenian", "Erewan")[1]
            == "Երևան\n"
        )
        assert (
            run(capsys, "transliterate", "-s", "iso_9984", "--to", "script", "T'bilisi")[1]
            == "თბილისი\n"
        )

    def test_script_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert (
            run(capsys, "transliterate", "-s", "ala_lc", "-S", "ka", "თბილისი")[1] == "tʻbilisi\n"
        )

    def test_unknown_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, err = run(capsys, "transliterate", "-s", "nope", "Երևան")
        assert status == 2 and out == "" and "unknown scheme" in err

    def test_ambiguous_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "transliterate", "-s", "ala_lc", "--to", "script", "Erevan")
        assert status == 2 and "say which" in err

    def test_irreversible_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "transliterate", "-s", "hy/ala_lc", "--to", "script", "Erevan")
        assert status == 2 and "not reversible" in err


class TestFold:
    def test_folds_each_argument(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "fold", "-S", "hy", "Boghossian", "Պօղոսեան")
        assert status == 0
        assert out.splitlines() == ["poghosian", "poghosian"]

    def test_georgian(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "fold", "--script", "ka", "Chavchavadze", "ჭავჭავაძე")
        assert status == 0
        assert len(set(out.splitlines())) == 1

    def test_scheme_hint(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "fold", "-s", "iso_9985", "Jowkn")
        assert status == 0 and out.strip() == run(capsys, "fold", "Ձուկն")[1].strip()

    def test_latin_without_a_script_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "fold", "Tbilisi")
        assert status == 2 and "script" in err

    def test_unknown_scheme_fails_cleanly(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, _, err = run(capsys, "fold", "-s", "nope", "x")
        assert status == 2 and "unknown scheme" in err


class TestSchemes:
    def test_lists_every_scheme_under_its_script(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "schemes")
        assert status == 0
        assert out.startswith("Armenian (hy)")
        for scheme_id in (
            "hy/ala_lc",
            "hy/iso_9985",
            "hy/western",
            "ka/ala_lc",
            "ka/iso_9984",
            "ka/national",
        ):
            assert scheme_id in out

    def test_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        status, out, _ = run(capsys, "schemes", "--json")
        rows = json.loads(out)
        assert status == 0
        assert {row["id"] for row in rows} >= {"hy/ala_lc", "ka/iso_9984"}
        assert all(
            {"id", "script", "key", "name", "version", "standard", "reversible", "notes"}
            <= set(row)
            for row in rows
        )


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.startswith("tetrak-translit ")
