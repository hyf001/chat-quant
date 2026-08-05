from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from app.core.config import get_settings
from app.db.schema import ensure_database_schema
from app.db.session import get_engine, get_session_factory
from app.main import app
from app.model.project import ProjectRow
from fastapi.testclient import TestClient
from sqlalchemy import create_engine


@pytest.fixture(autouse=True)
def isolated_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("CHATQ_DATABASE_PATH", str(tmp_path / "chat-quant.db"))
    _clear_dependency_caches()
    yield
    _clear_dependency_caches()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def project_test() -> None:
    settings = get_settings()
    ensure_database_schema(settings)
    engine = create_engine(f"sqlite:///{settings.database_path}")
    now = datetime.now(UTC)
    try:
        with engine.begin() as connection:
            connection.execute(
                ProjectRow.__table__.insert().prefix_with("OR IGNORE"),
                {
                    "id": "project_test",
                    "local_path": "/tmp/chatq-test-project",
                    "name": "测试项目",
                    "description": None,
                    "created_at": now,
                    "updated_at": now,
                    "deleted_at": None,
                },
            )
    finally:
        engine.dispose()


def _clear_dependency_caches() -> None:
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
