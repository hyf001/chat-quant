"""Path normalization and containment checks."""

from __future__ import annotations

import posixpath
from pathlib import Path

from .errors import PathSafetyError


def normalize_remote_path(path: str | None) -> str:
    """Return a safe Jupyter relative path using POSIX separators."""

    raw = (path or "").replace("\\", "/").strip()
    if raw in {"", "."}:
        return ""
    if raw.startswith("/"):
        raise PathSafetyError("Remote path must be relative")
    if any(part == ".." for part in raw.split("/")):
        raise PathSafetyError("Remote path cannot contain '..'")

    normalized = posixpath.normpath(raw)
    if normalized in {"", "."}:
        return ""
    parts = [part for part in normalized.split("/") if part]
    if any(part == ".." for part in parts):
        raise PathSafetyError("Remote path cannot contain '..'")
    return "/".join(parts)


def join_remote_path(*parts: str | None) -> str:
    """Join remote path fragments and validate the result."""

    joined = "/".join(part.strip("/") for part in parts if part)
    return normalize_remote_path(joined)


def safe_local_target(base: str | Path, relative_path: str) -> Path:
    """Join a base directory with a relative path without escaping the base."""

    base_path = Path(base).expanduser().resolve()
    relative = normalize_remote_path(relative_path)
    target = (base_path / relative).resolve()

    if target != base_path and base_path not in target.parents:
        raise PathSafetyError("Local target escapes destination directory")
    return target
