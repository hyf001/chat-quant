import asyncio
from collections.abc import Iterator
from pathlib import Path

import pytest
from app.application.dependencies import (
    get_backtest_service,
    get_database_session_factory,
    get_project_service,
    get_strategy_service,
)
from app.core.config import get_settings
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolated_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("CHATQ_DATABASE_PATH", str(tmp_path / "chat-quant.db"))
    _clear_dependency_caches()
    asyncio.run(get_strategy_service().repository.clear())
    yield
    asyncio.run(get_strategy_service().repository.clear())
    _clear_dependency_caches()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _clear_dependency_caches() -> None:
    get_settings.cache_clear()
    get_database_session_factory.cache_clear()
    get_project_service.cache_clear()
    get_strategy_service.cache_clear()
    get_backtest_service.cache_clear()
    if hasattr(app.state, "m1_services"):
        delattr(app.state, "m1_services")
