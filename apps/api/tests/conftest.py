from collections.abc import Iterator

import pytest
from app.domain.strategies.repository import strategy_repository
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def clear_strategy_repository() -> Iterator[None]:
    strategy_repository.clear()
    yield
    strategy_repository.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
