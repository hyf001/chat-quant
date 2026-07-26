from __future__ import annotations

from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import Settings


class Base(DeclarativeBase):
    pass


def sync_sqlite_url(path: Path) -> str:
    return f"sqlite:///{path}"


def async_sqlite_url(path: Path) -> str:
    return f"sqlite+aiosqlite:///{path}"


def database_url(settings: Settings) -> str:
    return async_sqlite_url(settings.database_path)


def sync_database_url(settings: Settings) -> str:
    return sync_sqlite_url(settings.database_path)


def make_engine(settings: Settings) -> AsyncEngine:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    return create_async_engine(database_url(settings))


def make_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
