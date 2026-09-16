from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from app.core.config import get_settings
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path


class MarketDataError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


@dataclass(frozen=True)
class DatasetMarketDataConfig:
    dataset_id: str
    symbol_field: str
    datetime_field: str
    open_field: str
    high_field: str
    low_field: str
    close_field: str
    volume_field: str


@dataclass(frozen=True)
class DatasetBenchmarkConfig:
    dataset_id: str
    symbol_field: str
    datetime_field: str
    close_field: str


@dataclass(frozen=True)
class DatasetMarketDataResult:
    frame: pd.DataFrame
    dataset_name: str


def load_market(
    *,
    symbol: str,
    start_date: date | None = None,
    end_date: date | None = None,
    end_time: datetime | None = None,
    lookback_bars: int | None = None,
) -> DatasetMarketDataResult:
    return _load_market_frame(
        symbol=symbol,
        config_key="market_data_dataset",
        start_date=start_date,
        end_date=end_date,
        end_time=end_time,
        lookback_bars=lookback_bars,
    )


def load_benchmark(
    *,
    symbol: str,
    start_date: date,
    end_date: date,
) -> DatasetMarketDataResult | None:
    if not symbol:
        return None
    return _load_benchmark_frame(
        symbol=symbol,
        config_key="benchmark_dataset",
        start_date=start_date,
        end_date=end_date,
    )


def _load_market_frame(
    *,
    symbol: str,
    config_key: str,
    start_date: date | None,
    end_date: date | None,
    end_time: datetime | None,
    lookback_bars: int | None,
) -> DatasetMarketDataResult:
    if lookback_bars is None:
        if start_date is None or end_date is None:
            raise MarketDataError(
                "MARKET_DATA_WINDOW_INVALID",
                "start_date and end_date are required for range market data loading",
            )
    elif lookback_bars <= 0:
        raise MarketDataError(
            "MARKET_DATA_LOOKBACK_INVALID",
            "lookback_bars must be greater than zero",
            detail={"lookback_bars": lookback_bars},
        )
    elif end_time is None:
        raise MarketDataError(
            "MARKET_DATA_WINDOW_INVALID",
            "end_time is required for lookback market data loading",
        )

    settings = get_settings()
    config = _market_config(_settings_dataset_config(settings, config_key))
    dataset_name = _require_dataset_name(settings.database_path, config.dataset_id)
    _validate_dataset_fields(
        settings.database_path,
        dataset_id=config.dataset_id,
        dataset_name=dataset_name,
        mapping={
            "symbol": config.symbol_field,
            "datetime": config.datetime_field,
            "open": config.open_field,
            "high": config.high_field,
            "low": config.low_field,
            "close": config.close_field,
            "volume": config.volume_field,
        },
    )
    if lookback_bars is not None and end_time is not None:
        sql = _market_data_lookback_sql(
            view_name=dataset_name,
            symbol=symbol,
            end_time=end_time,
            lookback_bars=lookback_bars,
            config=config,
        )
    else:
        if start_date is None or end_date is None:
            raise MarketDataError(
                "MARKET_DATA_WINDOW_INVALID",
                "start_date and end_date are required for range market data loading",
            )
        sql = _market_data_sql(
            view_name=dataset_name,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            config=config,
        )
    raw_frame = _query_dataset_frame(settings.database_path, sql, config.dataset_id)
    frame = _normalize_dataset_market_frame(raw_frame, symbol=symbol)
    return DatasetMarketDataResult(frame=frame, dataset_name=dataset_name)


def _load_benchmark_frame(
    *,
    symbol: str,
    config_key: str,
    start_date: date,
    end_date: date,
) -> DatasetMarketDataResult:
    settings = get_settings()
    config = _benchmark_config(_settings_dataset_config(settings, config_key))
    dataset_name = _require_dataset_name(settings.database_path, config.dataset_id)
    _validate_dataset_fields(
        settings.database_path,
        dataset_id=config.dataset_id,
        dataset_name=dataset_name,
        mapping={
            "symbol": config.symbol_field,
            "datetime": config.datetime_field,
            "close": config.close_field,
        },
    )
    sql = _benchmark_sql(
        view_name=dataset_name,
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        config=config,
    )
    raw_frame = _query_dataset_frame(settings.database_path, sql, config.dataset_id)
    frame = _normalize_dataset_benchmark_frame(raw_frame, symbol=symbol)
    return DatasetMarketDataResult(frame=frame, dataset_name=dataset_name)


