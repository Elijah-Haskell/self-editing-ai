"""Utilities for generating and applying code edits.

This module centralises logic related to diff creation and application.  The
agent may propose changes to its own source files as unified diffs or via
higher‑level AST transformations.  Helper functions here abstract away the
mechanics of creating diff strings and applying them to files.
"""

from __future__ import annotations

import difflib
import logging
from pathlib import Path
from typing import Iterable, List

logger = logging.getLogger(__name__)


def generate_unified_diff(
    original: str, updated: str, filename: str, context: int = 3
) -> str:
    """Generate a unified diff between two versions of a file.

    :param original: original file contents
    :param updated: updated file contents
    :param filename: the filename to embed in the diff header
    :param context: number of context lines to include on either side of changes
    :returns: a unified diff string
    """
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=filename,
        tofile=filename,
        n=context,
    )
    return "".join(diff)


def apply_unified_diff(original: str, diff: str) -> str:
    """Apply a unified diff to the original text.

    This function attempts to apply a unified diff and returns the modified
    content.  It uses a simple third‑party patch library if available.  If
    applying the patch fails, a ``RuntimeError`` is raised.

    :param original: original file contents
    :param diff: unified diff string
    :returns: updated file contents after applying the diff
    :raises NotImplementedError: if no patching backend is available
    :raises RuntimeError: if the patch could not be applied cleanly
    """
    try:
        import patch  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise NotImplementedError(
            "The 'patch' library is required to apply unified diffs."
        ) from exc
    pset = patch.fromstring(diff)
    if pset is None:
        raise RuntimeError("Failed to parse unified diff")
    # The patch library expects a dict of filename->content
    # Use a dummy name since unified diffs embed the filename
    patched = pset.apply({"dummy": original})
    if not patched:
        raise RuntimeError("Failed to apply patch")
    return patched["dummy"]


def propose_ast_edit(original: str, instructions: str) -> str:
    """Propose an AST‑level edit for the given code based on instructions.

    This is a placeholder for AST‑based editing.  In a real implementation
    you might parse the Python abstract syntax tree using the ``ast`` module,
    traverse it, and perform modifications.  For now this function raises
    ``NotImplementedError`` to indicate that AST editing is not yet available.
    """
    raise NotImplementedError(
        "AST editing is not implemented.  Please implement propose_ast_edit() in edits.py."
    )


__all__ = ["generate_unified_diff", "apply_unified_diff", "propose_ast_edit"]
