from __future__ import annotations

import asyncio
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Annotated

import nbformat
import websockets
from fastapi import APIRouter, Depends, HTTPException, Request, Response, WebSocket, status
from sqlalchemy.ext.asyncio import AsyncSession
from websockets.exceptions import ConnectionClosed

from app.db.session import get_db
from app.schema.notebook import (
    NotebookCreateRequest,
    NotebookDeleteRequest,
    NotebookFileEntry,
    NotebookFileListResponse,
    NotebookRenameRequest,
    NotebookServerResponse,
    NotebookServerStatusResponse,
    NotebookSessionRequest,
    NotebookSessionResponse,
)
from app.service import project as project_service
from app.service.notebook import NotebookRuntimeError, notebook_runtime_manager
from app.service.notebook.runtime import NOTEBOOK_DIR_NAME
from app.service.project import ProjectNotFoundError

router = APIRouter()

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}
WEBSOCKET_HANDSHAKE_HEADERS = {
    "sec-websocket-extensions",
    "sec-websocket-key",
    "sec-websocket-protocol",
    "sec-websocket-version",
}


@router.get("/{project_id}/files", response_model=NotebookFileListResponse)
async def list_notebook_files(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotebookFileListResponse:
    project = await _require_project(project_id, db)
    root_dir = _notebook_root(project.local_path)
    files: list[NotebookFileEntry] = []
    for file in root_dir.rglob("*.ipynb"):
        relative_parts = file.relative_to(root_dir).parts
        if not file.is_file() or any(part.startswith(".") for part in relative_parts):
            continue
        _ensure_python_kernel_metadata(file)
        files.append(_notebook_file_entry(root_dir, file))
    files.sort(key=lambda item: item.relative_path.casefold())
    return NotebookFileListResponse(project_id=project.id, root_dir=str(root_dir), files=files)


@router.post(
    "/{project_id}/files",
    response_model=NotebookFileEntry,
    status_code=status.HTTP_201_CREATED,
)
async def create_notebook_file(
    project_id: str,
    payload: NotebookCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotebookFileEntry:
    project = await _require_project(project_id, db)
    root_dir = _notebook_root(project.local_path)
    file = _available_notebook_path(root_dir, payload.name)
    notebook = nbformat.v4.new_notebook(
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        cells=[],
    )
    nbformat.write(notebook, file)
    return _notebook_file_entry(root_dir, file)


@router.patch("/{project_id}/files", response_model=NotebookFileEntry)
async def rename_notebook_file(
    project_id: str,
    payload: NotebookRenameRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotebookFileEntry:
    project = await _require_project(project_id, db)
    root_dir = _notebook_root(project.local_path)
    source = _resolve_notebook_file(root_dir, payload.path)
    target = _notebook_file_path(root_dir, payload.name)
    if target.exists() and target != source:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Notebook file already exists",
        )
    source.rename(target)
    _ensure_python_kernel_metadata(target)
    return _notebook_file_entry(root_dir, target)


@router.delete("/{project_id}/files", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notebook_file(
    project_id: str,
    payload: NotebookDeleteRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    project = await _require_project(project_id, db)
    root_dir = _notebook_root(project.local_path)
    file = _resolve_notebook_file(root_dir, payload.path)
    file.unlink()


@router.post("/{project_id}/server", response_model=NotebookServerResponse)
async def ensure_notebook_server(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotebookServerResponse:
    project = await _require_project(project_id, db)
    try:
        return await notebook_runtime_manager.ensure_server(
            project_id=project.id,
            project_path=project.local_path,
        )
    except NotebookRuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.get("/{project_id}/server", response_model=NotebookServerStatusResponse)
async def get_notebook_server_status(project_id: str) -> NotebookServerStatusResponse:
    return await notebook_runtime_manager.server_status(project_id=project_id)


@router.post("/{project_id}/sessions", response_model=NotebookSessionResponse)
async def ensure_notebook_session(
    project_id: str,
    payload: NotebookSessionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotebookSessionResponse:
    project = await _require_project(project_id, db)
    root_dir = _notebook_root(project.local_path)
    file = _resolve_notebook_file(root_dir, payload.path)
    _ensure_python_kernel_metadata(file)
    try:
        await notebook_runtime_manager.ensure_server(
            project_id=project.id,
            project_path=project.local_path,
        )
        return await notebook_runtime_manager.ensure_session(
            project_id=project.id,
            relative_path=file.relative_to(root_dir).as_posix(),
            name=file.name,
        )
    except NotebookRuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.delete("/{project_id}/server", status_code=status.HTTP_204_NO_CONTENT)
async def stop_notebook_server(project_id: str) -> None:
    await notebook_runtime_manager.stop_server(project_id=project_id)


@router.websocket("/{project_id}/proxy/{target_path:path}")
async def proxy_notebook_websocket(project_id: str, websocket: WebSocket) -> None:
    try:
        record = await notebook_runtime_manager.running_record(project_id=project_id)
    except NotebookRuntimeError:
        await websocket.close(code=1011)
        return

    upstream_url = _upstream_url(
        record.base_url.replace("http://", "ws://", 1),
        websocket,
        token=record.token,
    )
    headers = [
        (key.decode("latin-1"), value.decode("latin-1"))
        for key, value in websocket.headers.raw
        if key.decode("latin-1").lower()
        not in HOP_BY_HOP_HEADERS | WEBSOCKET_HANDSHAKE_HEADERS | {"host"}
    ]

    try:
        async with websockets.connect(
            upstream_url,
            additional_headers=headers,
            max_size=None,
            proxy=None,
        ) as upstream:
            await websocket.accept()
            await _relay_websocket(websocket, upstream)
    except Exception:
        if websocket.client_state.name != "DISCONNECTED":
            await websocket.close(code=1011)


@router.api_route(
    "/{project_id}/proxy",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
@router.api_route(
    "/{project_id}/proxy/{target_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
async def proxy_notebook_http(project_id: str, request: Request) -> Response:
    try:
        record = await notebook_runtime_manager.running_record(project_id=project_id)
        upstream_url = _upstream_url(record.base_url, request, token=record.token)
        status_code, headers, body = await asyncio.to_thread(
            _request_notebook_upstream,
            upstream_url,
            request.method,
            dict(request.headers),
            await request.body(),
            record.base_url,
        )
    except NotebookRuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    response = Response(content=body, status_code=status_code)
    for name, value in headers:
        response.headers.append(name, value)
    return response


async def _require_project(project_id: str, db: AsyncSession):
    try:
        return await project_service.require_project(db, project_id)
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        ) from exc


def _notebook_root(project_path: str) -> Path:
    root_dir = Path(project_path).expanduser().resolve(strict=True) / NOTEBOOK_DIR_NAME
    root_dir.mkdir(parents=True, exist_ok=True)
    return root_dir


def _available_notebook_path(root_dir: Path, requested_name: str | None) -> Path:
    file = _notebook_file_path(root_dir, requested_name or "Untitled")
    stem = file.stem
    index = 1
    while file.exists():
        file = root_dir / f"{stem} {index}.ipynb"
        index += 1
    return file


def _notebook_file_path(root_dir: Path, name: str) -> Path:
    raw_name = name.strip() or "Untitled"
    candidate = Path(raw_name)
    if candidate.is_absolute() or len(candidate.parts) != 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Notebook name must be a file name",
        )
    stem = candidate.stem.strip() or "Untitled"
    suffix = candidate.suffix or ".ipynb"
    if suffix.lower() != ".ipynb":
        stem = candidate.name
    return root_dir / f"{stem}.ipynb"


def _resolve_notebook_file(root_dir: Path, relative_path: str) -> Path:
    if not relative_path.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Notebook path is required",
        )
    requested = Path(relative_path)
    if requested.is_absolute():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Notebook path must be relative",
        )
    file = (root_dir / requested).resolve(strict=False)
    try:
        file.relative_to(root_dir)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Notebook path must stay inside the notebook directory",
        ) from exc
    if file.suffix.lower() != ".ipynb" or not file.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notebook file not found",
        )
    return file


def _ensure_python_kernel_metadata(file: Path) -> None:
    try:
        notebook = nbformat.read(file, as_version=4)
    except Exception:
        return
    metadata = notebook.setdefault("metadata", {})
    kernelspec = metadata.setdefault("kernelspec", {})
    language_info = metadata.setdefault("language_info", {})
    changed = False
    if not kernelspec.get("name"):
        kernelspec["name"] = "python3"
        changed = True
    if not kernelspec.get("display_name"):
        kernelspec["display_name"] = "Python 3"
        changed = True
    if not language_info.get("name"):
        language_info["name"] = "python"
        changed = True
    if changed:
        nbformat.write(notebook, file)


def _notebook_file_entry(root_dir: Path, file: Path) -> NotebookFileEntry:
    stat = file.stat()
    return NotebookFileEntry(
        name=file.name,
        relative_path=file.relative_to(root_dir).as_posix(),
        size=stat.st_size,
        modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
    )


def _upstream_url(base_url: str, request: Request | WebSocket, *, token: str) -> str:
    raw_path = request.scope.get("raw_path")
    if isinstance(raw_path, bytes):
        path = raw_path.decode("ascii")
    else:
        path = urllib.parse.quote(request.url.path, safe="/%")
    query = _query_with_token(
        request.scope.get("query_string", b"").decode("ascii"),
        token=token,
    )
    return f"{base_url}{path}{f'?{query}' if query else ''}"


def _query_with_token(query: str, *, token: str) -> str:
    if not token:
        return query
    pairs = urllib.parse.parse_qsl(query, keep_blank_values=True)
    if any(name == "token" for name, _ in pairs):
        return query
    pairs.append(("token", token))
    return urllib.parse.urlencode(pairs)


def _request_notebook_upstream(
    url: str,
    method: str,
    incoming_headers: dict[str, str],
    body: bytes,
    internal_base_url: str,
) -> tuple[int, list[tuple[str, str]], bytes]:
    headers = {
        name: value
        for name, value in incoming_headers.items()
        if name.lower() not in HOP_BY_HOP_HEADERS | {"host", "content-length"}
    }
    data = body if method.upper() not in {"GET", "HEAD"} else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=60) as response:
            return (
                response.status,
                _response_headers(response.headers.items(), internal_base_url),
                response.read(),
            )
    except urllib.error.HTTPError as exc:
        return (
            exc.code,
            _response_headers(exc.headers.items(), internal_base_url),
            exc.read(),
        )
    except OSError as exc:
        raise NotebookRuntimeError(f"Jupyter Notebook proxy request failed: {exc}") from exc


def _response_headers(
    headers: object,
    internal_base_url: str,
) -> list[tuple[str, str]]:
    safe_headers: list[tuple[str, str]] = []
    for name, value in headers:
        lower_name = name.lower()
        if lower_name in HOP_BY_HOP_HEADERS | {"content-length"}:
            continue
        if lower_name == "location" and value.startswith(internal_base_url):
            value = value[len(internal_base_url) :]
        safe_headers.append((name, value))
    return safe_headers


async def _relay_websocket(websocket: WebSocket, upstream: object) -> None:
    async def client_to_upstream() -> None:
        while True:
            message = await websocket.receive()
            message_type = message.get("type")
            if message_type == "websocket.disconnect":
                await upstream.close()
                return
            if "text" in message:
                await upstream.send(message["text"])
            elif "bytes" in message:
                await upstream.send(message["bytes"])

    async def upstream_to_client() -> None:
        try:
            async for message in upstream:
                if isinstance(message, bytes):
                    await websocket.send_bytes(message)
                else:
                    await websocket.send_text(message)
        except ConnectionClosed:
            return

    tasks = [
        asyncio.create_task(client_to_upstream()),
        asyncio.create_task(upstream_to_client()),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    for task in done:
        task.result()
