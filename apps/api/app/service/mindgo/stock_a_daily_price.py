from __future__ import annotations

import json
import math
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Protocol

import pandas as pd

from app.schema.mindgo import (
    MindgoDatasetQueryRequest,
    MindgoDatasetSchema,
    MindgoDatasetSyncRequest,
    MindgoDatasetSyncResult,
    MindgoFieldSpec,
    MindgoParameterOption,
    MindgoParameterSpec,
)
from app.service.mindgo.jupyter_runner import MindgoJupyterRunner
from app.storage import DuckDBParquetStore, ParquetWriteOptions

STOCK_A_DAILY_PRICE_DATASET_ID = "stock_a_daily_price"
DEFAULT_MINDGO_PARQUET_ROOT = (
    Path(__file__).resolve().parents[2] / "storage" / "mindgo" / "parquet"
)
STOCK_A_DAILY_PRICE_MARKER_START = "MINDGO_STOCK_A_DAILY_PRICE_JSON_START"
STOCK_A_DAILY_PRICE_MARKER_END = "MINDGO_STOCK_A_DAILY_PRICE_JSON_END"
STOCK_A_DAILY_PRICE_QUERY_ID = "1014"
RAW_1014_COLUMNS = [
    "trade_date",
    "query_id",
    "uid",
    "成交量(日)",
    "成交额(日)",
    "换手(日)",
    "股票代码",
    "收盘价(日)",
    "股票简称",
    "最低价(日)",
    "振幅(日)",
    "涨跌(日)",
    "最高价(日)",
    "开盘价(日)",
]
STOCK_A_DAILY_PRICE_FIELDS = [
    ("symbol", "股票代码", "string"),
    ("trade_date", "交易日", "date"),
    ("name", "股票简称", "string"),
    ("open", "开盘价", "number"),
    ("high", "最高价", "number"),
    ("low", "最低价", "number"),
    ("close", "收盘价", "number"),
    ("volume", "成交量", "number"),
    ("turnover", "成交额", "number"),
    ("turnover_rate", "换手", "number"),
    ("amplitude", "振幅", "number"),
    ("change", "涨跌", "number"),
]
DEFAULT_QUERY_FIELDS = [name for name, _, _ in STOCK_A_DAILY_PRICE_FIELDS]
RAW_TO_STANDARD_FIELD = {
    "股票代码": "symbol",
    "trade_date": "trade_date",
    "股票简称": "name",
    "开盘价(日)": "open",
    "最高价(日)": "high",
    "最低价(日)": "low",
    "收盘价(日)": "close",
    "成交量(日)": "volume",
    "成交额(日)": "turnover",
    "换手(日)": "turnover_rate",
    "振幅(日)": "amplitude",
    "涨跌(日)": "change",
    "uid": "uid",
    "query_id": "query_id",
}
STANDARD_FIELD_NAMES = {name for name, _, _ in STOCK_A_DAILY_PRICE_FIELDS}


@dataclass(frozen=True)
class MindgoPartitionedParquetWrite:
    dataset_id: str
    partition_values: Mapping[str, str]
    path: Path
    request: MindgoDatasetSyncRequest
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
        return self._store.write(frame, write.path, options=write.options)


class StockADailyPriceAdapter:
    dataset_id = STOCK_A_DAILY_PRICE_DATASET_ID

    def __init__(
        self,
        runner: MindgoJupyterRunner | None = None,
        *,
        sync_writer: MindgoSyncWriter | None = None,
        parquet_root: Path | str | None = None,
    ) -> None:
        self._runner = runner
        self._sync_writer = sync_writer or DuckDBParquetMindgoSyncWriter()
        self._parquet_root = Path(parquet_root) if parquet_root else DEFAULT_MINDGO_PARQUET_ROOT

    async def get_schema(self) -> MindgoDatasetSchema:
        return stock_a_daily_price_schema()

    async def query(self, request: MindgoDatasetQueryRequest) -> pd.DataFrame:
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")

        payload = await self._runner.run_json(
            stock_a_daily_price_remote_code(_query_params(request)),
            marker_start=STOCK_A_DAILY_PRICE_MARKER_START,
            marker_end=STOCK_A_DAILY_PRICE_MARKER_END,
        )
        if payload.get("error"):
            raise RuntimeError(
                "Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False)
            )
        return normalize_stock_a_daily_price(payload.get("data"))

    async def sync(self, request: MindgoDatasetSyncRequest) -> MindgoDatasetSyncResult:
        started_at = time.perf_counter()
        synced_count = 0
        for sync_day in _date_range(request.start_date, request.end_date):
            query_request = MindgoDatasetQueryRequest(
                params={
                    **request.params,
                    "start_date": sync_day.isoformat(),
                    "end_date": sync_day.isoformat(),
                }
            )
            frame = await self.query(query_request)
            for partition_date, partition_frame in _daily_partitions(frame, sync_day):
                write = MindgoPartitionedParquetWrite(
                    dataset_id=self.dataset_id,
                    partition_values={"trade_day": partition_date},
                    path=mindgo_parquet_partition_path(
                        self._parquet_root,
                        self.dataset_id,
                        {"trade_day": partition_date},
                    ),
                    request=request,
                    options=ParquetWriteOptions(order_by=["trade_date", "symbol"]),
                )
                synced_count += await self._sync_writer.write(write, partition_frame)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return MindgoDatasetSyncResult(
            status="success",
            elapsed_ms=elapsed_ms,
            synced_count=synced_count,
        )


