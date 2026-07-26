from __future__ import annotations

from app.domain.backtests.models import StrategyBacktestDetail, StrategyBacktestRecord
from app.domain.strategies.repository import StrategyRepository


class BacktestError(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


class BacktestService:
    def __init__(self, repository: StrategyRepository) -> None:
        self.repository = repository

    async def list_records(
        self,
        *,
        strategy_version_id: str | None,
        limit: int,
    ) -> list[StrategyBacktestRecord]:
        return await self.repository.list_backtests(
            strategy_version_id=strategy_version_id,
            limit=limit,
        )

    async def get_detail(self, backtest_id: str) -> StrategyBacktestDetail:
        backtest = await self.repository.get_backtest(backtest_id)
        if backtest is None:
            raise BacktestError("BACKTEST_NOT_FOUND", "Backtest record not found", 404)
        return StrategyBacktestDetail(
            backtest=backtest,
            result=await self.repository.get_backtest_result(backtest_id),
        )
