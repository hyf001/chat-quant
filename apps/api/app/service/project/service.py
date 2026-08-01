from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.project import ProjectRow
from app.service.project.types import Project, utc_now


class ProjectAccessError(PermissionError):
    pass


class ProjectNotFoundError(LookupError):
    pass


def _new_id() -> str:
    return f"project_{uuid4().hex[:16]}"


def _clean_name(name: str) -> str:
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ValueError("project name is required")
    return normalized[:120]


class ProjectService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_project(
        self,
        *,
        user_id: str,
        name: str,
        description: str | None = None,
    ) -> Project:
        now = utc_now()
        project = Project(
            id=_new_id(),
            user_id=user_id,
            name=_clean_name(name),
            description=description,
            created_at=now,
            updated_at=now,
        )
        self._db.add(_project_to_row(project))
        await self._db.commit()
        return replace(project)

    async def update_project(
        self,
        project_id: str,
        *,
        user_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Project:
        project = await self._require_project(project_id, user_id)
        updated = replace(
            project,
            name=_clean_name(name) if name is not None else project.name,
            description=description if description is not None else project.description,
            updated_at=utc_now(),
        )
        row = await self._db.get(ProjectRow, updated.id)
        if row is None:
            raise ProjectNotFoundError(updated.id)
        _apply_project(row, updated)
        await self._db.commit()
        return replace(updated)

    async def list_projects(
        self,
        *,
        user_id: str,
        query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Project], int]:
        filters = [
            ProjectRow.user_id == user_id,
            ProjectRow.deleted_at.is_(None),
        ]
        if query:
            pattern = f"%{query.casefold()}%"
            filters.append(
                func.lower(ProjectRow.name).like(pattern)
                | func.lower(func.coalesce(ProjectRow.description, "")).like(pattern)
            )

        total = (
            await self._db.scalar(select(func.count()).select_from(ProjectRow).where(*filters))
            or 0
        )
        result = await self._db.scalars(
            select(ProjectRow)
            .where(*filters)
            .order_by(ProjectRow.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = result.all()
        return [_row_to_project(row) for row in rows], total

    async def soft_delete_project(self, project_id: str, *, user_id: str) -> None:
        project = await self._require_project(project_id, user_id)
        now = utc_now()
        deleted = replace(project, deleted_at=now, updated_at=now)
        row = await self._db.get(ProjectRow, deleted.id)
        if row is None:
            raise ProjectNotFoundError(deleted.id)
        _apply_project(row, deleted)
        await self._db.commit()

    async def _require_project(self, project_id: str, user_id: str) -> Project:
        row = await self._db.get(ProjectRow, project_id)
        project = _row_to_project(row) if row is not None else None
        if project is None or project.deleted_at is not None:
            raise ProjectNotFoundError(project_id)
        if project.user_id != user_id:
            raise ProjectAccessError(project_id)
        return project


def _service(db: AsyncSession) -> ProjectService:
    return ProjectService(db)


async def create_project(
    db: AsyncSession,
    *,
    user_id: str,
    name: str,
    description: str | None = None,
) -> Project:
    return await _service(db).create_project(
        user_id=user_id,
        name=name,
        description=description,
    )


async def update_project(
    db: AsyncSession,
    project_id: str,
    *,
    user_id: str,
    name: str | None = None,
    description: str | None = None,
) -> Project:
    return await _service(db).update_project(
        project_id,
        user_id=user_id,
        name=name,
        description=description,
    )


async def list_projects(
    db: AsyncSession,
    *,
    user_id: str,
    query: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[Project], int]:
    return await _service(db).list_projects(
        user_id=user_id,
        query=query,
        limit=limit,
        offset=offset,
    )


async def soft_delete_project(db: AsyncSession, project_id: str, *, user_id: str) -> None:
    await _service(db).soft_delete_project(project_id, user_id=user_id)


def _project_to_row(project: Project) -> ProjectRow:
    row = ProjectRow()
    _apply_project(row, project)
    return row


def _apply_project(row: ProjectRow, project: Project) -> None:
    row.id = project.id
    row.user_id = project.user_id
    row.name = project.name
    row.description = project.description
    row.created_at = project.created_at
    row.updated_at = project.updated_at
    row.deleted_at = project.deleted_at


def _row_to_project(row: ProjectRow) -> Project:
    return Project(
        id=row.id,
        user_id=row.user_id,
        name=row.name,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
    )
