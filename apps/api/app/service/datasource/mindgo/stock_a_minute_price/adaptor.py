from __future__ import annotations

import json
import math
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Protocol

import pandas as pd

from app.core.config import get_settings
from app.schema.dataset.taxonomy import (
    DatasetAssetClass,
    DatasetFrequency,
    DatasetMarket,
    category_path,
    category_path_en,
    dataset_name_en,
    dataset_name_zh,
)
from app.schema.mindgo import (
    MindgoFieldSpec,
    MindgoParameterOption,
    MindgoParameterSpec,
    MindgoSourceQueryRequest,
    MindgoSourceSchema,
    MindgoSourceStorageSpec,
    MindgoSourceSyncRequest,
    MindgoSourceSyncResult,
    MindgoSourceSyncSpec,
    MindgoSourceSyncWriteMode,
)
from app.service.datasource.mindgo.jupyter_runner import MindgoJupyterRunner
from app.service.datasource.mindgo.stock_a_minute_price.constants import (
    STOCK_A_MINUTE_PRICE_SOURCE_ID,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage, mindgo_source_partition_path
from app.storage import (
    DuckDBParquetStore,
    DuckDBViewStore,
    DuckDBViewStoreError,
    ParquetWriteOptions,
    duckdb_dataset_path,
)

STOCK_A_MINUTE_PRICE_MARKER_START = "MINDGO_STOCK_A_MINUTE_PRICE_JSON_START"
STOCK_A_MINUTE_PRICE_MARKER_END = "MINDGO_STOCK_A_MINUTE_PRICE_JSON_END"
STOCK_A_MINUTE_PRICE_FIELDS = [
    ("symbol", "股票代码", "string"),
    ("trade_date", "时间", "date"),
    ("open", "开盘价", "number"),
    ("high", "最高价", "number"),
    ("low", "最低价", "number"),
    ("close", "收盘价", "number"),
    ("volume", "成交量", "number"),
]
DEFAULT_QUERY_FIELDS = [
    name for name, _, _ in STOCK_A_MINUTE_PRICE_FIELDS if name not in {"symbol", "trade_date"}
]
RAW_TO_STANDARD_FIELD = {
    "symbol": "symbol",
    "security": "symbol",
    "securities": "symbol",
    "code": "symbol",
    "股票代码": "symbol",
    "证券代码": "symbol",
    "同花顺代码": "symbol",
    "trade_date": "trade_date",
    "datetime": "trade_date",
    "date": "trade_date",
    "time": "trade_date",
    "trade_time": "trade_date",
    "时间": "trade_date",
    "日期": "trade_date",
    "open": "open",
    "开盘价": "open",
    "high": "high",
    "最高价": "high",
    "low": "low",
    "最低价": "low",
    "close": "close",
    "收盘价": "close",
    "factor": "factor",
    "复权因子": "factor",
    "volume": "volume",
    "成交量": "volume",
    "turnover": "turnover",
    "成交金额(元)": "turnover",
    "成交额": "turnover",
    "turnover_rate": "turnover_rate",
    "换手率(%)": "turnover_rate",
    "换手率": "turnover_rate",
    "is_paused": "is_paused",
    "是否停牌": "is_paused",
}
STANDARD_FIELD_NAMES = {name for name, _, _ in STOCK_A_MINUTE_PRICE_FIELDS}
TIME_FIELD_NAMES = {"trade_date", "datetime", "date", "time", "trade_time", "时间", "日期"}


@dataclass(frozen=True)
class MindgoPartitionedParquetWrite:
    source_id: str
    partition_values: Mapping[str, str]
    path: Path
    request: MindgoSourceSyncRequest
    options: ParquetWriteOptions


class MindgoSyncWriter(Protocol):
    async def write(
        self,
        write: MindgoPartitionedParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        """Write one MindGo dataset partition and return persisted row count."""


class DuckDBParquetMindgoSyncWriter:
    def __init__(self, store: DuckDBParquetStore | None = None) -> None:
        self._store = store or DuckDBParquetStore()

    async def write(
        self,
        write: MindgoPartitionedParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        if write.request.write_mode == MindgoSourceSyncWriteMode.SKIP and write.path.exists():
            return 0
        return self._store.write(frame, write.path, options=write.options)


class StockAMinutePriceAdapter:
    source_id = STOCK_A_MINUTE_PRICE_SOURCE_ID

    def __init__(
        self,
        runner: MindgoJupyterRunner | None = None,
        *,
        sync_writer: MindgoSyncWriter | None = None,
        storage: MindgoSourceStorage | None = None,
        storage_root: Path | str | None = None,
        parquet_root: Path | str | None = None,
    ) -> None:
        if storage is not None and (storage_root is not None or parquet_root is not None):
            raise ValueError("storage cannot be combined with storage_root or parquet_root")
        self._runner = runner
        self._sync_writer = sync_writer or DuckDBParquetMindgoSyncWriter()
        root = storage_root if storage_root is not None else parquet_root
        if storage is not None:
            self._storage = storage
        elif root is not None:
            self._storage = MindgoSourceStorage(root)
        else:
            self._storage = MindgoSourceStorage()

    async def get_source_schema(self) -> MindgoSourceSchema:
        return stock_a_minute_price_schema(self._storage)

    async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")

        payload = await self._runner.run_json(
            stock_a_minute_price_remote_code(_query_params(request)),
            marker_start=STOCK_A_MINUTE_PRICE_MARKER_START,
            marker_end=STOCK_A_MINUTE_PRICE_MARKER_END,
        )
        if payload.get("error"):
            raise RuntimeError(
                "Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False)
            )
        return normalize_stock_a_minute_price(payload.get("data"))

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        started_at = time.perf_counter()
        query_request = MindgoSourceQueryRequest(
            params={
                **request.params,
                "start_date": request.start_date.isoformat(),
                "end_date": request.end_date.isoformat(),
                "bar_count": 0,
            }
        )
        frame = await self.query_from_mindgo(query_request)
        synced_count = await self._write_partitions(request, frame, request.start_date)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return MindgoSourceSyncResult(
            status="success",
            elapsed_ms=elapsed_ms,
            synced_count=synced_count,
        )

    async def _write_partitions(
        self,
        request: MindgoSourceSyncRequest,
        frame: pd.DataFrame,
        fallback_date: date,
    ) -> int:
        synced_count = 0
        for partition_date, partition_frame in _daily_partitions(frame, fallback_date):
            write = MindgoPartitionedParquetWrite(
                source_id=self.source_id,
                partition_values={"trade_day": partition_date},
                path=self._storage.partition_path(
                    self.source_id,
                    {"trade_day": partition_date},
                ),
                request=request,
                options=ParquetWriteOptions(order_by=["trade_date", "symbol"]),
            )
            synced_count += await self._sync_writer.write(write, partition_frame)
        return synced_count


def stock_a_minute_price_schema(
    storage: MindgoSourceStorage | None = None,
) -> MindgoSourceSchema:
    storage = storage or MindgoSourceStorage()
    partitioned_by = ["trade_day"]
    partition_summary = storage.partition_summary(
        STOCK_A_MINUTE_PRICE_SOURCE_ID,
        partitioned_by,
    )
    market = DatasetMarket.A
    asset_class = DatasetAssetClass.STOCK
    frequency = DatasetFrequency.MINUTE
    topic_zh = "行情数据"
    topic_en = "price"
    name_zh = dataset_name_zh(market, asset_class, frequency, topic_zh)
    security_options = _snapshot_info_security_options()
    return MindgoSourceSchema(
        name=name_zh,
        name_zh=name_zh,
        name_en=dataset_name_en(market, asset_class, frequency, topic_en),
        category_path=category_path(market, asset_class, frequency, topic_zh),
        category_path_en=category_path_en(market, asset_class, frequency, topic_en),
        description="A股股票分钟级历史行情数据",
        mindgo_function="get_price",
        storage=MindgoSourceStorageSpec(
            path=storage.source_root(STOCK_A_MINUTE_PRICE_SOURCE_ID).as_posix(),
            format="parquet",
            partitioned_by=partitioned_by,
            min_partition=partition_summary.min_partition,
            max_partition=partition_summary.max_partition,
            partition_count=partition_summary.partition_count,
        ),
        sync=MindgoSourceSyncSpec(
            supports_query_window=True,
            min_start_offset_days=-20000,
            max_end_offset_days=0,
        ),
        query_params=[
            MindgoParameterSpec(
                name="securities",
                label="标的代码",
                value_type="string[]",
                required=True,
                default=[symbol for symbol, _ in security_options],
                options=[
                    MindgoParameterOption(label=label, value=symbol)
                    for symbol, label in security_options
                ],
                description="从 a_stock_snapshot_info 维表读取 A 股股票代码和名称。",
            ),
            MindgoParameterSpec(
                name="start_date",
                label="起始时间",
                value_type="string",
                required=False,
                description="支持日期或日期时间，例如 2023-02-01 09:30。",
            ),
            MindgoParameterSpec(
                name="end_date",
                label="结束时间",
                value_type="string",
                required=False,
                description="支持日期或日期时间，例如 2023-02-01 10:59。",
            ),
            MindgoParameterSpec(
                name="fields",
                label="数据字段",
                value_type="string[]",
                required=False,
                default=DEFAULT_QUERY_FIELDS,
                options=[
                    MindgoParameterOption(label=label, value=name)
                    for name, label, _ in STOCK_A_MINUTE_PRICE_FIELDS
                    if name not in {"symbol", "trade_date"}
                ],
            ),
            MindgoParameterSpec(
                name="fq",
                label="复权选项",
                value_type="enum",
                required=False,
                default="none",
                options=[
                    MindgoParameterOption(label="不复权", value="none"),
                    MindgoParameterOption(label="前复权", value="pre"),
                    MindgoParameterOption(label="后复权", value="post"),
                ],
            ),
            MindgoParameterSpec(
                name="skip_paused",
                label="跳过停牌",
                value_type="boolean",
                required=False,
                default=False,
            ),
            MindgoParameterSpec(
                name="bar_count",
                label="历史长度",
                value_type="integer",
                required=False,
                default=0,
                description="bar_count 不为 0 时 start_date 必须为空。",
            ),
        ],
        result_schema=[
            MindgoFieldSpec(
                name=name,
                label=label,
                value_type=value_type,
                required=name in {"symbol", "trade_date"},
            )
            for name, label, value_type in STOCK_A_MINUTE_PRICE_FIELDS
        ],
    )


def stock_a_minute_price_remote_code(params: dict[str, Any]) -> str:
    params_json = json.dumps(params, ensure_ascii=False, sort_keys=True)
    return f"""
import json
import math
import traceback
from datetime import datetime

PARAMS_JSON = {params_json!r}
PARAMS = json.loads(PARAMS_JSON)
FIELDS = {json.dumps(DEFAULT_QUERY_FIELDS, ensure_ascii=False)}
KNOWN_FIELDS = set(FIELDS)
MARKER_START = {json.dumps(STOCK_A_MINUTE_PRICE_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_MINUTE_PRICE_MARKER_END)}


def jsonable(value):
    if value is None:
        return None
    try:
        import pandas as pd
        if pd.isna(value):
            return None
    except Exception:
        pass
    try:
        value = value.item()
    except Exception:
        pass
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {{str(k): jsonable(v) for k, v in value.items()}}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return str(value)


def datetime_text(value):
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        text = str(int(value))
    else:
        text = str(value).strip()
    if text.isdigit():
        formats = {{
            8: "%Y%m%d",
            12: "%Y%m%d%H%M",
            14: "%Y%m%d%H%M%S",
        }}
        if len(text) in formats:
            try:
                import pandas as pd
                return pd.to_datetime(text, format=formats[len(text)]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception:
                pass
    try:
        import pandas as pd
        timestamp = pd.to_datetime(value)
        if pd.isna(timestamp):
            return None
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return text


def normalize_securities(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return value


def securities_symbols(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return []


def mindgo_datetime(value):
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip().replace("T", " ")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return datetime.strptime(text[:10], "%Y-%m-%d")


def frame_records(frame, symbol=None, field_name=None):
    working = frame.copy()
    if not any(
        name in working.columns
        for name in ("trade_date", "datetime", "date", "time", "trade_time")
    ):
        working = working.reset_index()
        working = working.rename(columns={{str(working.columns[0]): "trade_date"}})
    rows = []
    for raw_row in working.to_dict(orient="records"):
        row = {{str(key): jsonable(value) for key, value in raw_row.items()}}
        for time_key in ("datetime", "date", "time", "trade_time"):
            if time_key in row and "trade_date" not in row:
                row["trade_date"] = row.pop(time_key)
                break
        if row.get("trade_date") is not None:
            row["trade_date"] = datetime_text(row["trade_date"])
        if symbol is not None:
            row.setdefault("symbol", symbol)
        if field_name and "value" in row:
            row[field_name] = row.pop("value")
        rows.append(row)
    return rows


def looks_like_panel(value):
    if not isinstance(value, dict):
        return False
    return any(
        str(key) in KNOWN_FIELDS and hasattr(child, "to_dict")
        for key, child in value.items()
    )


def panel_records(value):
    by_key = {{}}
    for field_name, frame in value.items():
        field_name = str(field_name)
        if field_name not in KNOWN_FIELDS or not hasattr(frame, "copy"):
            continue
        working = frame.copy().reset_index()
        time_column = str(working.columns[0])
        for raw_row in working.to_dict(orient="records"):
            trade_date = datetime_text(raw_row.get(time_column))
            for symbol, field_value in raw_row.items():
                symbol = str(symbol)
                if symbol == time_column:
                    continue
                key = (trade_date, symbol)
                row = by_key.setdefault(
                    key, {{"trade_date": trade_date, "symbol": symbol}}
                )
                row[field_name] = jsonable(field_value)
    return list(by_key.values())


def normalize_result(value, securities):
    if value is None:
        return []
    if hasattr(value, "to_dict"):
        symbols = securities_symbols(securities)
        symbol = symbols[0] if len(symbols) == 1 else None
        return frame_records(value, symbol=symbol)
    if looks_like_panel(value):
        return panel_records(value)
    if isinstance(value, dict):
        rows = []
        for symbol, item in value.items():
            if hasattr(item, "to_dict"):
                rows.extend(frame_records(item, symbol=str(symbol)))
            elif isinstance(item, list):
                for row in item:
                    if isinstance(row, dict):
                        normalized = {{str(key): jsonable(val) for key, val in row.items()}}
                        normalized.setdefault("symbol", str(symbol))
                        rows.append(normalized)
            elif isinstance(item, dict):
                normalized = {{str(key): jsonable(val) for key, val in item.items()}}
                normalized.setdefault("symbol", str(symbol))
                rows.append(normalized)
        return rows
    if isinstance(value, list):
        return [
            {{str(key): jsonable(val) for key, val in row.items()}}
            for row in value
            if isinstance(row, dict)
        ]
    return []


payload = {{"data": None}}
try:
    call_params = dict(PARAMS)
    securities = normalize_securities(call_params.get("securities"))
    fields = call_params.get("fields") or FIELDS
    fq = call_params.get("fq", "none")
    if fq == "none":
        fq = None
    get_price_params = dict(
        start_date=mindgo_datetime(call_params.get("start_date")),
        end_date=mindgo_datetime(call_params.get("end_date")),
        fre_step="1m",
        fields=fields,
        skip_paused=bool(call_params.get("skip_paused", False)),
        fq=fq,
        is_panel=False,
    )
    bar_count = int(call_params.get("bar_count") or 0)
    if bar_count > 0:
        get_price_params["bar_count"] = bar_count
    # MindGo's minute endpoint can time out when too many securities are
    # requested in one call. Fetch in bounded batches and merge the rows.
    security_list = securities if isinstance(securities, (list, tuple)) else [securities]
    rows = []
    batch_size = 20
    for offset in range(0, len(security_list), batch_size):
        batch = security_list[offset:offset + batch_size]
        value = get_price(batch, **get_price_params)
        rows.extend(normalize_result(value, batch))
    payload["data"] = rows
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=8)

print(MARKER_START)
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print(MARKER_END)
"""


def normalize_stock_a_minute_price(value: Any) -> pd.DataFrame:
    if value is None:
        return _stock_a_minute_price_frame([])
    if isinstance(value, pd.DataFrame):
        return _normalize_frame(value)
    if isinstance(value, dict):
        if _looks_like_panel_dict(value):
            return _normalize_panel_dict(value)
        return _normalize_dict(value)
    if isinstance(value, list):
        return _stock_a_minute_price_frame(
            [_normalize_row(row) for row in value if isinstance(row, dict)]
        )
    raise TypeError(f"Unsupported MindGo stock minute result type: {type(value).__name__}")


def _query_params(request: MindgoSourceQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    if not params.get("securities"):
        params["securities"] = _snapshot_info_securities()
    params.setdefault("fields", DEFAULT_QUERY_FIELDS)
    params.setdefault("fq", "none")
    params.setdefault("skip_paused", False)
    params.setdefault("bar_count", 0)
    return params


def _daily_partitions(frame: pd.DataFrame, fallback_date: date) -> list[tuple[str, pd.DataFrame]]:
    working = frame.copy()
    fallback_trade_day = fallback_date.strftime("%Y%m%d")
    if "trade_date" not in working.columns:
        working["trade_date"] = f"{fallback_trade_day} 00:00:00"
    working["trade_date"] = working["trade_date"].map(_datetime_text)
    working["trade_day"] = working["trade_date"].map(_trade_day_text).fillna(fallback_trade_day)
    if working.empty:
        return [(fallback_trade_day, working.drop(columns=["trade_day"]))]
    return [
        (str(trade_day), partition.drop(columns=["trade_day"]).reset_index(drop=True))
        for trade_day, partition in working.groupby("trade_day", sort=True, dropna=False)
    ]


def mindgo_parquet_partition_path(
    storage_root: Path | str,
    source_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    return mindgo_source_partition_path(storage_root, source_id, partition_values)


def _normalize_dict(value: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for symbol, item in value.items():
        if isinstance(item, pd.DataFrame):
            for row in _frame_to_rows(item):
                row["symbol"] = str(symbol)
                rows.append(row)
        elif isinstance(item, list):
            for row in item:
                if isinstance(row, dict):
                    normalized = _normalize_row(row)
                    normalized.setdefault("symbol", str(symbol))
                    rows.append(normalized)
        elif isinstance(item, dict):
            normalized = _normalize_row(item)
            normalized.setdefault("symbol", str(symbol))
            rows.append(normalized)
    return _stock_a_minute_price_frame(rows)


def _looks_like_panel_dict(value: dict[str, Any]) -> bool:
    return any(
        str(key) in STANDARD_FIELD_NAMES and isinstance(item, pd.DataFrame)
        for key, item in value.items()
    )


def _normalize_panel_dict(value: dict[str, Any]) -> pd.DataFrame:
    rows_by_key: dict[tuple[str | None, str], dict[str, Any]] = {}
    for field_name, frame in value.items():
        field_name = RAW_TO_STANDARD_FIELD.get(str(field_name), str(field_name))
        if field_name not in STANDARD_FIELD_NAMES or not isinstance(frame, pd.DataFrame):
            continue
        working = frame.reset_index()
        time_column = str(working.columns[0])
        for raw_row in working.to_dict(orient="records"):
            trade_date = _datetime_text(raw_row.get(time_column))
            for symbol, field_value in raw_row.items():
                symbol = str(symbol)
                if symbol == time_column:
                    continue
                key = (trade_date, symbol)
                row = rows_by_key.setdefault(
                    key,
                    {"trade_date": trade_date, "symbol": symbol},
                )
                row[field_name] = _json_scalar(field_value)
    return _stock_a_minute_price_frame(list(rows_by_key.values()))


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _stock_a_minute_price_frame(_frame_to_rows(frame))


def _frame_to_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    working = frame.copy()
    if not any(str(column) in TIME_FIELD_NAMES for column in working.columns):
        working = working.reset_index()
        index_column = str(working.columns[0])
        working = working.rename(columns={index_column: "trade_date"})
    for row in working.to_dict(orient="records"):
        rows.append(_normalize_row(row))
    return rows


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        RAW_TO_STANDARD_FIELD.get(str(key), str(key)): _json_scalar(value)
        for key, value in row.items()
        if str(key) in RAW_TO_STANDARD_FIELD or str(key) in STANDARD_FIELD_NAMES
    }
    if "trade_date" in normalized:
        normalized["trade_date"] = _datetime_text(normalized["trade_date"])
    if "symbol" in normalized and normalized["symbol"] is not None:
        normalized["symbol"] = str(normalized["symbol"])
    return normalized


def _stock_a_minute_price_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    columns = [name for name, _, _ in STOCK_A_MINUTE_PRICE_FIELDS]
    for column in columns:
        if column not in frame.columns:
            frame[column] = pd.NA
    return frame[columns]


def _json_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list | tuple):
        return [_json_scalar(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_scalar(item) for key, item in value.items()}
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _datetime_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        text = str(int(value))
    else:
        text = str(value).strip()
    if text.isdigit():
        formats = {
            8: "%Y%m%d",
            12: "%Y%m%d%H%M",
            14: "%Y%m%d%H%M%S",
        }
        if len(text) in formats:
            try:
                return pd.to_datetime(text, format=formats[len(text)]).strftime("%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError):
                return None
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return None
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def _trade_day_text(value: Any) -> str | None:
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return None
    return timestamp.strftime("%Y%m%d")


def _snapshot_info_security_options() -> list[tuple[str, str]]:
    try:
        frame = _snapshot_info_frame()
    except RuntimeError:
        return []
    if "symbol" not in frame.columns:
        return []
    options: list[tuple[str, str]] = []
    seen: set[str] = set()
    for record in frame.to_dict(orient="records"):
        symbol = _normalize_security_symbol(record.get("symbol"))
        if not symbol or symbol in seen:
            continue
        name = str(record.get("name") or "").strip()
        options.append((symbol, f"{name} {symbol}".strip() if name else symbol))
        seen.add(symbol)
    return options


def _snapshot_info_securities() -> list[str]:
    options = _snapshot_info_security_options()
    if not options:
        raise RuntimeError(
            "a_stock_snapshot_info dataset is unavailable or contains no stock symbols"
        )
    return [symbol for symbol, _ in options]


def _snapshot_info_frame() -> pd.DataFrame:
    try:
        return DuckDBViewStore(duckdb_dataset_path(get_settings().database_path)).query_frame(
            "SELECT * FROM a_stock_snapshot_info"
        )
    except DuckDBViewStoreError as exc:
        raise RuntimeError("a_stock_snapshot_info dataset is unavailable: " + str(exc)) from exc


def _normalize_security_symbol(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    symbol = str(value).strip().upper()
    return symbol or None
