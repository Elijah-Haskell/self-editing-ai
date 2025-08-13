"""Example script to run the agent loop from Python code.

Usage:

.. code-block:: bash

    python -m scripts.run_loop --goal "Fix failing tests"

This script instantiates the agent memory, ensures directories exist, and
runs the agent loop for the given goal.  It is a thin wrapper around
``self_editing_ai.src.cli`` but may be easier to customise for programmatic
use.
"""

from __future__ import annotations

import argparse
import logging

from self_editing_ai.src import config
from self_editing_ai.src.agent.loop import AgentLoop
from self_editing_ai.src.agent.memory import Memory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the self‑editing AI agent loop")
    parser.add_argument(
        "--goal",
        type=str,
        required=True,
        help="Goal for the agent to accomplish",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Maximum number of iterations before stopping",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    config.ensure_directories()
    memory = Memory()
    agent = AgentLoop(memory=memory)
    agent.run(goal=args.goal, max_steps=args.max_steps)


if __name__ == "__main__":  # pragma: no cover
    main()
