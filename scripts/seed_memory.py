"""Seed the memory database with example entries.

Run this script with ``python -m scripts.seed_memory`` to add some initial
messages to the memory database.  This can be useful for bootstrapping the
agent with prior context or sample conversations.
"""

from __future__ import annotations

import logging

from self_editing_ai.src.agent.memory import Memory
from self_editing_ai.src import config


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    mem = Memory()
    mem.append_message("system", "Seed: initial system prompt", metadata={"type": "seed"})
    mem.append_message("user", "Seed: hello", metadata={"type": "seed"})
    mem.append_message("assistant", "Seed: world", metadata={"type": "seed"})
    logging.info("Seeded memory database at %s", mem.db_path)


if __name__ == "__main__":  # pragma: no cover
    main()
