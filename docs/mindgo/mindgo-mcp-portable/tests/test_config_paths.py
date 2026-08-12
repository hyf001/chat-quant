from __future__ import annotations

from pathlib import Path

import pytest

from supermind_mcp.config import resolve_config
from supermind_mcp.errors import ConfigError, PathSafetyError
from supermind_mcp.paths import join_remote_path, normalize_remote_path, safe_local_target


def test_resolve_config_uses_arguments_over_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JUPYTER_URL", "https://env.example")
    monkeypatch.setenv("JUPYTER_TOKEN", "env-token")

    config = resolve_config(url="https://arg.example/", token="arg-token")

    assert config.url == "https://arg.example"
    assert config.token == "arg-token"


def test_resolve_config_requires_url_and_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JUPYTER_URL", raising=False)
    monkeypatch.delenv("JUPYTER_TOKEN", raising=False)

    with pytest.raises(ConfigError, match="Jupyter URL not provided"):
        resolve_config()

    with pytest.raises(ConfigError, match="Jupyter token not provided"):
        resolve_config(url="https://example.test")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("", ""),
        (".", ""),
        ("project//data", "project/data"),
        ("project/./data", "project/data"),
        ("project\\data", "project/data"),
    ],
)
def test_normalize_remote_path(raw: str, expected: str) -> None:
    assert normalize_remote_path(raw) == expected


@pytest.mark.parametrize("raw", ["/absolute", "../secret", "project/../../secret"])
def test_normalize_remote_path_rejects_unsafe_paths(raw: str) -> None:
    with pytest.raises(PathSafetyError):
        normalize_remote_path(raw)


def test_join_remote_path_validates_result() -> None:
    assert join_remote_path("project", "data/file.csv") == "project/data/file.csv"
    with pytest.raises(PathSafetyError):
        join_remote_path("project", "../data")


def test_safe_local_target_keeps_path_inside_base(tmp_path: Path) -> None:
    assert safe_local_target(tmp_path, "data/result.csv") == tmp_path / "data/result.csv"

    with pytest.raises(PathSafetyError):
        safe_local_target(tmp_path, "../outside.csv")
