from __future__ import annotations

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.backtests.models import (
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
)
from app.domain.strategies.models import (
    StrategyRecord,
    StrategyStatus,
    StrategyVersionRecord,
)
from app.infrastructure.db.models import (
    StrategyBacktestResultRow,
    StrategyBacktestRow,
    StrategyRow,
    StrategyVersionRow,
)


class SQLAlchemyStrategyRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def clear(self) -> None:
        async with self._session_factory() as db:
            await db.execute(delete(StrategyBacktestResultRow))
            await db.execute(delete(StrategyBacktestRow))
            await db.execute(delete(StrategyVersionRow))
            await db.execute(delete(StrategyRow))
            await db.commit()

    async def add_strategy(self, strategy: StrategyRecord) -> None:
        await self.save_strategy(strategy)

    async def save_strategy(self, strategy: StrategyRecord) -> None:
        async with self._session_factory() as db:
            await db.merge(_strategy_to_row(strategy))
            await db.commit()

    async def get_strategy(self, strategy_id: str) -> StrategyRecord | None:
        async with self._session_factory() as db:
            row = await db.get(StrategyRow, strategy_id)
            return _strategy_from_row(row) if row is not None else None

    async def list_strategies(self, user_id: str, project_id: str) -> list[StrategyRecord]:
        async with self._session_factory() as db:
            result = await db.scalars(
                select(StrategyRow)
                .where(
                    StrategyRow.user_id == user_id,
                    StrategyRow.project_id == project_id,
                    StrategyRow.status != StrategyStatus.DELETED.value,
                )
                .order_by(StrategyRow.updated_at.desc())
            )
            return [_strategy_from_row(row) for row in result.all()]

    async def add_version(self, version: StrategyVersionRecord) -> None:
        await self.save_version(version)

    async def save_version(self, version: StrategyVersionRecord) -> None:
        async with self._session_factory() as db:
            await db.merge(_version_to_row(version))
            await db.commit()

    async def get_version(self, version_id: str) -> StrategyVersionRecord | None:
        async with self._session_factory() as db:
            row = await db.get(StrategyVersionRow, version_id)
            return _version_from_row(row) if row is not None else None

    async def list_versions(self, strategy_id: str) -> list[StrategyVersionRecord]:
        async with self._session_factory() as db:
            result = await db.scalars(
                select(StrategyVersionRow)
                .where(StrategyVersionRow.strategy_id == strategy_id)
                .order_by(StrategyVersionRow.version.asc())
            )
            return [_version_from_row(row) for row in result.all()]

    async def next_version_number(self, strategy_id: str) -> int:
        async with self._session_factory() as db:
            max_version = await db.scalar(
                select(func.coalesce(func.max(StrategyVersionRow.version), 0)).where(
                    StrategyVersionRow.strategy_id == strategy_id
                )
            )
            return int(max_version or 0) + 1

    async def add_backtest(self, backtest: StrategyBacktestRecord) -> None:
        await self.save_backtest(backtest)

    async def save_backtest(self, backtest: StrategyBacktestRecord) -> None:
        async with self._session_factory() as db:
            await db.merge(_backtest_to_row(backtest))
            await db.commit()

    async def get_backtest(self, backtest_id: str) -> StrategyBacktestRecord | None:
        async with self._session_factory() as db:
            row = await db.get(StrategyBacktestRow, backtest_id)
            return _backtest_from_row(row) if row is not None else None

    async def list_backtests(
        self,
        *,
        strategy_version_id: str | None,
        limit: int,
    ) -> list[StrategyBacktestRecord]:
        filters = []
        if strategy_version_id is not None:
            filters.append(StrategyBacktestRow.strategy_version_id == strategy_version_id)
        async with self._session_factory() as db:
            result = await db.scalars(
                select(StrategyBacktestRow)
                .where(*filters)
                .order_by(StrategyBacktestRow.created_at.desc())
                .limit(limit)
            )
            return [_backtest_from_row(row) for row in result.all()]

    async def save_backtest_result(self, result: StrategyBacktestResultRecord) -> None:
        async with self._session_factory() as db:
            await db.merge(_backtest_result_to_row(result))
            await db.commit()

    async def get_backtest_result(
        self,
        backtest_id: str,
    ) -> StrategyBacktestResultRecord | None:
        async with self._session_factory() as db:
            row = await db.scalar(
                select(StrategyBacktestResultRow).where(
                    StrategyBacktestResultRow.strategy_backtest_id == backtest_id
                )
            )
            return _backtest_result_from_row(row) if row is not None else None


