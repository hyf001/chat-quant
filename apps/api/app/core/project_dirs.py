from __future__ import annotations

import re
from pathlib import Path

_UNSAFE_PATH_CHARS = re.compile(r"[^A-Za-z0-9_.-]+")


def project_dir(project_home: str, project_id: str) -> str:
    return str(Path(project_home) / safe_project_dir_segment(project_id))


def safe_project_dir_segment(value: str) -> str:
    segment = _UNSAFE_PATH_CHARS.sub("_", value.strip())
    if segment in {"", ".", ".."}:
        return "local_project"
    return segment
