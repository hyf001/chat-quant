from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, Request

from app.core.config import get_settings
from app.domain.chat_sessions.repositories import (
    InMemoryAssetLinkRepository,
    InMemoryChatSessionRepository,
)
from app.domain.chat_sessions.services import AssetLinkService, ChatSessionService


class M1Services:
    def __init__(self) -> None:
        settings = get_settings()
        self.session_repository = InMemoryChatSessionRepository()
        self.asset_repository = InMemoryAssetLinkRepository()
        self.chat_sessions = ChatSessionService(
            self.session_repository,
            self.asset_repository,
            claude_agent_cwd=settings.claude_agent_cwd,
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
