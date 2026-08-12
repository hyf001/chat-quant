"""Jupyter-to-local file download support."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from .errors import JupyterHTTPError
from .jupyter_api import jupyter_api
from .models import DownloadResult, FileTransferItem
from .paths import normalize_remote_path, safe_local_target


async def download_files(
    *,
    remote_path: str = "",
    local_path: str = ".",
    url: str | None = None,
    token: str | None = None,
) -> DownloadResult:
    """Download a remote Jupyter file or directory into a local directory."""

    safe_remote_path = normalize_remote_path(remote_path)
    base = Path(local_path).expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)
    result = DownloadResult(success=True)

    async with jupyter_api(url=url, token=token) as api:
        try:
            root = await api.get_contents(safe_remote_path, content=True)
            await _download_node(api, root, base=base, result=result)
        except JupyterHTTPError as exc:
            if exc.status_code == 404:
                result.success = False
                result.failed += 1
                result.errors.append("PATH_NOT_FOUND")
            elif exc.status_code == 413:
                result.success = False
                result.errors.append("超过当日下载量限制")
            else:
                result.success = False
                result.failed += 1
                result.errors.append(str(exc))

    result.success = result.success and result.failed == 0
    return result


async def _download_node(
    api: object,
    node: dict[str, Any],
    *,
    base: Path,
    result: DownloadResult,
) -> None:
    node_type = node.get("type")
    node_path = normalize_remote_path(node.get("path") or node.get("name") or "")

    if node_type == "directory":
        children = node.get("content") or []
        if not isinstance(children, list):
            node = await api.get_contents(node_path, content=True)  # type: ignore[attr-defined]
            children = node.get("content") or []
        for child in children:
            if not result.success:
                return
            try:
                child_path = normalize_remote_path(child.get("path") or "")
                child_node = await api.get_contents(child_path, content=True)  # type: ignore[attr-defined]
                await _download_node(api, child_node, base=base, result=result)
            except JupyterHTTPError as exc:
                if exc.status_code == 413:
                    result.success = False
                    result.errors.append("超过当日下载量限制")
                    return
                result.failed += 1
                result.errors.append(f"{child.get('path', '')}: {exc}")
        return

    if node_type not in {"file", "notebook"}:
        result.skipped += 1
        result.files.append(
            FileTransferItem(path=node_path, action="skip", error=f"Unsupported type: {node_type}")
        )
        return

    result.total += 1
    try:
        target = safe_local_target(base, node_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        _write_file_node(target, node)
        result.downloaded += 1
        result.files.append(
            FileTransferItem(
                path=node_path,
                size=target.stat().st_size,
                local_path=str(target),
                action="download",
            )
        )
    except Exception as exc:  # noqa: BLE001 - report partial download state
        target = safe_local_target(base, node_path)
        if target.exists():
            target.unlink()
        result.failed += 1
        result.files.append(
            FileTransferItem(path=node_path, action="download", error=str(exc))
        )
        result.errors.append(f"{node_path}: {exc}")


def _write_file_node(target: Path, node: dict[str, Any]) -> None:
    if node.get("type") == "notebook":
        content = node.get("content")
        if content is None:
            raise ValueError("Notebook content is missing")
        target.write_text(
            json.dumps(content, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return

    fmt = node.get("format")
    content = node.get("content")
    if content is None:
        raise ValueError("File content is missing")
    if fmt == "base64":
        target.write_bytes(base64.b64decode(content))
    elif fmt == "text" or fmt is None:
        target.write_text(str(content), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file format: {fmt}")
