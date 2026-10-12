"""Transliterate between a script and its named Latin schemes.

The public face of :mod:`tetrak_translit.engine`: it resolves which
scheme, of which script, the caller means, then hands over. A scheme
key alone (``"ala_lc"``) is enough when the text says which script it is
in; when it does not -- reading Latin back, or a key several scripts
define -- say so with ``script=`` or a qualified key (``"ka/ala_lc"``).
"""

from __future__ import annotations

from . import engine
from .engine import NotReversibleError
from .registry import UnknownSchemeError, UnknownScriptError, get_scheme, get_script
from .script import Scheme, Script


def to_latin(
    text: str,
    scheme: str | Scheme = "ala_lc",
    script: str | Script | None = None,
    orthography: str | None = None,
) -> str:
    """Render the script in *text* through *scheme*, leaving the rest alone.

    *orthography* is for the schemes with rules that hold in one
    orthography only (ALA-LC writes a classical word-initial ``յ`` as
    ``ḥ``). Left as ``None``, the script's detector decides from *text*
    itself, and an *indeterminate* verdict applies none of those rules.
    """
    resolved = get_scheme(scheme, script, text)
    if orthography is None and any(rule.variant for rule in resolved.rules):
        orthography = get_script(resolved.script).variant(text)
    return engine.render(text, resolved, orthography)


def to_script(text: str, scheme: str | Scheme, script: str | Script | None = None) -> str:
    """Read Latin written in *scheme* back into its script.

    Raises:
        NotReversibleError: *scheme* is lossy and cannot be reversed.
    """
    return engine.read(text, get_scheme(scheme, script))


def to_armenian(text: str, scheme: str | Scheme) -> str:
    """Read Latin written in an Armenian *scheme* back into Armenian."""
    return to_script(text, scheme, "hy")


def transliterate(
    text: str,
    scheme: str | Scheme = "ala_lc",
    *,
    script: str | Script | None = None,
    to: str = "latin",
    orthography: str | None = None,
) -> str:
    """Transliterate *text* between a script and *scheme*.

    Args:
        text: The text. For ``to="latin"`` the script's letters in it are
            rendered and everything else is passed through; otherwise the
            whole string is read as Latin in *scheme*.
        scheme: A scheme key (``"ala_lc"``, ``"iso_9985"``, ``"bgn_pcgn"``,
            ``"hubschmann_meillet"``, ``"western"`` for Armenian;
            ``"ala_lc"``, ``"iso_9984"``, ``"national"`` for Georgian),
            optionally qualified with the script (``"ka/ala_lc"``), or a
            :class:`Scheme`.
        script: Which script, when the text and the key do not settle it:
            a key (``"hy"``, ``"ka"``) or name (``"Armenian"``).
        to: ``"latin"`` (the default); ``"script"`` to read Latin back; or
            a script key or name, which reads back into that script.
        orthography: For Armenian, ``"classical"`` or ``"reformed"``,
            when rendering through a scheme whose rules depend on it
            (ALA-LC). By default it is detected from *text*; a short
            string with no tell is *indeterminate* and gets none of the
            orthography-specific rules, so say so when you know.

    Returns:
        The transliterated string.

    Raises:
        UnknownSchemeError: *scheme* names no table, or tables in several
            scripts with nothing to choose between them.
        UnknownScriptError: *script* or *to* names no script.
        NotReversibleError: reading back through a lossy scheme.
    """
    if to == "latin":
        return to_latin(text, scheme, script, orthography)
    if to == "script":
        return to_script(text, scheme, script)
    return to_script(text, scheme, get_script(to).script)


__all__ = [
    "NotReversibleError",
    "UnknownSchemeError",
    "UnknownScriptError",
    "get_scheme",
    "to_armenian",
    "to_latin",
    "to_script",
    "transliterate",
]
