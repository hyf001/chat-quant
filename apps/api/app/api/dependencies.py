from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, Request

from app.application.dependencies import get_database_session_factory
from app.core.config import get_settings
from app.domain.chat_sessions.repositories import (
    AssetLinkRepository,
    ChatSessionRepository,
)
from app.domain.chat_sessions.services import AssetLinkService, ChatSessionService
from app.infrastructure.db import SQLAlchemyAssetLinkRepository, SQLAlchemyChatSessionRepository


class M1Services:
    def __init__(
        self,
        session_repository: ChatSessionRepository | None = None,
        asset_repository: AssetLinkRepository | None = None,
    ) -> None:
        settings = get_settings()
        uses_default_repositories = session_repository is None or asset_repository is None
        if session_repository is None or asset_repository is None:
            session_factory = get_database_session_factory()
            session_repository = session_repository or SQLAlchemyChatSessionRepository(
                session_factory
            )
            asset_repository = asset_repository or SQLAlchemyAssetLinkRepository(session_factory)

        self.session_repository = session_repository
        self.asset_repository = asset_repository
        self.chat_sessions = ChatSessionService(
            self.session_repository,
            self.asset_repository,
            claude_agent_cwd=settings.claude_agent_cwd,
            project_home=settings.project_home if uses_default_repositories else None,
        )
        self.asset_links = AssetLinkService(self.session_repository, self.asset_repository)


def get_m1_services(request: Request) -> M1Services:
    services = getattr(request.app.state, "m1_services", None)
    if services is None:
        services = M1Services()
        request.app.state.m1_services = services
    return services


def reset_m1_services(request: Request) -> None:
    request.app.state.m1_services = M1Services()


def get_user_id(x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None) -> str:
    return x_user_id or get_settings().default_user_id


def get_project_id(
    x_project_id: Annotated[str | None, Header(alias="X-Project-Id")] = None,
) -> str:
    return x_project_id or get_settings().default_project_id


UserId = Annotated[str, Depends(get_user_id)]
ProjectId = Annotated[str, Depends(get_project_id)]
ServicesDep = Annotated[M1Services, Depends(get_m1_services)]
