"""Basic tests for memory and test runner functionality."""

from pathlib import Path

from self_editing_ai.src.agent.memory import Memory
from self_editing_ai.src.agent.tests_runner import run_tests



def test_memory_append_and_fetch(tmp_path: Path) -> None:
    db_path = tmp_path / "memory.sqlite3"
    mem = Memory(db_path)
    mem.append_message("user", "hello", metadata={"foo": 1})
    mem.append_message("assistant", "world", metadata={})
    messages = mem.all_messages()
    assert len(messages) == 2
    assert messages[0][1] == "user"
    assert messages[0][2] == "hello"
    assert messages[0][3]["foo"] == 1
    assert messages[1][1] == "assistant"



def test_run_tests_smoke() -> None:
    passed, output = run_tests()
    # The test suite should at least run and produce output; we don't assert pass/fail
    assert isinstance(passed, bool)
    assert isinstance(output, str)
