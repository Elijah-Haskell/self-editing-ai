# Self‑Editing AI

This repository contains a **self‑editing autonomous agent** written in Python.  It is designed to read a user‑specified goal, plan a set of code edits to achieve that goal, apply those edits to its own codebase, run tests, and decide whether to accept or revert its changes.  All of this happens in a controlled loop with strict safety policies, giving the agent the ability to improve itself while remaining within predefined boundaries.

## Features

* **Planner/Editor/Reviewer loop** – the agent breaks down a high level goal into concrete edit tasks, generates unified diff patches (preferring AST manipulations when possible), applies them, runs the test suite, and evaluates the results before committing or reverting.
* **Persistent memory** – goals, actions and rationales are stored in a SQLite database.  A simple vector store (via FAISS) is provided for semantic search over past conversations and code embeddings.
* **Modular tools** – web search, file IO, test execution and code embedding are encapsulated in the `agent.tools` module.  Additional tools can be registered by editing this module.
* **Safety policies** – the agent enforces file allow/deny lists, step budgets and timeout budgets.  These guardrails prevent it from modifying sensitive files, spending unbounded time, or making irreversible changes.
* **CLI interface** – run the agent from the command line with a goal, or integrate it into your own scripts.  Example entry points can be found in `scripts/`.

## Getting started

### Prerequisites

* Python 3.10 or later.
* An OpenAI API key exported in your environment (if you plan to use language models).  The agent will look for `OPENAI_API_KEY` in its environment.  Without an API key the core loop will still run but certain functions (e.g. search or code generation) will raise `NotImplementedError`.

### Installation

Clone this repository and install the dependencies:

```
git clone https://example.com/self_editing_ai.git
cd self_editing_ai
pip install -e .
```

The `-e` (editable) flag installs the package in development mode so that the agent can modify its own source files.

### Usage

You can run the agent against a goal via the CLI:

```
python -m src.cli --goal "Add a web search tool"
```

The agent will run a planning/editing/testing/reviewing loop until the goal is satisfied or a step budget is exhausted.  Logs and rationales will be written to the SQLite memory at the path specified in `config.py`.

Scripts in the `scripts/` directory provide additional entry points: e.g. `scripts/run_loop.py` demonstrates how to seed the memory and invoke the loop programmatically.

## Project structure

```
self_editing_ai/
├── README.md           # This file
├── pyproject.toml      # Build specification and dependencies
├── src/
│   ├── agent/
│   │   ├── __init__.py        # Package initialization
│   │   ├── loop.py            # Main planner/editor/tester loop
│   │   ├── tools.py           # Tool implementations (web search, file IO, etc.)
│   │   ├── memory.py          # SQLite and vector store interfaces
│   │   ├── edits.py           # AST and diff editing utilities
│   │   ├── tests_runner.py    # Wrapper around pytest
│   │   └── policies.py        # Safety policies and allow/deny lists
│   ├── cli.py          # Command line interface for running the agent
│   ├── config.py       # Global configuration variables
│   └── prompts/
│       ├── planner.md  # Prompt for the planner LLM
│       ├── editor.md   # Prompt for the editor LLM
│       └── reviewer.md # Prompt for the reviewer LLM
├── tests/
│   ├── test_smoke.py   # Sanity checks for the package
│   └── test_self_edits.py # Example tests for self‑editing behaviour
├── scripts/
│   ├── seed_memory.py  # Example script to seed the memory database
│   └── run_loop.py     # Example script to run the agent loop from Python
├── docker/
│   ├── Dockerfile      # Container specification for running the agent
│   └── docker-compose.yml # Compose file for local development
└── .gitignore
```

## Contributing

Contributions are welcome!  Feel free to open an issue or submit a pull request if you find a bug or have a suggestion for improvement.  Please include tests for any new features.
