"""Async REST client for the Jupyter Server API."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import httpx

from .config import JupyterConfig, resolve_config
from .errors import JupyterHTTPError
from .paths import normalize_remote_path


class JupyterAPI:
    """Small wrapper over Jupyter's kernels and contents REST APIs."""

    def __init__(self, config: JupyterConfig, client: httpx.AsyncClient | None = None):
        self.config = config
        self._client = client
        self._owns_client = client is None

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"{self.config.auth_scheme} {self.config.token}"}

    async def __aenter__(self) -> "JupyterAPI":
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.url,
                headers=self.headers,
                timeout=httpx.Timeout(30.0, connect=10.0),
                follow_redirects=True,
            )
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
        self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("JupyterAPI must be used as an async context manager")
        return self._client

    async def list_kernels(self) -> list[dict[str, Any]]:
        return await self._request_json("GET", "/api/kernels")

    async def create_kernel(
        self, kernel_name: str = "python3", path: str | None = None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": kernel_name}
        if path:
            payload["path"] = normalize_remote_path(path)
        return await self._request_json("POST", "/api/kernels", json=payload)

    async def interrupt_kernel(self, kernel_id: str) -> dict[str, Any]:
        await self._request("POST", f"/api/kernels/{kernel_id}/interrupt")
        return {"success": True, "kernel_id": kernel_id}

    async def delete_kernel(self, kernel_id: str) -> dict[str, Any]:
        await self._request("DELETE", f"/api/kernels/{kernel_id}")
        return {"success": True, "kernel_id": kernel_id}

    async def get_contents(self, path: str = "", content: bool = True) -> dict[str, Any]:
        safe_path = normalize_remote_path(path)
        params = {"content": "1" if content else "0"}
        return await self._request_json(
            "GET", f"/api/contents/{safe_path}", params=params
        )

    async def save_contents(
        self,
        path: str,
        *,
        content: str,
        fmt: str,
        content_type: str = "file",
    ) -> dict[str, Any]:
        safe_path = normalize_remote_path(path)
        payload = {"type": content_type, "format": fmt, "content": content}
        return await self._request_json("PUT", f"/api/contents/{safe_path}", json=payload)

    async def create_directory(self, path: str) -> dict[str, Any]:
        safe_path = normalize_remote_path(path)
        return await self.save_contents(
            safe_path,
            content="",
            fmt="text",
            content_type="directory",
        )

    async def _request_json(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self._request(method, path, **kwargs)
        if not response.content:
            return None
        return response.json()

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.client.request(method, path, **kwargs)
        if response.status_code >= 400:
            message = _safe_error_message(response)
            raise JupyterHTTPError(response.status_code, message)
        return response


@asynccontextmanager
async def jupyter_api(
    url: str | None = None,
    token: str | None = None,
    auth_scheme: str | None = None,
) -> AsyncIterator[JupyterAPI]:
    """Create a Jupyter API client from explicit arguments or environment."""

    config = resolve_config(url=url, token=token, auth_scheme=auth_scheme)
    async with JupyterAPI(config) as api:
        yield api


def _safe_error_message(response: httpx.Response) -> str:
    """Extract a concise HTTP error without leaking request headers."""

    try:
        payload = response.json()
    except ValueError:
        text = response.text.strip()
        if len(text) > 500:
            text = f"{text[:500]}..."
        return f"Jupyter API returned HTTP {response.status_code}: {text}"

    if isinstance(payload, dict):
        reason = payload.get("reason") or payload.get("message") or payload.get("error")
        if reason:
            return f"Jupyter API returned HTTP {response.status_code}: {reason}"
    return f"Jupyter API returned HTTP {response.status_code}"
