"""The canonical fold: one index form for every spelling of a word.

This is the function a search index calls, at index time and at query
time, so that a record catalogued as ``Պօղոսեան`` is found by a reader who
types *Poghosyan*, *Boghossian*, *Pōghosean* or ``Պողոսյան``, and one
catalogued as ``ჭავჭავაძე`` by *Chavchavadze*, *Čavčavaje* or
*Ch'avch'avadze*. It is for **finding**, not display: the key it returns
is a deliberately coarse Latin skeleton that nobody should ever show to a
reader. The schemes are for display; this is the other half of the job,
and the two must not be confused.

Each script owns its rules -- :mod:`tetrak_translit.hy.fold` and
:mod:`tetrak_translit.ka.fold` -- because what should be merged differs
between scripts. This module only decides which rules a token gets: a
token in a registered script gets that script's; a Latin token gets the
rules of the script named by ``script=``, because *Tbilisi* folded under
Armenian rules would never find ``თბილისი``.
"""

from __future__ import annotations

import re
import unicodedata

from . import engine
from .registry import PACKAGES, ScriptPackage, get_scheme, get_script, scripts_in
from .script import Scheme, Script

_TOKEN = re.compile(r"\S+")


class ScriptRequiredError(ValueError):
    """Raised when Latin text is folded with no script to fold it for."""


def _package_for(token: str, default: ScriptPackage | None) -> ScriptPackage:
    present = scripts_in(token)
    if present:
        # One token in two scripts is a typo or a homoglyph; the first
        # registered script wins, and the key is still deterministic.
        return present[0]
    if default is None:
        choices = ", ".join(
            f"script={key!r} ({package.script.name})" for key, package in PACKAGES.items()
        )
        raise ScriptRequiredError(
            f"fold() needs to know which script's rules to apply to Latin text: pass {choices}"
        )
    return default


def fold_token(token: str, script: str | Script | None = None) -> str:
    """Fold one whitespace-free token. Empty when nothing survives."""
    default = get_script(script) if script is not None else None
    return _package_for(token, default).fold_token(token, None)


def fold(
    text: str, *, script: str | Script | None = None, scheme: str | Scheme | None = None
) -> str:
    """Fold *text* onto its canonical index form.

    Args:
        text: Text in a registered script, Latin in any of its
            romanisations, or a mixture. Tokens are folded one at a time
            and joined with single spaces.
        script: Which script's rules Latin tokens get: a key (``"hy"``,
            ``"ka"``) or name. Tokens written in a registered script are
            recognised regardless. Required if any token is Latin.
        scheme: Optional. When the Latin in *text* is known to be written
            in a reversible scheme (``"iso_9985"``, ``"hubschmann_meillet"``,
            ``"ka/iso_9984"``), name it and each Latin token is read back
            into the script exactly before folding, which removes the
            ambiguities the heuristic fold has (Armenian ``j``, when nothing
            else in the text shows the scheme). Tokens already in the
            script are folded as they are, so a mixed line gets the hint
            for its Latin tokens. For a lossy scheme the heuristic fold is
            used. Either way the scheme's script becomes the default for
            Latin tokens.

    Returns:
        A lowercase ASCII key: for comparing and indexing, never for
        display.

    Raises:
        ScriptRequiredError: a Latin token and no *script*.
        UnknownScriptError, UnknownSchemeError: the names resolve to nothing.
    """
    text = unicodedata.normalize("NFC", text)
    default = get_script(script) if script is not None else None
    table: Scheme | None = None
    if scheme is not None:
        table = get_scheme(scheme, default.script if default else None)
        default = get_script(table.script)
        if not table.reversible:
            table = None

    def prepare(token: str) -> str:
        if table is not None and not table.script.has_letters(token):
            return engine.read(token, table)
        return token

    tokens = (prepare(match.group()) for match in _TOKEN.finditer(text))
    keys = (_package_for(token, default).fold_token(token, text) for token in tokens)
    return " ".join(key for key in keys if key)


__all__ = ["ScriptRequiredError", "fold", "fold_token"]
