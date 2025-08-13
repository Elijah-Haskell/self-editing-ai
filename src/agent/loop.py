"""Main planning/editing/testing/reviewing loop for the agent.

This module defines ``AgentLoop``, a class responsible for orchestrating the
steps required to achieve a user‑provided goal.  The loop interacts with
memory, tools, and policies defined elsewhere in this package.  A minimal
implementation is provided here; users are expected to extend it with their
own planning and editing logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import logging

from .. import config
from .memory import Memory
from .tests_runner import run_tests
from .tools import read_file, write_file
from .policies import is_path_allowed


logger = logging.getLogger(__name__)


@dataclass
class AgentLoop:
    """Orchestrates the planning/editing/testing/reviewing loop."""

    memory: Memory

    def run(self, goal: str, max_steps: Optional[int] = None) -> None:
        """Run the agent loop to achieve the given goal.

        The current implementation logs the goal and stores it in memory,
        runs the test suite once, and exits.  You can extend this method
        with logic for planning edits, generating patches, applying them,
        running tests, evaluating results and iterating.

        :param goal: the user‑supplied objective
        :param max_steps: maximum number of iterations; defaults to config.MAX_STEPS
        """
        max_steps = max_steps or config.MAX_STEPS
        logger.info("Starting agent loop for goal: %s", goal)
        # Record the goal in memory
        self.memory.append_message("user", goal, metadata={"type": "goal"})
        # Example: run tests once before editing
        passed, output = run_tests()
        self.memory.append_message(
            "system",
            f"Initial test run {'passed' if passed else 'failed'}:\n{output}",
            metadata={"type": "test_result"},
        )
        # Log and print output for the user
        if passed:
            logger.info("All tests passed.  The code is currently healthy.")
        else:
            logger.warning("Tests failed.  Agent should plan edits to fix issues.")
        print(output)
        # Placeholder: user can implement planning and editing logic here
        logger.info(
            "AgentLoop.run() completed after 1 iteration.  Extend this method to implement planning/editing."
        )


__all__ = ["AgentLoop"]