def market_data_source_metadata(symbols: list[str]) -> dict[str, object]:
    settings = get_settings()
    market_config = _market_config(settings.market_data_dataset)
    benchmark_config = _optional_benchmark_config(settings.benchmark_dataset)
    market_data_dataset_name = _dataset_name_or_none(
        settings.database_path,
        market_config.dataset_id,
    )
    benchmark_dataset_id = benchmark_config.dataset_id if benchmark_config is not None else ""
    benchmark_dataset_name = (
        _dataset_name_or_none(settings.database_path, benchmark_dataset_id)
        if benchmark_dataset_id
        else None
    )
    return {
        "mode": "dataset",
        "symbols": symbols,
        "market_data_dataset": {
            "dataset_id": market_config.dataset_id,
            "dataset_name": market_data_dataset_name,
            "field_mapping": {
                "symbol": market_config.symbol_field,
                "datetime": market_config.datetime_field,
                "open": market_config.open_field,
                "high": market_config.high_field,
                "low": market_config.low_field,
                "close": market_config.close_field,
                "volume": market_config.volume_field,
            },
        },
        "benchmark_dataset": {
            "dataset_id": benchmark_dataset_id,
            "dataset_name": benchmark_dataset_name,
            "field_mapping": {
                "symbol": benchmark_config.symbol_field if benchmark_config is not None else "",
                "datetime": (
                    benchmark_config.datetime_field if benchmark_config is not None else ""
                ),
                "close": benchmark_config.close_field if benchmark_config is not None else "",
            },
        },
    }


def _market_config(value: dict[str, object]) -> DatasetMarketDataConfig:
    dataset_id = _required_text(value, "dataset_id", "MARKET_DATA_DATASET_NOT_CONFIGURED")
    return DatasetMarketDataConfig(
        dataset_id=dataset_id,
        symbol_field=_required_text(value, "symbol_field"),
        datetime_field=_required_text(value, "datetime_field"),
        open_field=_required_text(value, "open_field"),
        high_field=_required_text(value, "high_field"),
        low_field=_required_text(value, "low_field"),
        close_field=_required_text(value, "close_field"),
        volume_field=_required_text(value, "volume_field"),
    )


def _settings_dataset_config(settings: object, key: str) -> dict[str, object]:
    value = getattr(settings, key)
    return value if isinstance(value, dict) else {}


def _optional_benchmark_config(value: dict[str, object]) -> DatasetBenchmarkConfig | None:
    try:
        return _benchmark_config(value)
    except MarketDataError:
        return None


def _benchmark_config(value: dict[str, object]) -> DatasetBenchmarkConfig:
    dataset_id = _required_text(value, "dataset_id", "MARKET_DATA_BENCHMARK_NOT_CONFIGURED")
    return DatasetBenchmarkConfig(
        dataset_id=dataset_id,
        symbol_field=_required_text(value, "symbol_field"),
        datetime_field=_required_text(value, "datetime_field"),
        close_field=_required_text(value, "close_field"),
    )


def _required_text(
    value: dict[str, object],
    key: str,
    error_code: str = "BACKTEST_DATASET_MAPPING_INVALID",
) -> str:
    raw_value = value.get(key)
    if isinstance(raw_value, str) and raw_value.strip():
        return raw_value.strip()
    raise MarketDataError(
        error_code,
        "Market data dataset configuration is incomplete",
        detail={"field": key},
    )


def _raw_text(value: dict[str, object], key: str) -> str:
    raw_value = value.get(key)
    return raw_value.strip() if isinstance(raw_value, str) else ""


