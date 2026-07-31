from __future__ import annotations

from dataclasses import replace

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.projects.models import Project
from app.domain.projects.repositories import ProjectNotFoundError, ProjectRepository
from app.infrastructure.db.models.project import ProjectRow


class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(self, project: Project) -> Project:
        async with self._session_factory() as db:
            db.add(_project_to_row(project))
            await db.commit()
        return replace(project)

    async def update(self, project: Project) -> Project:
        async with self._session_factory() as db:
            row = await db.get(ProjectRow, project.id)
            if row is None:
                raise ProjectNotFoundError(project.id)
            _apply_project(row, project)
            await db.commit()
        return replace(project)

    async def get(self, project_id: str) -> Project | None:
        async with self._session_factory() as db:
            row = await db.get(ProjectRow, project_id)
            return _row_to_project(row) if row is not None else None

    async def list_for_user(
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

        async with self._session_factory() as db:
            total = (
                await db.scalar(select(func.count()).select_from(ProjectRow).where(*filters))
                or 0
            )
            result = await db.scalars(
                select(ProjectRow)
                .where(*filters)
                .order_by(ProjectRow.updated_at.desc())
                .limit(limit)
                .offset(offset)
            )
            rows = result.all()
            return [_row_to_project(row) for row in rows], total


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
