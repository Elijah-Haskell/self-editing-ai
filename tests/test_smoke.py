"""Smoke tests for the self‑editing AI package."""

def test_import_package() -> None:
    import importlib
    pkg = importlib.import_module("self_editing_ai")
    assert pkg is not None


def test_import_cli() -> None:
    import importlib
    cli = importlib.import_module("self_editing_ai.src.cli")
    assert hasattr(cli, "main")
