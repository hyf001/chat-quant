from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from app.domain.projects.models import Project, utc_now
from app.domain.projects.repositories import ProjectNotFoundError, ProjectRepository


class ProjectAccessError(PermissionError):
    pass


def _new_id() -> str:
    return f"project_{uuid4().hex[:16]}"


def _clean_name(name: str) -> str:
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ValueError("project name is required")
    return normalized[:120]


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self._projects = repository

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
        return await self._projects.create(project)

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
        return await self._projects.update(updated)

    async def list_projects(
        self,
        *,
        user_id: str,
        query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Project], int]:
        return await self._projects.list_for_user(
            user_id=user_id,
            query=query,
            limit=limit,
            offset=offset,
        )

    async def soft_delete_project(self, project_id: str, *, user_id: str) -> None:
        project = await self._require_project(project_id, user_id)
        now = utc_now()
        await self._projects.update(replace(project, deleted_at=now, updated_at=now))

    async def _require_project(self, project_id: str, user_id: str) -> Project:
        project = await self._projects.get(project_id)
        if project is None or project.deleted_at is not None:
            raise ProjectNotFoundError(project_id)
        if project.user_id != user_id:
            raise ProjectAccessError(project_id)
        return project
