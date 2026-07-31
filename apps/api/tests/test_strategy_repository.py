from pathlib import Path

import pytest
from app.core.config import Settings
from app.domain.strategies.models import StrategyPackage
from app.domain.strategies.service import StrategyService
from app.infrastructure.db.schema import ensure_database_schema
from app.infrastructure.db.session import make_engine, make_session_factory
from app.infrastructure.db.strategy_repository import SQLAlchemyStrategyRepository
from tests.test_strategy_api import strategy_package


@pytest.mark.asyncio
async def test_sqlalchemy_repository_persists_strategy_across_instances(
    tmp_path: Path,
) -> None:
    settings = Settings(_env_file=None, CHATQ_DATABASE_PATH=tmp_path / "chat-quant.db")
    ensure_database_schema(settings)

    session_factory = make_session_factory(make_engine(settings))
    service = StrategyService(SQLAlchemyStrategyRepository(session_factory))
    created = await service.create_strategy(
        user_id="user_a",
        project_id="project_a",
        package=StrategyPackage.model_validate(strategy_package()),
    )

    restored_service = StrategyService(SQLAlchemyStrategyRepository(session_factory))
    detail = await restored_service.get_strategy(created.strategy_id)
    versions = await restored_service.repository.list_versions(created.strategy_id)

    assert detail.strategy.current_version_id == versions[0].id
    assert versions[0].default_params["fast_period"] == 20
    assert versions[0].code_checksum
