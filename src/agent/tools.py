"""Utility functions and tool abstractions for the self‑editing agent.

These functions provide a thin wrapper around external capabilities such as
web search, file IO, code execution and embeddings.  By centralising access
here it becomes easy to audit and control what the agent is allowed to do.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List

import logging

from .. import config


logger = logging.getLogger(__name__)


def search_web(query: str, max_results: int = 5) -> List[str]:
    """Search the web for the given query and return a list of result snippets.

    This function is intentionally left as a stub because the environment in
    which this package runs may not have direct internet access.  To use web
    search, implement this function using an appropriate API (e.g. Google
    Custom Search, Bing Search, SerpAPI) or by calling out to `requests`.

    :param query: search query string
    :param max_results: maximum number of results to return
    :returns: list of result snippets or URLs
    :raises NotImplementedError: if no search implementation is configured
    """
    raise NotImplementedError(
        "Web search is not implemented.  Provide an implementation in agent.tools"
    )


def read_file(path: str | Path) -> str:
    """Read the contents of a text file.

    :param path: path to the file
    :returns: contents of the file as a string
    :raises FileNotFoundError: if the file does not exist
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str | Path, content: str) -> None:
    """Write the given content to a file, creating any parent directories.

    :param path: path to the file
    :param content: text content to write
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        f.write(content)


def run_python_file(path: str | Path, timeout: int = config.TEST_TIMEOUT) -> subprocess.CompletedProcess:
    """Execute a Python script and return the completed process object.

    This helper runs the script in a subprocess using the same Python
    interpreter that is running the agent.  It captures stdout and stderr and
    propagates the return code.  Use this for quick smoke tests or for
    evaluating changes made to the agent.

    :param path: path to the Python script to run
    :param timeout: maximum time (in seconds) to allow the script to run
    :returns: the ``subprocess.CompletedProcess`` instance
    """
    python_exe = sys.executable
    try:
        result = subprocess.run(
            [python_exe, str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result
    except subprocess.TimeoutExpired as e:
        logger.error("Script %s timed out after %s seconds", path, timeout)
        raise


def embed_texts(texts: Iterable[str]) -> List[List[float]]:
    """Compute embeddings for a list of texts.

    By default this function is a stub.  To enable embeddings, set up your
    environment with an OpenAI API key and implement a call to the OpenAI
    embedding endpoint or another embedding provider.  The returned list
    should contain one embedding (a list of floats) per input text.

    :param texts: an iterable of text strings
    :returns: a list of embedding vectors
    :raises NotImplementedError: if embeddings are not implemented
    """
    raise NotImplementedError(
        "Embedding not implemented.  Provide an implementation in agent.tools"
    )


__all__ = [
    "search_web",
    "read_file",
    "write_file",
    "run_python_file",
    "embed_texts",
]
