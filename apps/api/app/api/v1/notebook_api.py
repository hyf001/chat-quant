from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Annotated

import nbformat
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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
