from __future__ import annotations

from threading import Lock

from sqlalchemy import create_engine

from app.core.config import Settings
from app.infrastructure.db import models  # noqa: F401
from app.infrastructure.db.session import Base, sync_database_url

_SCHEMA_LOCK = Lock()
_INITIALIZED_DATABASE_URLS: set[str] = set()


def ensure_database_schema(settings: Settings) -> None:
    database_url = sync_database_url(settings)
    with _SCHEMA_LOCK:
        if database_url in _INITIALIZED_DATABASE_URLS and settings.database_path.exists():
            return
        settings.database_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(database_url)
        try:
            Base.metadata.create_all(engine)
        finally:
            engine.dispose()
        _INITIALIZED_DATABASE_URLS.add(database_url)
