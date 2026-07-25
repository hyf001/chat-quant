from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import Settings


class Base(DeclarativeBase):
    pass


def sqlite_url(path: Path) -> str:
    return f"sqlite:///{path}"


def chat_session_database_url(settings: Settings) -> str:
    return sqlite_url(settings.chat_session_index_path)


def make_engine(database_url: str, *, connect_args: dict[str, object] | None = None) -> Engine:
    return create_engine(database_url, connect_args=connect_args or {})


def make_chat_session_engine(settings: Settings) -> Engine:
    settings.chat_session_index_path.parent.mkdir(parents=True, exist_ok=True)
    return make_engine(
        chat_session_database_url(settings),
        connect_args={"check_same_thread": False},
    )


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
