from __future__ import annotations

from app.domain.projects.models import Project


class ProjectNotFoundError(LookupError):
    pass


class ProjectRepository:
    async def create(self, project: Project) -> Project:
        raise NotImplementedError

    async def update(self, project: Project) -> Project:
        raise NotImplementedError

    async def get(self, project_id: str) -> Project | None:
        raise NotImplementedError

    async def list_for_user(
        self,
        *,
        user_id: str,
        query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Project], int]:
        raise NotImplementedError

