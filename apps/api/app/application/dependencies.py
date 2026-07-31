from functools import lru_cache

from app.core.config import get_settings
from app.domain.backtests.service import BacktestService
from app.domain.projects.services import ProjectService
from app.domain.strategies.service import StrategyService
from app.infrastructure.backtests import BacktraderStrategyBacktestEngine
from app.infrastructure.db import (
    SQLAlchemyProjectRepository,
    SQLAlchemyStrategyRepository,
)
from app.infrastructure.db.schema import ensure_database_schema
from app.infrastructure.db.session import make_engine, make_session_factory


@lru_cache
def get_database_session_factory():
    settings = get_settings()
    ensure_database_schema(settings)
    engine = make_engine(settings)
    return make_session_factory(engine)


@lru_cache
def get_strategy_service() -> StrategyService:
    return StrategyService(SQLAlchemyStrategyRepository(get_database_session_factory()))


@lru_cache
def get_backtest_service() -> BacktestService:
    return BacktestService(SQLAlchemyStrategyRepository(get_database_session_factory()))


@lru_cache
def get_project_service() -> ProjectService:
    return ProjectService(SQLAlchemyProjectRepository(get_database_session_factory()))


@lru_cache
def get_strategy_backtest_engine() -> BacktraderStrategyBacktestEngine:
    return BacktraderStrategyBacktestEngine()
