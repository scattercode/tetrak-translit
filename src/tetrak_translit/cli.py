"""Command-line interface: ``tetrak-translit``.

Four subcommands, mirroring the four public functions::

    tetrak-translit detect "Երեւան" "თბილისი"
    tetrak-translit transliterate --scheme ala_lc "Երևան"
    tetrak-translit transliterate --scheme iso_9984 --to script "T'bilisi"
    tetrak-translit fold --script hy "Boghossian" "Պօղոսեան"
    tetrak-translit schemes

Each takes its text as arguments or, when none are given, one string per
line on standard input -- so a column of catalogue titles can be piped
through. ``--json`` emits one JSON object per line for the commands whose
result has structure.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable, Iterator

from . import __version__
from .detect import detect
from .engine import NotReversibleError
from .fold import ScriptRequiredError, fold
from .registry import PACKAGES, UnknownSchemeError, UnknownScriptError
from .transliterate import transliterate

_USER_ERRORS = (UnknownSchemeError, UnknownScriptError, NotReversibleError, ScriptRequiredError)


def _inputs(texts: list[str]) -> Iterator[str]:
    """The texts given, or else the lines on standard input."""
    if texts:
        yield from texts
        return
    for line in sys.stdin:
        yield line.rstrip("\n")


def _emit(lines: Iterable[str]) -> int:
    try:
        for line in lines:
            print(line)
    except _USER_ERRORS as error:
        message = error.args[0] if error.args else str(error)
        print(f"tetrak-translit: {message}", file=sys.stderr)
        return 2
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    def lines() -> Iterator[str]:
        for text in _inputs(args.text):
            found = detect(text)
            if args.json:
                yield json.dumps({"text": text, **found.as_dict()}, ensure_ascii=False)
            else:
                orthography = f" ({found.orthography})" if found.orthography else ""
                marks = "".join(
                    f" [{r.key} marks: {', '.join(r.marks)}{'' if r.distinctive else ', shared'}]"
                    for r in found.romanisations
                )
                yield f"{found.script}{orthography}{marks}\t{text}"

    return _emit(lines())


def _cmd_transliterate(args: argparse.Namespace) -> int:
    return _emit(
        transliterate(
            text, args.scheme, script=args.script, to=args.to, orthography=args.orthography
        )
        for text in _inputs(args.text)
    )


def _cmd_fold(args: argparse.Namespace) -> int:
    return _emit(fold(text, script=args.script, scheme=args.scheme) for text in _inputs(args.text))


def _cmd_schemes(args: argparse.Namespace) -> int:
    if args.json:
        rows = [
            {
                "id": scheme.id,
                "script": scheme.script.key,
                "key": scheme.key,
                "name": scheme.name,
                "version": scheme.version,
                "standard": scheme.standard,
                "reversible": scheme.reversible,
                "notes": scheme.notes,
            }
            for package in PACKAGES.values()
            for scheme in package.schemes.values()
        ]
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for package in PACKAGES.values():
        print(f"{package.script.name} ({package.script.key})")
        width = max(len(scheme.id) for scheme in package.schemes.values())
        for scheme in package.schemes.values():
            reversible = "reversible" if scheme.reversible else "lossy"
            print(f"  {scheme.id:<{width}}  {scheme.name} v{scheme.version}, {reversible}")
            print(f"  {'':<{width}}  {scheme.standard}")
    return 0


def _add_script_flag(parser: argparse.ArgumentParser, help_text: str) -> None:
    parser.add_argument("-S", "--script", default=None, help=help_text)


def build_parser() -> argparse.ArgumentParser:
    """The ``tetrak-translit`` argument parser."""
    parser = argparse.ArgumentParser(
        prog="tetrak-translit",
        description="Detect, transliterate and fold Armenian, Georgian, Russian and Syriac text.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    detect_parser = commands.add_parser(
        "detect",
        help="say which script a string is in, for Armenian which orthography, "
        "and which romanisation marks a Latin value carries",
    )
    detect_parser.add_argument("text", nargs="*", help="text to examine; stdin lines if omitted")
    detect_parser.add_argument("--json", action="store_true", help="one JSON object per line")
    detect_parser.set_defaults(func=_cmd_detect)

    transliterate_parser = commands.add_parser(
        "transliterate", help="render a script in a romanisation scheme, or read one back"
    )
    transliterate_parser.add_argument(
        "text", nargs="*", help="text to transliterate; stdin lines if omitted"
    )
    transliterate_parser.add_argument(
        "-s",
        "--scheme",
        default="ala_lc",
        help="romanisation scheme, optionally qualified: ala_lc, ka/iso_9984 "
        "(default: ala_lc; see `tetrak-translit schemes`)",
    )
    _add_script_flag(
        transliterate_parser,
        "the script (hy, ka, ru, syr) when the text and the scheme key do not settle it",
    )
    transliterate_parser.add_argument(
        "--to",
        default="latin",
        help="direction: latin (default), script, or a script key such as hy or ka "
        "(reading back works for reversible schemes only)",
    )
    transliterate_parser.add_argument(
        "--orthography",
        choices=("classical", "reformed"),
        default=None,
        help="the Armenian orthography, for ALA-LC's classical-only rules "
        "(default: detected from each line)",
    )
    transliterate_parser.set_defaults(func=_cmd_transliterate)

    fold_parser = commands.add_parser(
        "fold", help="map any spelling onto the canonical index form, for matching"
    )
    fold_parser.add_argument("text", nargs="*", help="text to fold; stdin lines if omitted")
    _add_script_flag(fold_parser, "the script whose rules Latin text gets (hy, ka, ru, syr)")
    fold_parser.add_argument(
        "-s",
        "--scheme",
        default=None,
        help="the reversible scheme the Latin input is written in, if known",
    )
    fold_parser.set_defaults(func=_cmd_fold)

    schemes_parser = commands.add_parser("schemes", help="list the romanisation schemes")
    schemes_parser.add_argument("--json", action="store_true", help="as JSON")
    schemes_parser.set_defaults(func=_cmd_schemes)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns the exit status rather than calling ``sys.exit``."""
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
