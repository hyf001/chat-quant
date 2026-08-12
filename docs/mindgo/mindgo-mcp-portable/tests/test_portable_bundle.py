from __future__ import annotations

import importlib.util
from pathlib import Path

from supermind_mcp.intraday_realtime import DEFAULT_NOTEBOOK_PATH, _notebook_path


ROOT = Path(__file__).resolve().parents[1]


def load_launcher_module():
    spec = importlib.util.spec_from_file_location(
        "portable_launch_mcp", ROOT / "scripts" / "launch_mcp.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notebook_path_uses_environment_override(monkeypatch) -> None:
    monkeypatch.setenv("MINDGO_INTRADAY_NOTEBOOK_PATH", "/custom/path.ipynb/")
    assert _notebook_path() == "custom/path.ipynb"


def test_notebook_path_uses_default_for_blank_value(monkeypatch) -> None:
    monkeypatch.setenv("MINDGO_INTRADAY_NOTEBOOK_PATH", "  ")
    assert _notebook_path() == DEFAULT_NOTEBOOK_PATH


def test_env_loader_accepts_only_known_keys_and_preserves_process_env(tmp_path) -> None:
    launcher = load_launcher_module()
    env_file = tmp_path / ".env"
    env_file.write_text(
        "JUPYTER_URL=https://file.example\n"
        "JUPYTER_TOKEN='file-token'\n"
        "UNRELATED_SECRET=must-not-load\n",
        encoding="utf-8",
    )

    result = launcher.load_env_file(
        env_file,
        base={"JUPYTER_URL": "https://process.example", "PATH": "/bin"},
    )

    assert result["JUPYTER_URL"] == "https://process.example"
    assert result["JUPYTER_TOKEN"] == "file-token"
    assert result["PATH"] == "/bin"
    assert "UNRELATED_SECRET" not in result


def test_env_loader_rejects_malformed_lines(tmp_path) -> None:
    launcher = load_launcher_module()
    env_file = tmp_path / ".env"
    env_file.write_text("this-is-not-an-assignment\n", encoding="utf-8")

    try:
        launcher.load_env_file(env_file, base={})
    except ValueError as exc:
        assert "line 1" in str(exc)
    else:
        raise AssertionError("malformed .env line should fail")