def stock_a_daily_price_schema() -> MindgoDatasetSchema:
    return MindgoDatasetSchema(
        name="A股历史行情数据(日)",
        category_path=["股票", "A股", "行情数据(A股)"],
        description="A股股票日频历史行情数据",
        mindgo_function="query_index",
        sync_table_name="",
        query_params=[
            MindgoParameterSpec(
                name="start_date",
                label="起始日期",
                value_type="date",
                required=True,
                description="query_index 1014 按单个交易日返回；query 会使用 end_date/base_day。",
            ),
            MindgoParameterSpec(
                name="end_date",
                label="结束日期",
                value_type="date",
                required=True,
            ),
            MindgoParameterSpec(
                name="fields",
                label="数据字段",
                value_type="string[]",
                required=False,
                default=DEFAULT_QUERY_FIELDS,
                options=[
                    MindgoParameterOption(label=label, value=name)
                    for name, label, _ in STOCK_A_DAILY_PRICE_FIELDS
                ],
            ),
        ],
        result_schema=[
            *[
                MindgoFieldSpec(
                    name=name,
                    label=label,
                    value_type=value_type,
                    required=name in {"symbol", "trade_date"},
                )
                for name, label, value_type in STOCK_A_DAILY_PRICE_FIELDS
            ],
        ],
    )


def stock_a_daily_price_remote_code(params: dict[str, Any]) -> str:
    return f"""
import json
import math
import traceback

PARAMS = {json.dumps(params, ensure_ascii=False, sort_keys=True)}
QUERY_ID = {json.dumps(STOCK_A_DAILY_PRICE_QUERY_ID)}
MARKER_START = {json.dumps(STOCK_A_DAILY_PRICE_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_DAILY_PRICE_MARKER_END)}


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


def title_items(value):
    if isinstance(value, dict):
        titles = value.get("titles") or value.get("columns") or value.get("headers")
        if isinstance(titles, list):
            parsed = []
            for item in titles:
                if isinstance(item, dict) and item.get("key"):
                    parsed.append(item)
                elif isinstance(item, str):
                    parsed.append({{"key": item, "label": item}})
            if parsed:
                return parsed
        for child in value.values():
            found = title_items(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = title_items(child)
            if found:
                return found
    return []


def row_score(rows, title_keys):
    score = len(rows)
    first = rows[0] if rows else None
    if isinstance(first, dict):
        keys = {{str(key) for key in first}}
        score += 100 * len(keys.intersection(title_keys))
        score += len(keys)
    elif isinstance(first, (list, tuple)):
        score += 50 * int(bool(title_keys))
        score += len(first)
    return score


def looks_like_rows(value, title_keys):
    if not value:
        return False
    sample = value[: min(5, len(value))]
    if all(isinstance(item, dict) for item in sample):
        return any(row_score([item], title_keys) > 0 for item in sample)
    if title_keys and all(isinstance(item, (list, tuple)) for item in sample):
        return True
    return False


def row_list_candidates(value, title_keys):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {{"titles", "columns", "headers"}}:
                continue
            if isinstance(child, list) and looks_like_rows(child, title_keys):
                yield child
            yield from row_list_candidates(child, title_keys)
    elif isinstance(value, list):
        if looks_like_rows(value, title_keys):
            yield value
        for child in value:
            yield from row_list_candidates(child, title_keys)


def first_row_list(value, title_keys):
    candidates = list(row_list_candidates(value, title_keys))
    if not candidates:
        return []
    candidates.sort(key=lambda rows: row_score(rows, title_keys), reverse=True)
    return candidates[0]


def normalize_row(row, title_keys):
    if isinstance(row, dict):
        return {{str(key): jsonable(value) for key, value in row.items()}}
    if isinstance(row, (list, tuple)) and title_keys:
        keys = title_keys[: len(row)]
        return {{key: jsonable(value) for key, value in zip(keys, row)}}
    return {{}}


def unique_column_name(label, row):
    if label not in row:
        return label
    index = 2
    while f"{{label}}_{{index}}" in row:
        index += 1
    return f"{{label}}_{{index}}"


def rename_row(row, label_by_key):
    renamed = {{}}
    for key, value in row.items():
        label = label_by_key.get(key, key)
        renamed[unique_column_name(label, renamed)] = value
    return renamed


def normalize_query_index(raw, base_day):
    titles = title_items(raw)
    title_keys = [str(item["key"]) for item in titles if isinstance(item, dict) and item.get("key")]
    label_by_key = {{
        str(item["key"]): str(item.get("label") or item["key"])
        for item in titles
        if isinstance(item, dict) and item.get("key")
    }}
    rows = []
    for row in first_row_list(raw, title_keys):
        normalized = normalize_row(row, title_keys)
        if normalized:
            renamed = rename_row(normalized, label_by_key)
            renamed["trade_date"] = base_day
            renamed["query_id"] = QUERY_ID
            rows.append(renamed)
    return rows


payload = {{"data": None}}
try:
    call_params = dict(PARAMS)
    base_day = str(call_params.get("end_date") or call_params.get("base_day") or "")
    pod = call_params.get("pod") or "cbas-babel-frondend-pod"

    def query_index():
        api = get_arsenal_api(pod)
        response = api.post(
            "/babel/api/query_index",
            files={{"queryId": (None, QUERY_ID), "baseDay": (None, base_day.replace("-", ""))}},
        )
        return response.json()

    raw = query_index()
    payload["data"] = normalize_query_index(raw, base_day.replace("-", ""))
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=8)

print(MARKER_START)
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print(MARKER_END)
"""