def _require_dataset_name(database_path: Path, dataset_id: str) -> str:
    dataset_name = _dataset_name_or_none(database_path, dataset_id)
    if dataset_name is None:
        raise MarketDataError(
            "MARKET_DATASET_NOT_FOUND",
            "Market dataset was not found",
            detail={"dataset_id": dataset_id},
        )
    return dataset_name


def _dataset_name_or_none(database_path: Path, dataset_id: str) -> str | None:
    if not database_path.exists():
        return None
    try:
        connection = sqlite3.connect(database_path)
        try:
            row = connection.execute(
                "SELECT name FROM datasets WHERE id = ?",
                (dataset_id,),
            ).fetchone()
        finally:
            connection.close()
    except sqlite3.Error:
        return None
    return str(row[0]) if row is not None else None


def _query_dataset_frame(database_path: Path, sql: str, dataset_id: str) -> pd.DataFrame:
    try:
        return DuckDBViewStore(duckdb_dataset_path(database_path)).query_frame(sql)
    except DuckDBViewStoreError as exc:
        raise MarketDataError(
            "MARKET_DATASET_QUERY_FAILED",
            f"Failed to query market dataset: {exc}",
            detail={"dataset_id": dataset_id},
        ) from exc


def _validate_dataset_fields(
    database_path: Path,
    *,
    dataset_id: str,
    dataset_name: str,
    mapping: dict[str, str],
) -> None:
    columns = _dataset_columns(database_path, dataset_name=dataset_name, dataset_id=dataset_id)
    missing = [
        {"role": role, "field": field} for role, field in mapping.items() if field not in columns
    ]
    if missing:
        raise MarketDataError(
            "MARKET_DATASET_FIELD_NOT_FOUND",
            "Market dataset field mapping references missing columns",
            detail={
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "missing_fields": missing,
                "available_columns": columns,
            },
        )


def _dataset_columns(database_path: Path, *, dataset_name: str, dataset_id: str) -> list[str]:
    frame = _query_dataset_frame(
        database_path,
        f"SELECT * FROM {_quote_identifier(dataset_name)} LIMIT 0",
        dataset_id,
    )
    return [str(column) for column in frame.columns]


def _market_data_sql(
    *,
    view_name: str,
    symbol: str,
    start_date: date,
    end_date: date,
    config: DatasetMarketDataConfig,
) -> str:
    date_expr = _date_expression(config.datetime_field)
    return f"""
        SELECT
            {date_expr} AS datetime,
            {_quote_identifier(config.open_field)} AS open,
            {_quote_identifier(config.high_field)} AS high,
            {_quote_identifier(config.low_field)} AS low,
            {_quote_identifier(config.close_field)} AS close,
            {_quote_identifier(config.volume_field)} AS volume,
            0 AS openinterest
        FROM {_quote_identifier(view_name)}
        WHERE {_quote_identifier(config.symbol_field)} = {_sql_string(symbol)}
          AND {date_expr} BETWEEN DATE {_sql_string(start_date.isoformat())}
                              AND DATE {_sql_string(end_date.isoformat())}
        ORDER BY datetime
    """


def _market_data_lookback_sql(
    *,
    view_name: str,
    symbol: str,
    end_time: datetime,
    lookback_bars: int,
    config: DatasetMarketDataConfig,
) -> str:
    datetime_expr = _datetime_expression(config.datetime_field)
    return f"""
        SELECT * FROM (
            SELECT
                {datetime_expr} AS datetime,
                {_quote_identifier(config.open_field)} AS open,
                {_quote_identifier(config.high_field)} AS high,
                {_quote_identifier(config.low_field)} AS low,
                {_quote_identifier(config.close_field)} AS close,
                {_quote_identifier(config.volume_field)} AS volume,
                0 AS openinterest
            FROM {_quote_identifier(view_name)}
            WHERE {_quote_identifier(config.symbol_field)} = {_sql_string(symbol)}
              AND {datetime_expr} <= TIMESTAMP {_sql_string(end_time.isoformat(sep=" "))}
            ORDER BY datetime DESC
            LIMIT {int(lookback_bars)}
        ) AS recent_bars
        ORDER BY datetime
    """


