"""Command-line interface: ``tetrak-translit``.

Four subcommands, mirroring the four public functions::

    tetrak-translit detect "Երեւան"
    tetrak-translit transliterate --scheme ala_lc "Երևան"
    tetrak-translit transliterate --scheme iso_9985 --to armenian "Erewan"
    tetrak-translit fold "Boghossian" "Պօղոսեան"
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
from .fold import fold
from .schemes import SCHEMES
from .transliterate import NotReversibleError, UnknownSchemeError, transliterate


def _inputs(texts: list[str]) -> Iterator[str]:
    """The texts given, or else the lines on standard input."""
    if texts:
        yield from texts
        return
    for line in sys.stdin:
        yield line.rstrip("\n")


def _emit(lines: Iterable[str]) -> int:
    for line in lines:
        print(line)
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    def lines() -> Iterator[str]:
        for text in _inputs(args.text):
            found = detect(text)
            if args.json:
                yield json.dumps({"text": text, **found.as_dict()}, ensure_ascii=False)
            else:
                orthography = f" ({found.orthography})" if found.orthography else ""
                yield f"{found.script}{orthography}\t{text}"

    return _emit(lines())


def _cmd_transliterate(args: argparse.Namespace) -> int:
    try:
        return _emit(transliterate(text, args.scheme, to=args.to) for text in _inputs(args.text))
    except (UnknownSchemeError, NotReversibleError) as error:
        print(f"tetrak-translit: {error}", file=sys.stderr)
        return 2


def _cmd_fold(args: argparse.Namespace) -> int:
    try:
        return _emit(fold(text, args.scheme) for text in _inputs(args.text))
    except UnknownSchemeError as error:
        print(f"tetrak-translit: {error}", file=sys.stderr)
        return 2


def _cmd_schemes(args: argparse.Namespace) -> int:
    if args.json:
        rows = [
            {
                "key": scheme.key,
                "name": scheme.name,
                "version": scheme.version,
                "standard": scheme.standard,
                "reversible": scheme.reversible,
                "notes": scheme.notes,
            }
            for scheme in SCHEMES.values()
        ]
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    width = max(len(key) for key in SCHEMES)
    for scheme in SCHEMES.values():
        reversible = "reversible" if scheme.reversible else "lossy"
        print(f"{scheme.key:<{width}}  {scheme.name} v{scheme.version}, {reversible}")
        print(f"{'':<{width}}  {scheme.standard}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """The ``tetrak-translit`` argument parser."""
    parser = argparse.ArgumentParser(
        prog="tetrak-translit",
        description="Detect, transliterate and fold Armenian text.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    detect_parser = commands.add_parser(
        "detect", help="say which script a string is in and, for Armenian, which orthography"
    )
    detect_parser.add_argument("text", nargs="*", help="text to examine; stdin lines if omitted")
    detect_parser.add_argument("--json", action="store_true", help="one JSON object per line")
    detect_parser.set_defaults(func=_cmd_detect)

    transliterate_parser = commands.add_parser(
        "transliterate", help="render Armenian in a romanisation scheme, or read one back"
    )
    transliterate_parser.add_argument(
        "text", nargs="*", help="text to transliterate; stdin lines if omitted"
    )
    transliterate_parser.add_argument(
        "-s",
        "--scheme",
        default="ala_lc",
        help="romanisation scheme (default: ala_lc; see `tetrak-translit schemes`)",
    )
    transliterate_parser.add_argument(
        "--to",
        choices=("latin", "armenian"),
        default="latin",
        help="direction (default: latin; armenian only for reversible schemes)",
    )
    transliterate_parser.set_defaults(func=_cmd_transliterate)

    fold_parser = commands.add_parser(
        "fold", help="map any spelling onto the canonical index form, for matching"
    )
    fold_parser.add_argument("text", nargs="*", help="text to fold; stdin lines if omitted")
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
