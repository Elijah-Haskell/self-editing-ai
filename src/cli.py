"""Command line interface for the self‑editing AI agent.

This module exposes a simple entry point that can be run with
``python -m src.cli --goal "<your goal>"``.  It instantiates the agent
memory, prepares any required directories, and runs the agent loop.
"""

from __future__ import annotations

import argparse
import logging

from . import config
from .agent.loop import AgentLoop
from .agent.memory import Memory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the self‑editing AI agent")
    parser.add_argument(
        "--goal",
        type=str,
        required=True,
        help="Goal or objective for the agent to accomplish",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Maximum number of iterations before giving up",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    # Configure logging to stdout
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    # Ensure required directories exist
    config.ensure_directories()
    # Initialise memory
    memory = Memory()
    loop = AgentLoop(memory=memory)
    loop.run(goal=args.goal, max_steps=args.max_steps)


if __name__ == "__main__":  # pragma: no cover
    main()
