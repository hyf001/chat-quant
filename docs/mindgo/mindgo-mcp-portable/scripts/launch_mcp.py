#!/usr/bin/env python3
"""Load the bundle-local .env safely and replace this process with the MCP server."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ALLOWED_ENV_KEYS = {
    "JUPYTER_URL",
    "JUPYTER_TOKEN",
    "JUPYTER_AUTH_SCHEME",
    "MINDGO_INTRADAY_NOTEBOOK_PATH",
}


def load_env_file(path: Path, base: dict[str, str] | None = None) -> dict[str, str]:
    """Load simple KEY=VALUE entries; existing process variables take precedence."""

    original = dict(base if base is not None else os.environ)
    loaded: dict[str, str] = {}
    if path.exists():
        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), start=1
        ):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].lstrip()
            if "=" not in line:
                raise ValueError(f"Invalid .env line {line_number}: expected KEY=VALUE")
            key, value = line.split("=", 1)
            key = key.strip()
            if key not in ALLOWED_ENV_KEYS:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            loaded[key] = value
    return {**loaded, **original}


def bundle_root() -> Path:
    return Path(__file__).resolve().parents[1]


def server_command(root: Path) -> list[str]:
    if os.name == "nt":
        executable = root / ".venv" / "Scripts" / "supermind-mcp.exe"
    else:
        executable = root / ".venv" / "bin" / "supermind-mcp"
    if executable.exists():
        return [str(executable)]
    return [sys.executable, "-m", "supermind_mcp.server"]


def main() -> None:
    root = bundle_root()
    try:
        environment = load_env_file(root / ".env")
    except (OSError, ValueError) as exc:
        print(f"Cannot load {root / '.env'}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    command = server_command(root)
    os.chdir(root)
    os.execvpe(command[0], command, environment)


if __name__ == "__main__":
    main()
