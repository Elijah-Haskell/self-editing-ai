"""Wrapper around pytest for evaluating proposed changes.

This module defines a helper function to run the project's test suite in a
subprocess.  The agent uses this to determine whether a candidate edit has
improved or broken the code.  Test output is captured so that the agent can
analyse failures and make informed revisions.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Tuple

import logging

from .. import config

logger = logging.getLogger(__name__)

def run_tests(test_path: str | Path = "tests", timeout: int | None = None) -> Tuple[bool, str]:
    """
    Run the project's test suite and return a tuple of (passed, output).

    The preferred runner is ``pytest``.  If pytest is not available, a
    fallback to Python's built-in ``unittest`` discovery is used.  Output from
    the chosen test runner is captured and returned for analysis.

    :param test_path: directory or file to pass to the test runner
    :param timeout: optional timeout in seconds; defaults to config.TEST_TIMEOUT
    :returns: a tuple `(passed, output)` where `passed` is True if all tests
              succeeded, and `output` is the combined stdout/stderr from the
              test run.
    """
    timeout = timeout or config.TEST_TIMEOUT
    python_exe = sys.executable
    # Prefer pytest if available; otherwise skip tests gracefully.
    try:
        import pytest  # noqa: F401  # attempt to import to detect availability
    except ImportError:
        # pytest is not installed in this environment.  Skip running tests.
        msg = "pytest is not available; skipping tests"
        logger.warning(msg)
        return False, msg
    # Run pytest on the specified test path
    cmd = [python_exe, "-m", "pytest", str(test_path), "-q"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.error("test run timed out after %s seconds", timeout)
        return False, f"Timeout after {timeout} seconds"
    passed = result.returncode == 0
    output = (result.stdout or "") + (result.stderr or "")
    return passed, output

__all__ = ["run_tests"]
