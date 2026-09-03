from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Protocol

import pandas as pd

from app.schema.dataset.taxonomy import (
    DatasetAssetClass,
    DatasetFrequency,
    DatasetMarket,
    category_path,
    category_path_en,
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
    MindgoSourceSyncWriteMode,
)
from app.service.datasource.mindgo.jupyter_runner import MindgoJupyterRunner
from app.service.datasource.mindgo.stock_a_snapshot_info.constants import (
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage
from app.storage import DuckDBParquetStore, ParquetWriteOptions

STOCK_A_SNAPSHOT_INFO_MARKER_START = "MINDGO_STOCK_A_SNAPSHOT_INFO_JSON_START"
STOCK_A_SNAPSHOT_INFO_MARKER_END = "MINDGO_STOCK_A_SNAPSHOT_INFO_JSON_END"
STOCK_A_SNAPSHOT_INFO_QUERY_ID = "1018"
STOCK_A_SNAPSHOT_INFO_FIELDS = [
    ("symbol", "股票代码", "string"),
    ("name", "股票简称", "string"),
]
DEFAULT_QUERY_FIELDS = [name for name, _, _ in STOCK_A_SNAPSHOT_INFO_FIELDS]
RAW_TO_STANDARD_FIELD = {
    "股票代码": "symbol",
    "股票简称": "name",
}
STANDARD_FIELD_NAMES = {name for name, _, _ in STOCK_A_SNAPSHOT_INFO_FIELDS}


@dataclass(frozen=True)
class MindgoSnapshotParquetWrite:
    source_id: str
    path: Path
    request: MindgoSourceSyncRequest
    options: ParquetWriteOptions


class MindgoSnapshotSyncWriter(Protocol):
    async def write(
        self,
        write: MindgoSnapshotParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        """Write one MindGo dataset snapshot and return persisted row count."""


class DuckDBParquetMindgoSnapshotSyncWriter:
    def __init__(self, store: DuckDBParquetStore | None = None) -> None:
        self._store = store or DuckDBParquetStore()

    async def write(
        self,
        write: MindgoSnapshotParquetWrite,
        frame: pd.DataFrame,
    ) -> int:
        if write.request.write_mode == MindgoSourceSyncWriteMode.SKIP and write.path.exists():
            return 0
        return self._store.write(frame, write.path, options=write.options)


class StockASnapshotInfoAdapter:
    source_id = STOCK_A_SNAPSHOT_INFO_SOURCE_ID

    def __init__(
        self,
        runner: MindgoJupyterRunner | None = None,
        *,
        sync_writer: MindgoSnapshotSyncWriter | None = None,
        storage: MindgoSourceStorage | None = None,
        storage_root: Path | str | None = None,
        parquet_root: Path | str | None = None,
    ) -> None:
        if storage is not None and (storage_root is not None or parquet_root is not None):
            raise ValueError("storage cannot be combined with storage_root or parquet_root")
        self._runner = runner
        self._sync_writer = sync_writer or DuckDBParquetMindgoSnapshotSyncWriter()
        root = storage_root if storage_root is not None else parquet_root
        if storage is not None:
            self._storage = storage
        elif root is not None:
            self._storage = MindgoSourceStorage(root)
        else:
            self._storage = MindgoSourceStorage()

    async def get_source_schema(self) -> MindgoSourceSchema:
        return stock_a_snapshot_info_schema(self._storage)

    async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")

        payload = await self._runner.run_json(
            stock_a_snapshot_info_remote_code(_query_params(request)),
            marker_start=STOCK_A_SNAPSHOT_INFO_MARKER_START,
            marker_end=STOCK_A_SNAPSHOT_INFO_MARKER_END,
        )
        if payload.get("error"):
            raise RuntimeError(
                "Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False)
            )
        return normalize_stock_a_snapshot_info(payload.get("data"))

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        started_at = time.perf_counter()
        query_request = MindgoSourceQueryRequest(
            params={
                **request.params,
                "baseDay": request.end_date.isoformat(),
            }
        )
        frame = await self.query_from_mindgo(query_request)
        write = MindgoSnapshotParquetWrite(
            source_id=self.source_id,
            path=self._storage.snapshot_path(self.source_id),
            request=request,
            options=ParquetWriteOptions(order_by=["symbol"]),
        )
        synced_count = await self._sync_writer.write(write, frame)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return MindgoSourceSyncResult(
            status="success",
            elapsed_ms=elapsed_ms,
            synced_count=synced_count,
        )


def stock_a_snapshot_info_schema(
    storage: MindgoSourceStorage | None = None,
) -> MindgoSourceSchema:
    storage = storage or MindgoSourceStorage()
    market = DatasetMarket.A
    asset_class = DatasetAssetClass.STOCK
    frequency = DatasetFrequency.SNAPSHOT
    topic_zh = "信息维表"
    topic_en = "info"
    return MindgoSourceSchema(
        name="A股股票信息维表",
        name_zh="A股股票信息维表",
        name_en="a_stock_snapshot_info",
        category_path=category_path(market, asset_class, frequency, topic_zh),
        category_path_en=category_path_en(market, asset_class, frequency, topic_en),
        description="A股股票基础信息维表，query_index 1018，仅保留一个最新快照",
        mindgo_function="query_index",
        storage=MindgoSourceStorageSpec(
            path=storage.snapshot_path(STOCK_A_SNAPSHOT_INFO_SOURCE_ID).as_posix(),
            format="parquet",
            partitioned_by=[],
            min_partition=None,
            max_partition=None,
            partition_count=0,
        ),
        query_params=[
            MindgoParameterSpec(
                name="baseDay",
                label="baseDay",
                value_type="date",
                required=True,
                description="query_index 1018 的查询日期；同步时使用同步请求结束日期。",
            ),
            MindgoParameterSpec(
                name="fields",
                label="数据字段",
                value_type="string[]",
                required=False,
                default=DEFAULT_QUERY_FIELDS,
                options=[
                    MindgoParameterOption(label=label, value=name)
                    for name, label, _ in STOCK_A_SNAPSHOT_INFO_FIELDS
                ],
            ),
        ],
        result_schema=[
            MindgoFieldSpec(
                name=name,
                label=label,
                value_type=value_type,
                required=name in {"symbol", "name"},
            )
            for name, label, value_type in STOCK_A_SNAPSHOT_INFO_FIELDS
        ],
    )


def stock_a_snapshot_info_remote_code(params: dict[str, Any]) -> str:
    return f"""
import json
import math
import traceback

PARAMS = {json.dumps(params, ensure_ascii=False, sort_keys=True)}
QUERY_ID = {json.dumps(STOCK_A_SNAPSHOT_INFO_QUERY_ID)}
MARKER_START = {json.dumps(STOCK_A_SNAPSHOT_INFO_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_SNAPSHOT_INFO_MARKER_END)}


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


def normalize_query_index(raw):
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
            rows.append(rename_row(normalized, label_by_key))
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

    payload["data"] = normalize_query_index(query_index())
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=8)

print(MARKER_START)
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print(MARKER_END)
"""


def normalize_stock_a_snapshot_info(value: Any) -> pd.DataFrame:
    if value is None:
        return _stock_a_snapshot_info_frame([])
    if isinstance(value, pd.DataFrame):
        return _normalize_frame(value)
    if isinstance(value, dict):
        return _normalize_dict(value)
    if isinstance(value, list):
        return _stock_a_snapshot_info_frame(
            [_normalize_row(row) for row in value if isinstance(row, dict)]
        )
    raise TypeError(f"Unsupported MindGo stock static info result type: {type(value).__name__}")


def mindgo_parquet_snapshot_path(storage_root: Path | str, source_id: str) -> Path:
    return MindgoSourceStorage(storage_root).snapshot_path(source_id)


def _query_params(request: MindgoSourceQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    params.setdefault("baseDay", params.get("end_date") or params.get("start_date"))
    params.setdefault("fields", DEFAULT_QUERY_FIELDS)
    return params


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
    return _stock_a_snapshot_info_frame(rows)


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _stock_a_snapshot_info_frame(_frame_to_rows(frame))


def _frame_to_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [_normalize_row(row) for row in frame.to_dict(orient="records")]


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        RAW_TO_STANDARD_FIELD.get(str(key), str(key)): _json_scalar(value)
        for key, value in row.items()
        if str(key) in RAW_TO_STANDARD_FIELD or str(key) in STANDARD_FIELD_NAMES
    }
    filtered = {key: value for key, value in normalized.items() if key in STANDARD_FIELD_NAMES}
    if "symbol" in filtered and filtered["symbol"] is not None:
        filtered["symbol"] = str(filtered["symbol"])
    if "name" in filtered and filtered["name"] is not None:
        filtered["name"] = str(filtered["name"])
    return filtered


def _stock_a_snapshot_info_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    columns = [name for name, _, _ in STOCK_A_SNAPSHOT_INFO_FIELDS]
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
    try:
        missing = pd.isna(value)
        if isinstance(missing, bool) and missing:
            return None
    except Exception:
        pass
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value
