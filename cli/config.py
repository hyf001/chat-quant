from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

DEFAULT_API_BASE_URL = "http://127.0.0.1:12345/api"
RUNTIME_FILE_NAME = "api-runtime.json"
APP_SUPPORT_DIR_NAME = "chat-quant-desktop"


@dataclass(frozen=True)
class CliConfig:
    api_base_url: str = DEFAULT_API_BASE_URL


def get_config() -> CliConfig:
    env_api_base_url = _env_api_base_url()
    if env_api_base_url:
        return CliConfig(api_base_url=env_api_base_url)

    runtime_api_base_url = _runtime_api_base_url()
    if runtime_api_base_url and _is_api_healthy(runtime_api_base_url):
        return CliConfig(api_base_url=runtime_api_base_url)

    return CliConfig(
        api_base_url=DEFAULT_API_BASE_URL,
    )


def _env_api_base_url() -> str | None:
    api_base_url = os.environ.get("CHATQ_API_BASE_URL")
    if api_base_url:
        return _normalize_api_base_url(api_base_url)
    base_url = os.environ.get("CHATQ_API_BASE")
    if base_url:
        return _normalize_api_base_url(base_url)
    return None


def _runtime_api_base_url() -> str | None:
    runtime_file_path = _runtime_file_path()
    if not runtime_file_path.exists():
        return None
    try:
        payload = json.loads(runtime_file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    api_base_url = payload.get("api_base_url")
    if isinstance(api_base_url, str) and api_base_url.strip():
        return _normalize_api_base_url(api_base_url)
    base_url = payload.get("base_url")
    if isinstance(base_url, str) and base_url.strip():
        return _normalize_api_base_url(base_url)
    host = payload.get("host")
    port = payload.get("port")
    if isinstance(host, str) and isinstance(port, int):
        return _normalize_api_base_url(f"http://{host}:{port}")
    return None


def _runtime_file_path() -> Path:
    override = os.environ.get("CHATQ_API_RUNTIME_FILE")
    if override:
        return Path(override).expanduser()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_SUPPORT_DIR_NAME / RUNTIME_FILE_NAME
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / APP_SUPPORT_DIR_NAME / RUNTIME_FILE_NAME
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        return Path(state_home) / APP_SUPPORT_DIR_NAME / RUNTIME_FILE_NAME
    return Path.home() / ".local" / "state" / APP_SUPPORT_DIR_NAME / RUNTIME_FILE_NAME


def _is_api_healthy(api_base_url: str) -> bool:
    try:
        with urlopen(_health_url(api_base_url), timeout=0.5) as response:
            return 200 <= response.status < 300
    except (OSError, URLError):
        return False


def _health_url(api_base_url: str) -> str:
    base_url = api_base_url.rstrip("/")
    if base_url.endswith("/api"):
        return f"{base_url}/health"
    return f"{base_url}/api/health"


def _normalize_api_base_url(url: str) -> str:
    base_url = url.strip().rstrip("/")
    if base_url.endswith("/api"):
        return base_url
    return f"{base_url}/api"
