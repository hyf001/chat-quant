from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.project import (
    ProjectCreateRequest,
    ProjectListResponse,
    ProjectOpenRequest,
    ProjectResolveRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from app.service import project as project_service
from app.service.project import ProjectNotFoundError, ProjectPathError

router = APIRouter()


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
