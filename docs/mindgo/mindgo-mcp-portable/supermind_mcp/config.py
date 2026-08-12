"""Configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .errors import ConfigError


DEFAULT_AUTH_SCHEME = "Bearer"


@dataclass(frozen=True)
class JupyterConfig:
    """Connection settings for a Jupyter server."""

    url: str
    token: str
    auth_scheme: str = DEFAULT_AUTH_SCHEME


def resolve_config(
    url: str | None = None,
    token: str | None = None,
    auth_scheme: str | None = None,
) -> JupyterConfig:
    """Resolve Jupyter connection settings from parameters or environment."""

    resolved_url = (url or os.getenv("JUPYTER_URL") or "").strip()
    resolved_token = (token or os.getenv("JUPYTER_TOKEN") or "").strip()
    resolved_scheme = (
        auth_scheme or os.getenv("JUPYTER_AUTH_SCHEME") or DEFAULT_AUTH_SCHEME
    ).strip()

    if not resolved_url:
        raise ConfigError("Jupyter URL not provided")
    if not resolved_token:
        raise ConfigError("Jupyter token not provided")
    if not resolved_scheme:
        raise ConfigError("Jupyter auth scheme not provided")

    return JupyterConfig(
        url=resolved_url.rstrip("/"),
        token=resolved_token,
        auth_scheme=resolved_scheme,
    )
