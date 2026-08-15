from __future__ import annotations

import hashlib
import os
from dataclasses import replace
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.project import ProjectRow
from app.service.project.types import Project, local_now


class ProjectNotFoundError(LookupError):
    pass


class ProjectPathError(ValueError):
    pass


def project_id_from_local_path(local_path: str) -> str:
    return f"project_{hashlib.sha256(local_path.encode('utf-8')).hexdigest()[:24]}"


def canonicalize_local_path(local_path: str) -> str:
    if not local_path.strip():
        raise ProjectPathError("local_path is required")
    return str(Path(local_path).expanduser().resolve(strict=False))


def _clean_name(name: str | None, local_path: str) -> str:
    if name is None:
        name = Path(local_path).name or local_path
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ValueError("project name is required")
    return normalized[:120]


def _ensure_read_write_directory(local_path: str) -> None:
    path = Path(local_path)
    if not path.exists() or not path.is_dir():
        raise ProjectPathError("project directory does not exist")
    if not os.access(path, os.R_OK | os.W_OK):
        raise ProjectPathError("project directory must be readable and writable")


class ProjectService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def open_project(
        self,
        *,
        local_path: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Project:
        canonical_path = canonicalize_local_path(local_path)
        _ensure_read_write_directory(canonical_path)
        existing = await self._get_by_local_path(canonical_path)
        if existing is not None:
            if existing.deleted_at is not None:
                existing = await self.update_project(
                    existing.id,
                    name=name or existing.name,
                    description=description if description is not None else existing.description,
                    restore=True,
                )
            return replace(existing)
        return await self._register_project(
            local_path=canonical_path,
            name=name,
            description=description,
        )

    async def create_project(
        self,
        *,
        local_path: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Project:
        canonical_path = canonicalize_local_path(local_path)
        Path(canonical_path).mkdir(parents=True, exist_ok=True)
        _ensure_read_write_directory(canonical_path)
        existing = await self._get_by_local_path(canonical_path)
        if existing is not None:
            if existing.deleted_at is not None:
                return await self.update_project(
                    existing.id,
                    name=name or existing.name,
                    description=description if description is not None else existing.description,
                    restore=True,
                )
            return replace(existing)
        return await self._register_project(
            local_path=canonical_path,
            name=name,
            description=description,
        )

    async def resolve_project(
        self,
        *,
        local_path: str,
        name: str | None = None,
        description: str | None = None,
        auto_register: bool = True,
    ) -> Project:
        canonical_path = canonicalize_local_path(local_path)
        existing = await self._get_by_local_path(canonical_path)
        if existing is not None and existing.deleted_at is None:
            return replace(existing)
        if not auto_register:
            raise ProjectNotFoundError(canonical_path)
        _ensure_read_write_directory(canonical_path)
        if existing is not None:
            return await self.update_project(
                existing.id,
                name=name or existing.name,
                description=description if description is not None else existing.description,
                restore=True,
            )
        return await self._register_project(
            local_path=canonical_path,
            name=name,
            description=description,
        )

    async def _register_project(
        self,
        *,
        local_path: str,
        name: str | None,
        description: str | None,
    ) -> Project:
        now = local_now()
        project = Project(
            id=project_id_from_local_path(local_path),
            local_path=local_path,
            name=_clean_name(name, local_path),
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
        name: str | None = None,
        description: str | None = None,
        restore: bool = False,
    ) -> Project:
        project = await self.require_project(project_id, include_deleted=restore)
        updated = replace(
            project,
            name=_clean_name(name, project.local_path) if name is not None else project.name,
            description=description if description is not None else project.description,
            deleted_at=None if restore else project.deleted_at,
            updated_at=local_now(),
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
        query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Project], int]:
        filters = [
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

    async def soft_delete_project(self, project_id: str) -> None:
        project = await self.require_project(project_id)
        now = local_now()
        deleted = replace(project, deleted_at=now, updated_at=now)
        row = await self._db.get(ProjectRow, deleted.id)
        if row is None:
            raise ProjectNotFoundError(deleted.id)
        _apply_project(row, deleted)
        await self._db.commit()

    async def require_project(
        self, project_id: str, *, include_deleted: bool = False
    ) -> Project:
        row = await self._db.get(ProjectRow, project_id)
        project = _row_to_project(row) if row is not None else None
        if project is None or (project.deleted_at is not None and not include_deleted):
            raise ProjectNotFoundError(project_id)
        return project

    async def _get_by_local_path(self, local_path: str) -> Project | None:
        row = await self._db.scalar(
            select(ProjectRow).where(ProjectRow.local_path == local_path)
        )
        return _row_to_project(row) if row is not None else None


def _service(db: AsyncSession) -> ProjectService:
    return ProjectService(db)


async def create_project(
    db: AsyncSession,
    *,
    local_path: str,
    name: str | None = None,
    description: str | None = None,
) -> Project:
    return await _service(db).create_project(
        local_path=local_path,
        name=name,
        description=description,
    )


async def open_project(
    db: AsyncSession,
    *,
    local_path: str,
    name: str | None = None,
    description: str | None = None,
) -> Project:
    return await _service(db).open_project(
        local_path=local_path,
        name=name,
        description=description,
    )


async def resolve_project(
    db: AsyncSession,
    *,
    local_path: str,
    name: str | None = None,
    description: str | None = None,
    auto_register: bool = True,
) -> Project:
    return await _service(db).resolve_project(
        local_path=local_path,
        name=name,
        description=description,
        auto_register=auto_register,
    )


async def require_project(db: AsyncSession, project_id: str) -> Project:
    return await _service(db).require_project(project_id)


async def update_project(
    db: AsyncSession,
    project_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
) -> Project:
    return await _service(db).update_project(
        project_id,
        name=name,
        description=description,
    )


async def list_projects(
    db: AsyncSession,
    *,
    query: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[Project], int]:
    return await _service(db).list_projects(
        query=query,
        limit=limit,
        offset=offset,
    )


async def soft_delete_project(db: AsyncSession, project_id: str) -> None:
    await _service(db).soft_delete_project(project_id)


def _project_to_row(project: Project) -> ProjectRow:
    row = ProjectRow()
    _apply_project(row, project)
    return row


def _apply_project(row: ProjectRow, project: Project) -> None:
    row.id = project.id
    row.local_path = project.local_path
    row.name = project.name
    row.description = project.description
    row.created_at = project.created_at
    row.updated_at = project.updated_at
    row.deleted_at = project.deleted_at


def _row_to_project(row: ProjectRow) -> Project:
    return Project(
        id=row.id,
        local_path=row.local_path,
        name=row.name,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
    )
