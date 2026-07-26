from functools import lru_cache

from app.application.artifact_service import CodeArtifactService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.domain.backtests.service import BacktestService
from app.domain.strategies.service import StrategyService
from app.infrastructure.backtests import BacktraderStrategyBacktestEngine
from app.infrastructure.db import (
    SQLAlchemyArtifactRepository,
    SQLAlchemyStrategyRepository,
)
from app.infrastructure.db.schema import ensure_database_schema
from app.infrastructure.db.session import make_engine, make_session_factory
from app.infrastructure.storage import FilesystemArtifactStore

logger = get_logger(__name__)


@lru_cache
def get_database_session_factory():
    settings = get_settings()
    ensure_database_schema(settings)
    engine = make_engine(settings)
    return make_session_factory(engine)


@lru_cache
def get_artifact_service() -> CodeArtifactService:
    settings = get_settings()
    logger.info(
        "artifact service initialized",
        extra={
            "artifact_root": str(settings.artifact_root),
            "database_path": str(settings.database_path),
        },
    )
    return CodeArtifactService(
        repository=SQLAlchemyArtifactRepository(get_database_session_factory()),
        store=FilesystemArtifactStore(settings.artifact_root),
    )


@lru_cache
def get_strategy_service() -> StrategyService:
    return StrategyService(SQLAlchemyStrategyRepository(get_database_session_factory()))


@lru_cache
def get_backtest_service() -> BacktestService:
    return BacktestService(SQLAlchemyStrategyRepository(get_database_session_factory()))


@lru_cache
def get_strategy_backtest_engine() -> BacktraderStrategyBacktestEngine:
    return BacktraderStrategyBacktestEngine()
