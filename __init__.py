"""Top‑level package for the self‑editing AI.

This file makes `self_editing_ai` a Python package and exposes a
convenience import for the `AgentLoop` class.
"""

from .src.agent.loop import AgentLoop  # noqa: F401

__all__ = ["AgentLoop"]
