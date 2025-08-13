"""Safety policies for the self‑editing agent.

This module defines rules that constrain what the agent is allowed to do.
Policies include restrictions on which files may be read or modified, size
limits on proposed patches, and limits on the number of steps or amount of
time the agent can spend on a single goal.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Iterable, List

from .. import config


# Directories under the project root that the agent is allowed to modify.  The
# agent should never edit files outside of these paths.  Additional paths may
# be appended here by the user as needed.
ALLOWED_DIRS: List[Path] = [config.BASE_DIR]

# Patterns (glob style) that should never be modified.  Use these to protect
# configuration files, third party libraries, secrets, etc.
DISALLOWED_PATTERNS: List[str] = [
    "*/.git/*",
    "*/.venv/*",
    "*/node_modules/*",
    "*/__pycache__/*",
]

# Maximum number of bytes permitted in a single patch.  Large patches may
# indicate runaway edits and should be rejected.
MAX_PATCH_BYTES: int = 10_000


def is_path_allowed(path: Path) -> bool:
    """Return True if the given path is allowed to be read or modified."""
    try:
        abs_path = path.resolve()
    except Exception:
        return False
    # Ensure the path is inside one of the allowed directories
    if not any(abs_path.is_relative_to(allowed) for allowed in ALLOWED_DIRS):
        return False
    # Check against disallowed patterns
    for pattern in DISALLOWED_PATTERNS:
        if fnmatch.fnmatch(str(abs_path), pattern):
            return False
    return True


__all__ = ["ALLOWED_DIRS", "DISALLOWED_PATTERNS", "MAX_PATCH_BYTES", "is_path_allowed"]
