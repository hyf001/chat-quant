from __future__ import annotations

import json
import sys
from pathlib import Path

DEFAULTS = {
    "database_path": "data/chat-quant.db",
    "api_host": "127.0.0.1",
    "api_port": 12345,
    "web_host": "127.0.0.1",
    "web_port": 12346,
}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: read-runtime-config.py <key>")
    key = sys.argv[1]
    if key not in DEFAULTS:
        raise SystemExit(f"unknown config key: {key}")
    payload = _load_config()
    value = payload.get(key, DEFAULTS[key])
    if key.endswith("_port"):
        value = _coerce_port(value, int(DEFAULTS[key]))
    elif isinstance(value, str):
        value = value.strip() or DEFAULTS[key]
    print(value)


def _load_config() -> dict[str, object]:
    config_path = Path("config.json")
    if not config_path.exists():
        return {}
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _coerce_port(value: object, default: int) -> int:
    try:
        port = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default
    return port if 0 < port <= 65535 else default


if __name__ == "__main__":
    main()
