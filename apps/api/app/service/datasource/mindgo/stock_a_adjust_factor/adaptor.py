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
    MindgoFieldSpec,
    MindgoParameterOption,
    MindgoParameterSpec,
    MindgoSourceQueryRequest,
    MindgoSourceSchema,
    MindgoSourceStorageSpec,
    MindgoSourceSyncRequest,
    MindgoSourceSyncResult,
    MindgoSourceSyncWriteMode,
)
from app.service.datasource.mindgo.jupyter_runner import MindgoJupyterRunner
from app.service.datasource.mindgo.stock_a_adjust_factor.constants import (
    STOCK_A_ADJUST_FACTOR_SOURCE_ID,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage, mindgo_source_partition_path
from app.storage import DuckDBParquetStore, ParquetWriteOptions

STOCK_A_ADJUST_FACTOR_MARKER_START = "MINDGO_STOCK_A_ADJUST_FACTOR_JSON_START"
STOCK_A_ADJUST_FACTOR_MARKER_END = "MINDGO_STOCK_A_ADJUST_FACTOR_JSON_END"
STOCK_A_ADJUST_FACTOR_QUERY_ID = "1016"
STOCK_A_ADJUST_FACTOR_FIELDS = [
    ("symbol", "股票代码", "string"),
    ("trade_date", "交易日", "date"),
    ("name", "股票简称", "string"),
    ("factor", "复权因子", "number"),
]
DEFAULT_QUERY_FIELDS = [name for name, _, _ in STOCK_A_ADJUST_FACTOR_FIELDS]
RAW_TO_STANDARD_FIELD = {
    "股票代码": "symbol",
    "同花顺代码": "symbol",
    "trade_date": "trade_date",
    "date": "trade_date",
    "股票简称": "name",
    "证券简称": "name",
    "复权因子": "factor",
    "复权因子(日)": "factor",
    "复权因子:不复权": "factor",
    "factor": "factor",
    "uid": "uid",
    "query_id": "query_id",
}
STANDARD_FIELD_NAMES = {name for name, _, _ in STOCK_A_ADJUST_FACTOR_FIELDS}


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


class StockAAdjustFactorAdapter:
    source_id = STOCK_A_ADJUST_FACTOR_SOURCE_ID

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
        return stock_a_adjust_factor_schema(self._storage)

    async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")

        payload = await self._runner.run_json(
            stock_a_adjust_factor_remote_code(_query_params(request)),
            marker_start=STOCK_A_ADJUST_FACTOR_MARKER_START,
            marker_end=STOCK_A_ADJUST_FACTOR_MARKER_END,
        )
        if payload.get("error"):
            raise RuntimeError(
                "Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False)
            )
        return normalize_stock_a_adjust_factor(payload.get("data"))

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        started_at = time.perf_counter()
        synced_count = 0
        for sync_day in _date_range(request.start_date, request.end_date):
            query_request = MindgoSourceQueryRequest(
                params={
                    **request.params,
                    "baseDay": sync_day.isoformat(),
                }
            )
            frame = await self.query_from_mindgo(query_request)
            for partition_date, partition_frame in _daily_partitions(frame, sync_day):
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
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return MindgoSourceSyncResult(
            status="success",
            elapsed_ms=elapsed_ms,
            synced_count=synced_count,
        )


def stock_a_adjust_factor_schema(
    storage: MindgoSourceStorage | None = None,
) -> MindgoSourceSchema:
    storage = storage or MindgoSourceStorage()
    partitioned_by = ["trade_day"]
    partition_summary = storage.partition_summary(
        STOCK_A_ADJUST_FACTOR_SOURCE_ID,
        partitioned_by,
    )
    return MindgoSourceSchema(
        name="A股复权因子(日)",
        category_path=["股票", "A股", "行情数据(A股)"],
        description="A股股票日频复权因子，factor = 后复权价格 / 不复权价格",
        mindgo_function="query_index",
        storage=MindgoSourceStorageSpec(
            path=storage.source_root(STOCK_A_ADJUST_FACTOR_SOURCE_ID).as_posix(),
            format="parquet",
            partitioned_by=partitioned_by,
            min_partition=partition_summary.min_partition,
            max_partition=partition_summary.max_partition,
            partition_count=partition_summary.partition_count,
        ),
        query_params=[
            MindgoParameterSpec(
                name="baseDay",
                label="baseDay",
                value_type="date",
                required=True,
                description="query_index 1016 的单日查询日期。",
            ),
            MindgoParameterSpec(
                name="fields",
                label="数据字段",
                value_type="string[]",
                required=False,
                default=DEFAULT_QUERY_FIELDS,
                options=[
                    MindgoParameterOption(label=label, value=name)
                    for name, label, _ in STOCK_A_ADJUST_FACTOR_FIELDS
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
                for name, label, value_type in STOCK_A_ADJUST_FACTOR_FIELDS
            ],
        ],
    )


def stock_a_adjust_factor_remote_code(params: dict[str, Any]) -> str:
    return f"""
import json
import math
import traceback

PARAMS = {json.dumps(params, ensure_ascii=False, sort_keys=True)}
QUERY_ID = {json.dumps(STOCK_A_ADJUST_FACTOR_QUERY_ID)}
MARKER_START = {json.dumps(STOCK_A_ADJUST_FACTOR_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_ADJUST_FACTOR_MARKER_END)}


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


def title_date_text(value):
    if value is None:
        return None
    text = str(value).strip()
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) < 8:
        return None
    return digits[:8]


def title_trade_date(titles):
    dates = []
    for item in titles:
        if not isinstance(item, dict):
            continue
        text = title_date_text(item.get("from"))
        if text and text != "00000000":
            dates.append(text)
    unique_dates = sorted({{trade_date for trade_date in dates}})
    if len(unique_dates) > 1:
        raise ValueError("query_index returned multiple trade dates: " + ",".join(unique_dates))
    return unique_dates[0] if unique_dates else None


def normalize_query_index(raw, base_day):
    titles = title_items(raw)
    title_keys = [str(item["key"]) for item in titles if isinstance(item, dict) and item.get("key")]
    label_by_key = {{
        str(item["key"]): str(item.get("label") or item["key"])
        for item in titles
        if isinstance(item, dict) and item.get("key")
    }}
    trade_date = title_trade_date(titles) or base_day
    rows = []
    for row in first_row_list(raw, title_keys):
        normalized = normalize_row(row, title_keys)
        if normalized:
            renamed = rename_row(normalized, label_by_key)
            renamed["trade_date"] = trade_date
            renamed["query_id"] = QUERY_ID
            rows.append(renamed)
    return rows


payload = {{"data": None}}
try:
    call_params = dict(PARAMS)
    base_day = str(
        call_params.get("baseDay")
        or call_params.get("base_day")
        or call_params.get("end_date")
        or ""
    )
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


def normalize_stock_a_adjust_factor(value: Any) -> pd.DataFrame:
    if value is None:
        return _stock_a_adjust_factor_frame([])
    if isinstance(value, pd.DataFrame):
        return _normalize_frame(value)
    if isinstance(value, dict):
        return _normalize_dict(value)
    if isinstance(value, list):
        return _stock_a_adjust_factor_frame(
            [_normalize_row(row) for row in value if isinstance(row, dict)]
        )
    raise TypeError(f"Unsupported MindGo stock adjust factor result type: {type(value).__name__}")


def _query_params(request: MindgoSourceQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    params.setdefault("baseDay", params.get("end_date") or params.get("start_date"))
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
    return _stock_a_adjust_factor_frame(rows)


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _stock_a_adjust_factor_frame(_frame_to_rows(frame))


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


def _stock_a_adjust_factor_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    columns = [name for name, _, _ in STOCK_A_ADJUST_FACTOR_FIELDS]
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