def normalize_stock_a_daily_price(value: Any) -> pd.DataFrame:
    if value is None:
        return _stock_a_daily_price_frame([])
    if isinstance(value, pd.DataFrame):
        return _normalize_frame(value)
    if isinstance(value, dict):
        return _normalize_dict(value)
    if isinstance(value, list):
        return _stock_a_daily_price_frame(
            [_normalize_row(row) for row in value if isinstance(row, dict)]
        )
    raise TypeError(f"Unsupported MindGo stock daily result type: {type(value).__name__}")


def _query_params(request: MindgoDatasetQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    params.setdefault("fields", DEFAULT_QUERY_FIELDS)
    return params


def _date_range(start_date: date, end_date: date) -> list[date]:
    day_count = (end_date - start_date).days + 1
    return [start_date + timedelta(days=offset) for offset in range(day_count)]


def _daily_partitions(frame: pd.DataFrame, fallback_date: date) -> list[tuple[str, pd.DataFrame]]:
    working = frame.copy()
    fallback_trade_date = fallback_date.strftime("%Y%m%d")
    if "trade_date" not in working.columns:
        working["trade_date"] = fallback_trade_date
    working["trade_date"] = working["trade_date"].map(_date_text).fillna(fallback_trade_date)
    if working.empty:
        return [(fallback_trade_date, working)]
    return [
        (str(trade_date), partition.reset_index(drop=True))
        for trade_date, partition in working.groupby("trade_date", sort=True, dropna=False)
    ]


def mindgo_parquet_partition_path(
    root: Path | str,
    dataset_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    path = Path(root) / _safe_partition_segment(dataset_id)
    for key, value in partition_values.items():
        path /= f"{_safe_partition_segment(key)}={_safe_partition_segment(value)}"
    return path / "data.parquet"


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
    return _stock_a_daily_price_frame(rows)


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _stock_a_daily_price_frame(_frame_to_rows(frame))


def _frame_to_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    working = frame.copy()
    if "trade_date" not in working.columns:
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
        normalized["trade_date"] = _date_text(normalized["trade_date"])
    if "symbol" in normalized and normalized["symbol"] is not None:
        normalized["symbol"] = str(normalized["symbol"])
    if "name" in normalized and normalized["name"] is not None:
        normalized["name"] = str(normalized["name"])
    return normalized


def _stock_a_daily_price_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    columns = [name for name, _, _ in STOCK_A_DAILY_PRICE_FIELDS]
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


def _date_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str) and value.isdigit():
        return value
    timestamp = pd.to_datetime(value)
    if pd.isna(timestamp):
        return None
    return timestamp.strftime("%Y%m%d")


def _safe_partition_segment(value: str) -> str:
    text = str(value)
    if not text or "/" in text or "\\" in text or text in {".", ".."}:
        raise ValueError(f"invalid parquet partition path segment: {text!r}")
    return text
