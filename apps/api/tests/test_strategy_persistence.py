from pathlib import Path

import pytest
from app.core.config import Settings
from app.db.schema import ensure_database_schema
from app.db.session import make_engine, make_session_factory
from app.schema.strategy import StrategyCreate
from app.service import project as project_service
from app.service.strategy import StrategyService
from tests.test_strategy_api import strategy_create_payload


@pytest.mark.asyncio
async def test_strategy_service_persists_strategy_across_instances(
    tmp_path: Path,
) -> None:
    settings = Settings(database_path=tmp_path / "chat-quant.db")
    ensure_database_schema(settings)

    session_factory = make_session_factory(make_engine(settings))
    async with session_factory() as db:
        project = await project_service.create_project(
            db,
            local_path=str(tmp_path / "project-a"),
            name="Project A",
        )
        strategy_service = StrategyService(db)
        payload = strategy_create_payload()
        payload.pop("project_id")
        created = await strategy_service.create_strategy(
            project_id=project.id,
            strategy_input=StrategyCreate.model_validate(payload),
        )

    async with session_factory() as db:
        restored_strategy_service = StrategyService(db)
        detail = await restored_strategy_service.get_strategy(created.strategy_id)
        versions = await restored_strategy_service.list_versions(created.strategy_id)

    assert detail.strategy.current_version_id == versions[0].id
    assert versions[0].strategy_mode == "single_symbol"
    assert versions[0].custom_params[0].name_en == "fast_period"
    assert "chatq_next" in versions[0].source_code
