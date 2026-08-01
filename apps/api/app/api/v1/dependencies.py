from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header

from app.core.config import get_settings


def get_user_id(x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None) -> str:
    return x_user_id or get_settings().default_user_id


def get_project_id(
    x_project_id: Annotated[str | None, Header(alias="X-Project-Id")] = None,
) -> str:
    return x_project_id or get_settings().default_project_id


UserId = Annotated[str, Depends(get_user_id)]
ProjectId = Annotated[str, Depends(get_project_id)]
