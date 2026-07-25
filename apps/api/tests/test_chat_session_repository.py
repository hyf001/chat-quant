from __future__ import annotations

import asyncio
from pathlib import Path

from app.core.config import Settings
from app.domain.chat_sessions.models import AssetRelationType, AssetType
from app.domain.chat_sessions.services import AssetLinkService, ChatSessionService
from app.infrastructure.db import SQLAlchemyAssetLinkRepository, SQLAlchemyChatSessionRepository
from app.infrastructure.db.migrations import run_chat_session_migrations
from app.infrastructure.db.session import make_chat_session_engine, make_session_factory


def test_sqlalchemy_chat_session_repository_persists_index_across_instances(
    tmp_path: Path,
) -> None:
    asyncio.run(_run_persistence_assertions(tmp_path))


async def _run_persistence_assertions(tmp_path: Path) -> None:
    settings = Settings(
        _env_file=None,
        CHATQ_CHAT_SESSION_INDEX_PATH=tmp_path / "conversations.sqlite3",
    )
    run_chat_session_migrations(settings)

    session_factory = make_session_factory(make_chat_session_engine(settings))
    service = ChatSessionService(
        SQLAlchemyChatSessionRepository(session_factory),
        SQLAlchemyAssetLinkRepository(session_factory),
    )
    created = await service.create_chat_session(
        user_id="user_a",
        project_id="project_a",
        chat_session_id="conv_persisted",
        title="持久化会话",
        initial_prompt="分析贵州茅台",
        tags=["maotai"],
    )
    await service.update_chat_session(
        created.id,
        user_id="user_a",
        sdk_session_id="sdk_persisted",
        summary="最近请求：分析贵州茅台",
    )

    asset_service = AssetLinkService(
        SQLAlchemyChatSessionRepository(session_factory),
        SQLAlchemyAssetLinkRepository(session_factory),
    )
    await asset_service.link_asset(
        chat_session_id=created.id,
        user_id="user_a",
        asset_type=AssetType.BACKTEST_RUN,
        asset_id="bt_001",
        relation_type=AssetRelationType.RESULT,
        display_snapshot={"annual_return_pct": 12.3},
    )

    restored_service = ChatSessionService(
        SQLAlchemyChatSessionRepository(make_session_factory(make_chat_session_engine(settings))),
        SQLAlchemyAssetLinkRepository(make_session_factory(make_chat_session_engine(settings))),
    )
    items, total = await restored_service.list_chat_sessions(user_id="user_a", query="持久")
    detail, assets = await restored_service.get_context(
        created.id,
        user_id="user_a",
    )

    assert total == 1
    assert items[0].id == "conv_persisted"
    assert detail.sdk_session_id == "sdk_persisted"
    assert detail.summary == "最近请求：分析贵州茅台"
    assert assets[0].display_snapshot == {"annual_return_pct": 12.3}
