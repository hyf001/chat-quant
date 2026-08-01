from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import UserId
from app.db.session import get_db
from app.schema.project import (
    ProjectCreateRequest,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdateRequest,
)
from app.service import project as project_service
from app.service.project import ProjectAccessError, ProjectNotFoundError

router = APIRouter()


def _raise_not_found() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


def _raise_forbidden() -> None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project access denied")


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreateRequest,
    user_id: UserId,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.create_project(
            db,
            user_id=user_id,
            name=payload.name,
            description=payload.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    user_id: UserId,
    db: Annotated[AsyncSession, Depends(get_db)],
    query: str | None = Query(default=None, max_length=120),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    items, total = await project_service.list_projects(
        db,
        user_id=user_id,
        query=query,
        limit=limit,
        offset=offset,
    )
    return ProjectListResponse(items=items, total=total, limit=limit, offset=offset)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    payload: ProjectUpdateRequest,
    user_id: UserId,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await project_service.update_project(
            db,
            project_id,
            user_id=user_id,
            name=payload.name,
            description=payload.description,
        )
    except ProjectAccessError:
        _raise_forbidden()
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
    user_id: UserId,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await project_service.soft_delete_project(db, project_id, user_id=user_id)
    except ProjectAccessError:
        _raise_forbidden()
    except ProjectNotFoundError:
        _raise_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
