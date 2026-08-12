"""Shared exceptions for the Supermind MCP server."""

from __future__ import annotations


class SupermindError(Exception):
    """Base error for expected runtime failures."""


class ConfigError(SupermindError):
    """Raised when required configuration is missing or invalid."""


class PathSafetyError(SupermindError):
    """Raised when a remote or local path would escape its allowed root."""


class JupyterHTTPError(SupermindError):
    """HTTP failure from the Jupyter REST API."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(message)
