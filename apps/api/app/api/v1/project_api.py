from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.project import (
    ProjectCreateRequest,
    ProjectDirectoryResponse,
    ProjectFileContentResponse,
    ProjectFileEntry,
    ProjectListResponse,
    ProjectOpenRequest,
    ProjectResolveRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from app.service import project as project_service
from app.service.project import ProjectNotFoundError, ProjectPathError

router = APIRouter()

EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}
MAX_FILE_CONTENT_BYTES = 1_000_000


def _raise_not_found() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@router.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.create_project(
            db,
            local_path=payload.local_path,
            name=payload.name,
            description=payload.description,
        )
    except (ProjectPathError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project_legacy(
    payload: ProjectCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_project(payload, db)


@router.post("/open", response_model=ProjectResponse)
async def open_project(
    payload: ProjectOpenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.open_project(
            db,
            local_path=payload.local_path,
            name=payload.name,
            description=payload.description,
        )
    except ProjectPathError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/resolve", response_model=ProjectResponse)
async def resolve_project(
    payload: ProjectResolveRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.resolve_project(
            db,
            local_path=payload.local_path,
            name=payload.name,
            description=payload.description,
        )
    except ProjectPathError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    query: str | None = Query(default=None, max_length=120),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    items, total = await project_service.list_projects(
        db,
        query=query,
        limit=limit,
        offset=offset,
    )
    return ProjectListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.require_project(db, project_id)
    except ProjectNotFoundError:
        _raise_not_found()


@router.get("/{project_id}/files", response_model=ProjectDirectoryResponse)
async def list_project_files(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    path: str = Query(default="", max_length=2000),
):
    try:
        project = await project_service.require_project(db, project_id)
    except ProjectNotFoundError:
        _raise_not_found()

    project_dir, current_dir = _resolve_project_directory(project.local_path, path)
    try:
        children = list(current_dir.iterdir())
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project directory cannot be read",
        ) from exc

    items: list[ProjectFileEntry] = []
    for child in children:
        if child.name in EXCLUDED_FILE_NAMES:
            continue
        try:
            stat = child.stat()
        except OSError:
            continue
        is_dir = child.is_dir()
        relative_path = child.relative_to(project_dir).as_posix()
        items.append(
            ProjectFileEntry(
                name=child.name,
                relative_path=relative_path,
                type="directory" if is_dir else "file",
                size=None if is_dir else stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                extension=None if is_dir else child.suffix.lower().lstrip(".") or None,
            )
        )

    items.sort(key=lambda item: (item.type != "directory", item.name.casefold()))
    current_path = current_dir.relative_to(project_dir).as_posix()
    if current_path == ".":
        current_path = ""
    parent_path = None
    if current_path:
        parent = current_dir.parent.relative_to(project_dir).as_posix()
        parent_path = "" if parent == "." else parent

    return ProjectDirectoryResponse(
        project_id=project.id,
        root_name=project.name,
        current_path=current_path,
        parent_path=parent_path,
        items=items,
    )


@router.get("/{project_id}/files/content", response_model=ProjectFileContentResponse)
async def get_project_file_content(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    path: str = Query(..., min_length=1, max_length=2000),
):
    try:
        project = await project_service.require_project(db, project_id)
    except ProjectNotFoundError:
        _raise_not_found()

    file = _resolve_project_file(project.local_path, path)
    try:
        stat = file.stat()
        with file.open("rb") as handle:
            raw = handle.read(MAX_FILE_CONTENT_BYTES + 1)
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project file cannot be read",
        ) from exc

    truncated = len(raw) > MAX_FILE_CONTENT_BYTES
    preview_bytes = raw[:MAX_FILE_CONTENT_BYTES]
    try:
        content = preview_bytes.decode("utf-8", errors="ignore" if truncated else "strict")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project file is not UTF-8 text",
        ) from exc

    return ProjectFileContentResponse(
        project_id=project.id,
        name=file.name,
        relative_path=file.relative_to(Path(project.local_path).resolve(strict=True)).as_posix(),
        size=stat.st_size,
        modified_at=datetime.fromtimestamp(stat.st_mtime),
        extension=file.suffix.lower().lstrip(".") or None,
        content=content,
        truncated=truncated,
    )


@router.get("/{project_id}/visualization-html/{file_path:path}")
async def get_project_visualization_html(
    project_id: str,
    file_path: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        project = await project_service.require_project(db, project_id)
    except ProjectNotFoundError:
        _raise_not_found()
    requested = Path(file_path)
    if not file_path.strip() or requested.is_absolute():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="visualization html path must be a relative .html file path",
        )
    if requested.suffix.lower() != ".html":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="visualization html path must use .html extension",
        )
    html_file = _resolve_project_file(project.local_path, file_path)
    return FileResponse(
        html_file,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    payload: ProjectUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.update_project(
            db,
            project_id,
            name=payload.name,
            description=payload.description,
        )
    except ProjectNotFoundError:
        _raise_not_found()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await project_service.soft_delete_project(db, project_id)
    except ProjectNotFoundError:
        _raise_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _resolve_project_directory(project_local_path: str, directory_path: str) -> tuple[Path, Path]:
    resolved = _resolve_project_path(project_local_path, directory_path, allow_empty=True)
    try:
        project_dir = Path(project_local_path).resolve(strict=True)
        current_dir = resolved.resolve(strict=True)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project directory not found",
        ) from exc
    if not current_dir.is_dir() or not current_dir.is_relative_to(project_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project directory not found",
        )
    return project_dir, current_dir


def _resolve_project_file(project_local_path: str, file_path: str) -> Path:
    resolved = _resolve_project_path(project_local_path, file_path, allow_empty=False)
    try:
        project_dir = Path(project_local_path).resolve(strict=True)
        file = resolved.resolve(strict=True)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project file not found",
        ) from exc
    if not file.is_file() or not file.is_relative_to(project_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project file not found",
        )
    return file


def _resolve_project_path(
    project_local_path: str,
    relative_path: str,
    *,
    allow_empty: bool,
) -> Path:
    requested = Path(relative_path)
    if (not allow_empty and not relative_path.strip()) or requested.is_absolute():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="project path must be a relative path",
        )
    try:
        project_dir = Path(project_local_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project directory not found",
        ) from exc
    candidate = project_dir if not relative_path.strip() else project_dir / requested
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(project_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project path not found",
        )
    return resolved