def _benchmark_sql(
    *,
    view_name: str,
    symbol: str,
    start_date: date,
    end_date: date,
    config: DatasetBenchmarkConfig,
) -> str:
    date_expr = _date_expression(config.datetime_field)
    return f"""
        SELECT
            {date_expr} AS datetime,
            {_quote_identifier(config.close_field)} AS close
        FROM {_quote_identifier(view_name)}
        WHERE {_quote_identifier(config.symbol_field)} = {_sql_string(symbol)}
          AND {date_expr} BETWEEN DATE {_sql_string(start_date.isoformat())}
                              AND DATE {_sql_string(end_date.isoformat())}
        ORDER BY datetime
    """


def _date_expression(field_name: str) -> str:
    field = _quote_identifier(field_name)
    return (
        f"COALESCE(TRY_CAST({field} AS DATE), "
        f"CAST(TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y%m%d') AS DATE), "
        f"CAST(TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y-%m-%d') AS DATE))"
    )


def _datetime_expression(field_name: str) -> str:
    field = _quote_identifier(field_name)
    return (
        f"COALESCE(TRY_CAST({field} AS TIMESTAMP), "
        f"TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y%m%d'), "
        f"TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y%m%d%H%M%S'), "
        f"TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y-%m-%d'), "
        f"TRY_STRPTIME(CAST({field} AS VARCHAR), '%Y-%m-%d %H:%M:%S'))"
    )


def _normalize_dataset_market_frame(raw_frame: pd.DataFrame, *, symbol: str) -> pd.DataFrame:
    required_columns = ["datetime", "open", "high", "low", "close", "volume", "openinterest"]
    missing = [column for column in required_columns if column not in raw_frame.columns]
    if missing:
        raise MarketDataError(
            "MARKET_DATASET_FORMAT_INVALID",
            "Market dataset does not contain required mapped columns",
            detail={"missing_columns": missing, "symbol": symbol},
        )
    frame = raw_frame[required_columns].copy()
    frame["datetime"] = pd.to_datetime(frame["datetime"])
    for column in ["open", "high", "low", "close", "volume", "openinterest"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["datetime", "open", "high", "low", "close", "volume"])
    frame = frame.sort_values("datetime").set_index("datetime")
    if frame.empty:
        raise MarketDataError(
            "MARKET_DATASET_EMPTY",
            f"No market data returned for {symbol}",
            detail={"symbol": symbol},
        )
    return frame[["open", "high", "low", "close", "volume", "openinterest"]]


def _normalize_dataset_benchmark_frame(raw_frame: pd.DataFrame, *, symbol: str) -> pd.DataFrame:
    required_columns = ["datetime", "close"]
    missing = [column for column in required_columns if column not in raw_frame.columns]
    if missing:
        raise MarketDataError(
            "MARKET_BENCHMARK_FORMAT_INVALID",
            "Benchmark dataset does not contain required mapped columns",
            detail={"missing_columns": missing, "symbol": symbol},
        )
    frame = raw_frame[required_columns].copy()
    frame["datetime"] = pd.to_datetime(frame["datetime"])
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame = frame.dropna(subset=["datetime", "close"]).sort_values("datetime").set_index("datetime")
    if frame.empty:
        raise MarketDataError(
            "MARKET_BENCHMARK_EMPTY",
            f"No benchmark data returned for {symbol}",
            detail={"symbol": symbol},
        )
    return frame[["close"]]


def _quote_identifier(identifier: str | None) -> str:
    if not identifier or not identifier.strip():
        raise MarketDataError(
            "MARKET_DATASET_MAPPING_INVALID",
            "Market dataset field mapping contains an empty identifier",
        )
    return '"' + identifier.replace('"', '""') + '"'


def _sql_string(value: Any) -> str:
    return "'" + str(value).replace("'", "''") + "'"
