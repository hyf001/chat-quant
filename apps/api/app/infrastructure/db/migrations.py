from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.config import Settings
from app.infrastructure.db.session import sync_database_url


def run_database_migrations(settings: Settings) -> None:
    alembic_ini = _api_root() / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini))
    alembic_cfg.set_main_option("script_location", str(_api_root() / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", sync_database_url(settings))
    command.upgrade(alembic_cfg, "head")


def run_chat_session_migrations(settings: Settings) -> None:
    run_database_migrations(settings)


def _api_root() -> Path:
    return Path(__file__).resolve().parents[3]