def _strategy_to_row(strategy: StrategyRecord) -> StrategyRow:
    return StrategyRow(
        id=strategy.id,
        user_id=strategy.user_id,
        project_id=strategy.project_id,
        chat_session_id=strategy.chat_session_id,
        source_sdk_message_uuid=strategy.source_sdk_message_uuid,
        name=strategy.name,
        description=strategy.description,
        strategy_type=strategy.strategy_type,
        tags_json=list(strategy.tags),
        current_version_id=strategy.current_version_id,
        status=strategy.status.value,
        created_at=strategy.created_at,
        updated_at=strategy.updated_at,
        payload_json=strategy.model_dump(mode="json"),
    )


def _strategy_from_row(row: StrategyRow) -> StrategyRecord:
    return StrategyRecord.model_validate(row.payload_json)


def _version_to_row(version: StrategyVersionRecord) -> StrategyVersionRow:
    return StrategyVersionRow(
        id=version.id,
        strategy_id=version.strategy_id,
        version=version.version,
        version_name=version.version_name,
        parent_version_id=version.parent_version_id,
        code_artifact_id=version.code_artifact_id,
        entrypoint=version.entrypoint,
        params_schema_json={
            key: value.model_dump(mode="json") for key, value in version.params_schema.items()
        },
        default_params_json=dict(version.default_params),
        logic_summary=version.logic_summary,
        change_summary=version.change_summary,
        source_sdk_session_id=version.source_sdk_session_id,
        source_sdk_message_uuid=version.source_sdk_message_uuid,
        source_sdk_tool_use_id=version.source_sdk_tool_use_id,
        code_checksum=version.code_checksum,
        status=version.status.value,
        created_at=version.created_at,
        payload_json=version.model_dump(mode="json"),
    )


def _version_from_row(row: StrategyVersionRow) -> StrategyVersionRecord:
    return StrategyVersionRecord.model_validate(row.payload_json)


def _backtest_to_row(backtest: StrategyBacktestRecord) -> StrategyBacktestRow:
    return StrategyBacktestRow(
        id=backtest.id,
        user_id=backtest.user_id,
        project_id=backtest.project_id,
        chat_session_id=backtest.chat_session_id,
        strategy_id=backtest.strategy_id,
        strategy_version_id=backtest.strategy_version_id,
        run_type="backtest",
        status=backtest.status.value,
        config_hash=backtest.config_hash,
        result_id=backtest.result_id,
        started_at=backtest.started_at,
        completed_at=backtest.completed_at,
        created_at=backtest.created_at,
        updated_at=backtest.updated_at,
        payload_json=backtest.model_dump(mode="json"),
    )


def _backtest_from_row(row: StrategyBacktestRow) -> StrategyBacktestRecord:
    return StrategyBacktestRecord.model_validate(row.payload_json)


def _backtest_result_to_row(result: StrategyBacktestResultRecord) -> StrategyBacktestResultRow:
    return StrategyBacktestResultRow(
        id=result.id,
        strategy_backtest_id=result.strategy_backtest_id,
        created_at=result.created_at,
        payload_json=result.model_dump(mode="json"),
    )


def _backtest_result_from_row(row: StrategyBacktestResultRow) -> StrategyBacktestResultRecord:
    return StrategyBacktestResultRecord.model_validate(row.payload_json)
