"""The scripts this package handles, and how to find the one a string is in.

A script package exports five names -- ``SCRIPT``, ``SCHEMES``,
``fold_token``, ``variant`` and ``MARKS`` -- and is registered here. Everything
above this module (detection, transliteration, the fold, the command
line) goes through the registry and never names a script directly, which
is what keeps a new script a matter of adding a package.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from . import hy, ka, ru
from .script import RomanisationMark, Scheme, Script


class UnknownScriptError(KeyError):
    """Raised when a script key or name names no registered script."""


class UnknownSchemeError(KeyError):
    """Raised when a scheme key names no table, or names tables in several scripts."""


@dataclass(frozen=True)
class ScriptPackage:
    """What one script package contributes."""

    script: Script
    schemes: dict[str, Scheme]
    #: Folds one whitespace-free token; the second argument is the whole
    #: text it came from, or ``None``, for the rules that look beyond it.
    fold_token: Callable[[str, str | None], str]
    variant: Callable[[str], str | None]
    #: The signs that a Latin value is a romanisation of this script.
    marks: tuple[RomanisationMark, ...] = ()


#: Every registered script, by key, in documentation order.
PACKAGES: dict[str, ScriptPackage] = {
    package.script.key: package
    for package in (
        ScriptPackage(hy.SCRIPT, dict(hy.SCHEMES), hy.fold_token, hy.variant, hy.MARKS),
        ScriptPackage(ka.SCRIPT, dict(ka.SCHEMES), ka.fold_token, ka.variant, ka.MARKS),
        ScriptPackage(ru.SCRIPT, dict(ru.SCHEMES), ru.fold_token, ru.variant, ru.MARKS),
    )
}

#: Every scheme across every script, by fully qualified id (``"hy/ala_lc"``).
SCHEMES: dict[str, Scheme] = {
    scheme.id: scheme for package in PACKAGES.values() for scheme in package.schemes.values()
}


def get_script(script: str | Script) -> ScriptPackage:
    """Resolve a script key (``"hy"``), name (``"Armenian"``) or :class:`Script`.

    Raises:
        UnknownScriptError: nothing registered matches.
    """
    if isinstance(script, Script):
        wanted = script.key
    else:
        wanted = script.strip().lower()
    for key, package in PACKAGES.items():
        if wanted in (key, package.script.name.lower(), package.script.unicode_name):
            return package
    known = ", ".join(f"{key} ({package.script.name})" for key, package in PACKAGES.items())
    raise UnknownScriptError(f"unknown script {script!r}; known scripts: {known}")


def scripts_in(text: str) -> list[ScriptPackage]:
    """The registered scripts whose letters occur in *text*, in registry order."""
    return [package for package in PACKAGES.values() if package.script.has_letters(text)]


def _normalise_key(scheme: str) -> str:
    return scheme.strip().lower().replace("-", "_").replace(" ", "_")


def get_scheme(
    scheme: str | Scheme, script: str | Script | None = None, text: str | None = None
) -> Scheme:
    """Resolve a scheme by key, choosing the script it belongs to.

    The script is taken, in order, from: a qualified key
    (``"ka/ala_lc"``), the *script* argument, the one registered script
    whose letters occur in *text*, or the one registered script that has
    a scheme of that key. A key that several scripts define, with nothing
    to choose between them, is an error that names the choices.

    Raises:
        UnknownSchemeError: no table matches, or several do.
        UnknownScriptError: *script* or the key's prefix names no script.
    """
    if isinstance(scheme, Scheme):
        return scheme
    key = _normalise_key(scheme)
    if "/" in key:
        prefix, _, key = key.partition("/")
        script = prefix

    candidates: list[ScriptPackage]
    if script is not None:
        candidates = [get_script(script)]
    else:
        candidates = list(PACKAGES.values())
        if text is not None:
            present = scripts_in(text)
            if len(present) == 1:
                candidates = present

    matches = [package.schemes[key] for package in candidates if key in package.schemes]
    if len(matches) == 1:
        return matches[0]
    if not matches and script is not None:
        package = candidates[0]
        known = ", ".join(package.schemes)
        raise UnknownSchemeError(
            f"unknown scheme {scheme!r} for {package.script.name} ({package.script.key}); "
            f"its schemes: {known}"
        )
    if not matches:
        known = ", ".join(SCHEMES)
        raise UnknownSchemeError(f"unknown scheme {scheme!r}; known schemes: {known}")
    ids = ", ".join(match.id for match in matches)
    raise UnknownSchemeError(
        f"scheme {scheme!r} exists for more than one script ({ids}); "
        f"say which with script= or a qualified key such as {matches[0].id!r}"
    )


__all__ = [
    "PACKAGES",
    "SCHEMES",
    "ScriptPackage",
    "UnknownSchemeError",
    "UnknownScriptError",
    "get_scheme",
    "get_script",
    "scripts_in",
]
