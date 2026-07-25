from pathlib import Path

from app.domain.strategies.models import StrategyPackage
from app.domain.strategies.repository import StrategyRepository
from app.domain.strategies.service import StrategyService
from tests.test_strategy_api import strategy_package


def test_sqlite_repository_persists_strategy_across_instances(tmp_path: Path) -> None:
    db_path = tmp_path / "m5.sqlite3"
    service = StrategyService(StrategyRepository(str(db_path)))
    created = service.create_strategy(
        user_id="user_a",
        project_id="project_a",
        chat_session_id="conv_persisted",
        package=StrategyPackage.model_validate(strategy_package()),
    )

    restored_service = StrategyService(StrategyRepository(str(db_path)))
    detail = restored_service.get_strategy(created.strategy_id)
    versions = restored_service.repository.list_versions(created.strategy_id)

    assert detail.strategy.chat_session_id == "conv_persisted"
    assert detail.strategy.current_version_id == versions[0].id
    assert versions[0].default_params["fast_period"] == 20
    assert versions[0].code_checksum
