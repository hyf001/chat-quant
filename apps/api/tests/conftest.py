from collections.abc import Iterator
from pathlib import Path

import pytest
from app.core.config import get_settings
from app.db.session import get_engine, get_session_factory
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolated_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("CHATQ_DATABASE_PATH", str(tmp_path / "chat-quant.db"))
    _clear_dependency_caches()
    yield
    _clear_dependency_caches()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _clear_dependency_caches() -> None:
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
