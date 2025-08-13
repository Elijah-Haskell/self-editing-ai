"""Global configuration values for the self‑editing AI.

This module centralises configuration for the agent.  Many values can be
overridden via environment variables; defaults are provided here for
convenience.
"""

from __future__ import annotations

import os
from pathlib import Path


# Base directory of the project (the directory containing this file's parent).
BASE_DIR: Path = Path(__file__).resolve().parents[2]

# Path to the SQLite database used for persistent memory.
MEMORY_DB_PATH: Path = Path(
    os.getenv("SELF_EDITING_AI_MEMORY_DB", BASE_DIR / "memory.sqlite3")
)

# Path to the directory where vector store files are kept.  FAISS will create
# binary index and metadata files here.
VECTOR_STORE_DIR: Path = Path(
    os.getenv("SELF_EDITING_AI_VECTOR_STORE_DIR", BASE_DIR / "vector_store")
)

# Maximum number of steps the agent will take before giving up on a goal.
MAX_STEPS: int = int(os.getenv("SELF_EDITING_AI_MAX_STEPS", 20))

# Timeout (in seconds) for running tests.  If exceeded, the test runner will
# assume the patch introduced an infinite loop and revert.
TEST_TIMEOUT: int = int(os.getenv("SELF_EDITING_AI_TEST_TIMEOUT", 30))

# Model names or identifiers for the planner, editor and reviewer.  These
# environment variables should be set to valid OpenAI model names (e.g.
# "gpt-4") if you plan to use LLM‑based reasoning.  If left unset, the
# corresponding functions in `agent.tools` may raise NotImplementedError.
PLANNER_MODEL: str | None = os.getenv("SELF_EDITING_AI_PLANNER_MODEL")
EDITOR_MODEL: str | None = os.getenv("SELF_EDITING_AI_EDITOR_MODEL")
REVIEWER_MODEL: str | None = os.getenv("SELF_EDITING_AI_REVIEWER_MODEL")


def ensure_directories() -> None:
    """Create any directories referenced by configuration values if absent."""
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


__all__ = [
    "BASE_DIR",
    "MEMORY_DB_PATH",
    "VECTOR_STORE_DIR",
    "MAX_STEPS",
    "TEST_TIMEOUT",
    "PLANNER_MODEL",
    "EDITOR_MODEL",
    "REVIEWER_MODEL",
    "ensure_directories",
]
