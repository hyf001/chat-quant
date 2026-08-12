from __future__ import annotations

import asyncio
from pathlib import Path

from app.core.config import Settings
from app.db.schema import ensure_database_schema
from app.db.session import make_engine, make_session_factory
from app.service import project as project_service
from app.service.chat_session import AssetLinkService, ChatSessionService
from app.service.chat_session.types import AssetRelationType, AssetType


def test_chat_session_service_persists_index_across_instances(
    tmp_path: Path,
) -> None:
    asyncio.run(_run_persistence_assertions(tmp_path))


async def _run_persistence_assertions(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "chat-quant.db")
    ensure_database_schema(settings)

    session_factory = make_session_factory(make_engine(settings))
    async with session_factory() as db:
        project_path = tmp_path / "project-a"
        project_path.mkdir()
        project = await project_service.resolve_project(db, local_path=str(project_path))
        chat_session_service = ChatSessionService(db)
        created = await chat_session_service.create_chat_session(
            project_id=project.id,
            chat_session_id="conv_persisted",
            title="持久化会话",
            initial_prompt="分析贵州茅台",
            tags=["maotai"],
        )
        await chat_session_service.update_chat_session(
            created.id,
            sdk_session_id="sdk_persisted",
            summary="最近请求：分析贵州茅台",
        )

        asset_service = AssetLinkService(db)
        await asset_service.link_asset(
            chat_session_id=created.id,
            asset_type=AssetType.BACKTEST_RUN,
            asset_id="bt_001",
            relation_type=AssetRelationType.RESULT,
            display_snapshot={"annual_return_pct": 12.3},
        )

    async with make_session_factory(make_engine(settings))() as db:
        restored_chat_session_service = ChatSessionService(db)
        items, total = await restored_chat_session_service.list_chat_sessions(
            query="持久"
        )
        detail, assets = await restored_chat_session_service.get_context(created.id)

    assert total == 1
    assert items[0].id == "conv_persisted"
    assert detail.sdk_session_id == "sdk_persisted"
    assert detail.summary == "最近请求：分析贵州茅台"
    assert assets[0].display_snapshot == {"annual_return_pct": 12.3}
