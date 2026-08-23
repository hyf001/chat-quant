"""WebSocket execution client for Jupyter kernels."""

from __future__ import annotations

import asyncio
import base64
import json
import ssl
import tempfile
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

import certifi
import websockets

from .config import JupyterConfig, resolve_config
from .models import ExecutionResult, ImageArtifact


def build_kernel_ws_url(config: JupyterConfig, kernel_id: str) -> str:
    """Build the kernel channels WebSocket URL for a Jupyter server."""

    split = urlsplit(config.url)
    scheme = "wss" if split.scheme == "https" else "ws"
    base_path = split.path.rstrip("/")
    channel_path = f"{base_path}/api/kernels/{kernel_id}/channels"
    query = urlencode({"token": config.token})
    return urlunsplit((scheme, split.netloc, channel_path, query, ""))


async def execute_code_ws(
    kernel_id: str,
    code: str,
    *,
    url: str | None = None,
    token: str | None = None,
    auth_scheme: str | None = None,
    timeout: float = 120.0,
    image_dir: str | Path | None = None,
) -> ExecutionResult:
    """Execute code in a Jupyter kernel and collect structured outputs."""

    config = resolve_config(url=url, token=token, auth_scheme=auth_scheme)
    ws_url = build_kernel_ws_url(config, kernel_id)
    headers = {"Authorization": f"{config.auth_scheme} {config.token}"}
    msg_id = uuid.uuid4().hex
    session_id = uuid.uuid4().hex
    message = _execute_request(msg_id=msg_id, session_id=session_id, code=code)
    result = ExecutionResult()

    async with websockets.connect(
        ws_url,
        additional_headers=headers,
        ssl=_ssl_context_for_ws_url(ws_url),
        max_size=None,
    ) as websocket:
        await websocket.send(json.dumps(message))
        try:
            async with asyncio.timeout(timeout):
                while True:
                    raw = await websocket.recv()
                    payload = json.loads(raw)
                    if not _is_for_parent(payload, msg_id):
                        continue
                    if _handle_message(payload, result, image_dir=image_dir):
                        break
        except TimeoutError:
            result.error = {
                "ename": "TimeoutError",
                "evalue": f"Execution exceeded {timeout:g} seconds",
                "traceback": [],
            }
    return result


def _ssl_context_for_ws_url(ws_url: str) -> ssl.SSLContext | None:
    """Use certifi's CA bundle for wss connections."""

    if urlsplit(ws_url).scheme != "wss":
        return None
    return ssl.create_default_context(cafile=certifi.where())


def _execute_request(msg_id: str, session_id: str, code: str) -> dict[str, Any]:
    return {
        "header": {
            "msg_id": msg_id,
            "username": "supermind-mcp",
            "session": session_id,
            "msg_type": "execute_request",
            "version": "5.3",
        },
        "parent_header": {},
        "metadata": {},
        "content": {
            "code": code,
            "silent": False,
            "store_history": True,
            "user_expressions": {},
            "allow_stdin": False,
            "stop_on_error": True,
        },
        "channel": "shell",
        "buffers": [],
    }


def _is_for_parent(payload: dict[str, Any], parent_msg_id: str) -> bool:
    parent = payload.get("parent_header") or {}
    return parent.get("msg_id") == parent_msg_id


def _handle_message(
    payload: dict[str, Any],
    result: ExecutionResult,
    *,
    image_dir: str | Path | None = None,
) -> bool:
    """Update result from a Jupyter message. Returns True when execution is done."""

    msg_type = (payload.get("header") or {}).get("msg_type")
    content = payload.get("content") or {}

    if msg_type == "stream":
        name = content.get("name")
        text = content.get("text", "")
        if name == "stderr":
            result.stderr.append(text)
        else:
            result.stdout.append(text)
        return False

    if msg_type in {"execute_result", "display_data"}:
        data = content.get("data") or {}
        if msg_type == "execute_result":
            result.result = _plain_result(data)
        result.images.extend(
            _extract_images(data, start_id=len(result.images), image_dir=image_dir)
        )
        return False

    if msg_type == "error":
        result.error = {
            "ename": content.get("ename"),
            "evalue": content.get("evalue"),
            "traceback": content.get("traceback", []),
        }
        return False

    if msg_type == "status":
        return content.get("execution_state") == "idle"

    if msg_type == "execute_reply":
        status = content.get("status")
        if status == "error" and result.error is None:
            result.error = {
                "ename": content.get("ename"),
                "evalue": content.get("evalue"),
                "traceback": content.get("traceback", []),
            }
        return False

    return False


def _plain_result(data: dict[str, Any]) -> Any:
    if "text/plain" in data:
        return data["text/plain"]
    return data or None


def _extract_images(
    data: dict[str, Any],
    *,
    start_id: int = 0,
    image_dir: str | Path | None = None,
) -> list[ImageArtifact]:
    images: list[ImageArtifact] = []
    for mime in ("image/png", "image/jpeg", "image/svg+xml"):
        if mime not in data:
            continue
        images.append(
            _save_image(data[mime], mime, start_id + len(images), image_dir=image_dir)
        )
    return images


def _save_image(
    content: str,
    mime: str,
    image_id: int,
    *,
    image_dir: str | Path | None = None,
) -> ImageArtifact:
    suffix = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/svg+xml": ".svg",
    }[mime]
    directory = Path(image_dir) if image_dir else Path(tempfile.gettempdir())
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"jupyter_img_{uuid.uuid4().hex}_{image_id}{suffix}"

    if mime == "image/svg+xml":
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(base64.b64decode(content))
    return ImageArtifact(id=image_id, mime=mime, path=str(path))
