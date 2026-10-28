#!/usr/bin/env python
"""Probe tetrak-translit: render a text through every scheme, or trace a fold.

Purpose
    Two things that are tedious by hand while working on a table or a fold:

    render  For each text, print what ``detect()`` says, every scheme's
            rendering of it, and its fold key. Latin text needs ``--script``
            for the fold, exactly as ``fold()`` does; a reversible scheme's
            read-back is shown when ``--scheme`` is given.
    trace   For each token, print the fold step by step -- the orthography or
            archaic-letter normalisation, the ALA-LC rendering, the output of
            ``clean()``, and every Latin rule that changed the token -- so the
            step at which two spellings part company is visible. Ends by saying
            whether all the tokens reached one key.

Prerequisites
    The repository's own interpreter, from the repository root, so the
    development install of ``tetrak_translit`` is the one imported:

        .venv/bin/python .claude/skills/tetrak-translit-extending/scripts/probe.py render "Երևան" "თბილისი"
        .venv/bin/python .claude/skills/tetrak-translit-extending/scripts/probe.py trace --script hy Պօղոսեան Boghossian Poghosyan
        .venv/bin/python .claude/skills/tetrak-translit-extending/scripts/probe.py trace --scheme iso_9985 Jowkn Ձուկն

    ``trace`` reads private names from the script packages' fold modules
    (``_ORTHOGRAPHY``, ``_ARCHAIC``, ``_LETTERS``, ``_LATIN``) and compares its
    result with the public ``fold_token()``. A mismatch means the fold module
    changed shape and this script needs updating; the library is the truth.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from types import ModuleType

import tetrak_translit as tt
from tetrak_translit import engine, latin
from tetrak_translit.registry import ScriptPackage, get_scheme, get_script, scripts_in


def _package_for(token: str, default: str | None) -> ScriptPackage | None:
    present = scripts_in(token)
    if present:
        return present[0]
    return get_script(default) if default else None


def cmd_render(args: argparse.Namespace) -> int:
    status = 0
    for text in args.text:
        found = tt.detect(text)
        print(f"{text}")
        print(f"  detect     script={found.script} key={found.key} orthography={found.orthography}")
        key = found.key or args.script
        if found.key:
            for scheme in tt.schemes(found.key):
                print(f"  {scheme.id:<22} {tt.transliterate(text, scheme)}")
        if args.scheme:
            scheme = get_scheme(args.scheme, key)
            if scheme.reversible:
                print(f"  read back ({scheme.id})  {tt.transliterate(text, scheme, to='script')}")
            else:
                print(f"  read back ({scheme.id})  not reversible")
        try:
            print(f"  fold       {tt.fold(text, script=key, scheme=args.scheme)}")
        except tt.ScriptRequiredError:
            print("  fold       (Latin text: pass --script hy or --script ka)")
            status = 2
        print()
    return status


def _trace_token(token: str, package: ScriptPackage, module: ModuleType) -> str:
    print(f"{token}")
    work = token
    if package.script.has_letters(work):
        work = work.lower()
        rules = getattr(module, "_ORTHOGRAPHY", None)
        if rules is not None:
            normalised = latin.apply(work, rules)
            if normalised != work:
                print(f"  orthography   {normalised}")
            work = normalised
        archaic = getattr(module, "_ARCHAIC", None)
        if archaic is not None:
            modern = work.translate(archaic)
            if modern != work:
                print(f"  archaic       {modern}")
            work = modern
        # A fold that freezes its own table (Armenian's _BASIS) renders
        # through that; otherwise through the display ALA-LC table.
        work = engine.render(work, getattr(module, "_BASIS", None) or module.ALA_LC)
        print(f"  ala_lc        {work}")
    cleaned = latin.clean(work, getattr(module, "_LETTERS", {}))
    print(f"  clean         {cleaned}")
    work = cleaned
    # A fold with rules for Latin spellings only (Syriac's) gives script
    # tokens its _SKELETON instead.
    skeleton = getattr(module, "_SKELETON", None)
    rules = (
        skeleton if skeleton is not None and package.script.has_letters(token) else module._LATIN
    )
    for pattern, replacement in rules:
        changed = pattern.sub(replacement, work)
        if changed != work:
            shown = changed.replace("\x01", "\u2401")  # make the placeholder visible
            print(f"  {pattern.pattern:<13} {shown}")
            work = changed
    public = package.fold_token(token)
    flag = "" if public == work else f"   !! fold_token() says {public!r}; this script is stale"
    print(f"  key           {work}{flag}")
    return public


def cmd_trace(args: argparse.Namespace) -> int:
    default = args.script
    tokens = list(args.token)
    if args.scheme:
        scheme = get_scheme(args.scheme, default)
        default = scheme.script.key
        if scheme.reversible:
            tokens = [
                engine.read(token, scheme) if not scheme.script.has_letters(token) else token
                for token in tokens
            ]
            print(f"(Latin read back through {scheme.id} first: {' '.join(tokens)})\n")
    keys: list[str] = []
    for token in tokens:
        package = _package_for(token, default)
        if package is None:
            print(f"{token}\n  Latin text: pass --script hy or --script ka\n")
            return 2
        module = importlib.import_module(f"tetrak_translit.{package.script.key}.fold")
        keys.append(_trace_token(token, package, module))
        print()
    if len(keys) > 1:
        verdict = "one key" if len(set(keys)) == 1 else f"{len(set(keys))} different keys"
        print(f"=> {verdict}: {', '.join(sorted(set(keys)))}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render through every scheme, or trace a fold.")
    commands = parser.add_subparsers(dest="command", required=True)

    render = commands.add_parser("render", help="every scheme's rendering, detection and fold key")
    render.add_argument("text", nargs="+")
    render.add_argument("-S", "--script", help="script for Latin text (hy, ka, ru, syr)")
    render.add_argument("-s", "--scheme", help="also read back through this scheme if reversible")
    render.set_defaults(func=cmd_render)

    trace = commands.add_parser("trace", help="the fold, rule by rule, for one or more tokens")
    trace.add_argument("token", nargs="+", help="whitespace-free tokens to fold")
    trace.add_argument(
        "-S", "--script", help="script whose rules Latin tokens get (hy, ka, ru, syr)"
    )
    trace.add_argument("-s", "--scheme", help="reversible scheme the Latin is written in")
    trace.set_defaults(func=cmd_trace)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
