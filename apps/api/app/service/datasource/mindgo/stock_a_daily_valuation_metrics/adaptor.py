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
    MindgoSourceSyncWriteMode,
)
from app.service.datasource.mindgo.jupyter_runner import MindgoJupyterRunner
from app.service.datasource.mindgo.stock_a_daily_valuation_metrics.constants import (
    STOCK_A_VALUATION_METRICS_SOURCE_ID,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage, mindgo_source_partition_path
from app.storage import DuckDBParquetStore, ParquetWriteOptions

STOCK_A_VALUATION_METRICS_MARKER_START = "MINDGO_STOCK_A_VALUATION_METRICS_JSON_START"
STOCK_A_VALUATION_METRICS_MARKER_END = "MINDGO_STOCK_A_VALUATION_METRICS_JSON_END"
STOCK_A_VALUATION_METRICS_TABLE = "asharevalue"
STOCK_A_VALUATION_METRICS_FIELDS = [
    ("symbol", "股票代码", "string", "symbol"),
    ("trade_date", "日期", "date", "date"),
    ("report_date", "报告日期", "date", "report_date"),
    ("stat_date", "报告期", "date", "stat_date"),
    ("pe_lyr", "市盈率LYR", "number", "pe_lyr"),
    ("pe_mrq", "市盈率MRQ", "number", "pe_mrq"),
    ("pe_ttm", "市盈率TTM", "number", "pe_ttm"),
    ("fore_pe_his", "预测市盈率(PE,历史预测)", "number", "fore_pe_his"),
    ("fore_pe_in12m", "预测市盈率(PE,未来12个月)", "number", "fore_pe_in12m"),
    ("static_pe_csi", "静态市盈率(中证发布)", "number", "static_pe_csi"),
    ("auto_pe_csi", "滚动市盈率(中证发布)", "number", "auto_pe_csi"),
    ("his_peg", "历史PEG", "number", "his_peg"),
    ("fore_peg", "预测PEG", "number", "fore_peg"),
    ("pb_mrq", "市净率MRQ", "number", "pb_mrq"),
    ("pb_csi", "市净率(中证发布)", "number", "pb_csi"),
    (
        "pcf_operate_cash_flow_lyr",
        "市现率(PCF,经营现金流)LYR",
        "number",
        "pcf_operate_cash_flow_lyr",
    ),
    (
        "pcf_operate_cash_flow_ttm",
        "市现率(PCF,经营现金流)TTM",
        "number",
        "pcf_operate_cash_flow_ttm",
    ),
    ("pcf_net_cash_flow_lyr", "市现率(PCF,现金净流量)LYR", "number", "pcf_net_cash_flow_lyr"),
    ("pcf_net_cash_flow_ttm", "市现率(PCF,现金净流量)TTM", "number", "pcf_net_cash_flow_ttm"),
    ("ps_lyr", "市销率LYR", "number", "ps_lyr"),
    ("ps_mrq", "市销率MRQ", "number", "ps_mrq"),
    ("ps_ttm", "市销率TTM", "number", "ps_ttm"),
    ("dividend_rate_ttm", "股息率TTM", "number", "dividend_rate_ttm"),
    ("total_mv", "总市值(元)", "number", "total_mv"),
    ("total_mv_object", "总市值(面向对象)(元)", "number", "total_mv_object"),
    ("total_mv_csrc", "总市值(证监会算法)(元)", "number", "total_mv_csrc"),
    ("float_mv", "流通市值(元)", "number", "float_mv"),
    ("ev1", "企业价值(含货币资金)(元)", "number", "ev1"),
    ("ev2", "企业价值(剔除货币资金)(元)", "number", "ev2"),
    ("ev2_to_ebitda", "企业倍数", "number", "ev2_to_ebitda"),
    ("total_shares", "总股本(股)", "number", "total_shares"),
    ("float_shares", "流通股本(股)", "number", "float_shares"),
    ("ashare_total_shares", "A股总股本(股)", "number", "ashare_total_shares"),
    ("ashare_float_shares", "A股流通股本(股)", "number", "ashare_float_shares"),
]
DEFAULT_QUERY_FIELDS = [name for name, _, _, _ in STOCK_A_VALUATION_METRICS_FIELDS]
STANDARD_TO_MINDGO_FIELD = {
    name: mindgo_field for name, _, _, mindgo_field in STOCK_A_VALUATION_METRICS_FIELDS
}
STANDARD_FIELD_NAMES = {name for name, _, _, _ in STOCK_A_VALUATION_METRICS_FIELDS}
RAW_TO_STANDARD_FIELD = {
    "symbol": "symbol",
    "股票代码": "symbol",
    "asharevalue_symbol": "symbol",
    "date": "trade_date",
    "trade_date": "trade_date",
    "日期": "trade_date",
    "asharevalue_date": "trade_date",
    "report_date": "report_date",
    "asharevalue_report_date": "report_date",
    "stat_date": "stat_date",
    "asharevalue_stat_date": "stat_date",
    "total_mv_ashare": "total_mv_object",
    "asharevalue_total_mv_ashare": "total_mv_object",
    "float_mv_ashare": "float_mv",
    "asharevalue_float_mv_ashare": "float_mv",
}
for field_name in STANDARD_FIELD_NAMES:
    RAW_TO_STANDARD_FIELD.setdefault(field_name, field_name)
    RAW_TO_STANDARD_FIELD.setdefault(f"asharevalue_{field_name}", field_name)


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


class StockAValuationMetricsAdapter:
    source_id = STOCK_A_VALUATION_METRICS_SOURCE_ID

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
        return stock_a_daily_valuation_metrics_schema(self._storage)

    async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")

        payload = await self._runner.run_json(
            stock_a_daily_valuation_metrics_remote_code(_query_params(request)),
            marker_start=STOCK_A_VALUATION_METRICS_MARKER_START,
            marker_end=STOCK_A_VALUATION_METRICS_MARKER_END,
        )
        if payload.get("error"):
            raise RuntimeError(
                "Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False)
            )
        return normalize_stock_a_daily_valuation_metrics(payload.get("data"))

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        started_at = time.perf_counter()
        synced_count = 0
        for sync_day in _date_range(request.start_date, request.end_date):
            query_request = MindgoSourceQueryRequest(
                params={
                    **request.params,
                    "date": sync_day.isoformat(),
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


def stock_a_daily_valuation_metrics_schema(
    storage: MindgoSourceStorage | None = None,
) -> MindgoSourceSchema:
    storage = storage or MindgoSourceStorage()
    partitioned_by = ["trade_day"]
    partition_summary = storage.partition_summary(
        STOCK_A_VALUATION_METRICS_SOURCE_ID,
        partitioned_by,
    )
    market = DatasetMarket.A
    asset_class = DatasetAssetClass.STOCK
    frequency = DatasetFrequency.DAILY
    topic_zh = "估值指标"
    topic_en = "valuation_metrics"
    name_zh = dataset_name_zh(market, asset_class, frequency, topic_zh)
    return MindgoSourceSchema(
        name=name_zh,
        name_zh=name_zh,
        name_en=dataset_name_en(market, asset_class, frequency, topic_en),
        category_path=category_path(market, asset_class, frequency, topic_zh),
        category_path_en=category_path_en(market, asset_class, frequency, topic_en),
        description="A股上市公司日频估值相关计算财务指标，来源表 asharevalue",
        mindgo_function="get_fundamentals",
        storage=MindgoSourceStorageSpec(
            path=storage.source_root(STOCK_A_VALUATION_METRICS_SOURCE_ID).as_posix(),
            format="parquet",
            partitioned_by=partitioned_by,
            min_partition=partition_summary.min_partition,
            max_partition=partition_summary.max_partition,
            partition_count=partition_summary.partition_count,
        ),
        query_params=[
            MindgoParameterSpec(
                name="date",
                label="日期",
                value_type="date",
                required=True,
                description="get_fundamentals 的查询日期；同步时由日期范围自动填充。",
            ),
            MindgoParameterSpec(
                name="fields",
                label="数据字段",
                value_type="string[]",
                required=False,
                default=DEFAULT_QUERY_FIELDS,
                options=[
                    MindgoParameterOption(label=label, value=name)
                    for name, label, _, _ in STOCK_A_VALUATION_METRICS_FIELDS
                ],
            ),
        ],
        result_schema=[
            MindgoFieldSpec(
                name=name,
                label=label,
                value_type=value_type,
                required=name in {"symbol", "trade_date"},
            )
            for name, label, value_type, _ in STOCK_A_VALUATION_METRICS_FIELDS
        ],
    )


def stock_a_daily_valuation_metrics_remote_code(params: dict[str, Any]) -> str:
    params_json = json.dumps(params, ensure_ascii=False, sort_keys=True)
    query_fields = _selected_mindgo_fields(params)
    query_expr = ", ".join(f"asharevalue.{field}" for field in query_fields)
    return f"""
import json
import math
import time
import traceback

PARAMS_JSON = {params_json!r}
PARAMS = json.loads(PARAMS_JSON)
MARKER_START = {json.dumps(STOCK_A_VALUATION_METRICS_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_VALUATION_METRICS_MARKER_END)}


def jsonable(value):
    if value is None:
        return None
    try:
        value = value.item()
    except Exception:
        pass
    try:
        import pandas as pd
        missing = pd.isna(value)
        if isinstance(missing, bool) and missing:
            return None
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


def dataframe_rows(frame):
    import pandas as pd

    if frame is None:
        return []
    if not isinstance(frame, pd.DataFrame):
        return frame
    working = frame.reset_index() if frame.index.names and any(frame.index.names) else frame
    rows = []
    for row in working.to_dict(orient="records"):
        rows.append({{str(key): jsonable(value) for key, value in row.items()}})
    return rows


def emit_payload(value):
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    chunk_size = 65536
    print(MARKER_START, flush=True)
    for index in range(0, len(text), chunk_size):
        if index:
            time.sleep(0.25)
        print(text[index:index + chunk_size], end="", flush=True)
    print()
    print(MARKER_END, flush=True)


payload = {{"data": None}}
try:
    call_date = str(PARAMS.get("date") or PARAMS.get("baseDay") or PARAMS.get("base_day") or "")
    call_date = call_date.replace("-", "")
    query_object = query({query_expr})
    payload["data"] = dataframe_rows(get_fundamentals(query_object, date=call_date))
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=8)

emit_payload(payload)
"""


def normalize_stock_a_daily_valuation_metrics(value: Any) -> pd.DataFrame:
    if value is None:
        return _stock_a_daily_valuation_metrics_frame([])
    if isinstance(value, pd.DataFrame):
        return _normalize_frame(value)
    if isinstance(value, dict):
        return _normalize_dict(value)
    if isinstance(value, list):
        return _stock_a_daily_valuation_metrics_frame(
            [_normalize_row(row) for row in value if isinstance(row, dict)]
        )
    raise TypeError(f"Unsupported MindGo stock valuation result type: {type(value).__name__}")


def mindgo_parquet_partition_path(
    storage_root: Path | str,
    source_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    return mindgo_source_partition_path(storage_root, source_id, partition_values)


def _query_params(request: MindgoSourceQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    params.setdefault("date", params.get("baseDay") or params.get("base_day"))
    params.setdefault("fields", DEFAULT_QUERY_FIELDS)
    return params


def _selected_mindgo_fields(params: dict[str, Any]) -> list[str]:
    requested = params.get("fields") or DEFAULT_QUERY_FIELDS
    if not isinstance(requested, list):
        requested = DEFAULT_QUERY_FIELDS
    selected: list[str] = []
    for field in ["symbol", "trade_date", *requested]:
        mapped = STANDARD_TO_MINDGO_FIELD.get(str(field))
        if mapped and mapped not in selected:
            selected.append(mapped)
    return selected


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


def _normalize_dict(value: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for symbol, item in value.items():
        if isinstance(item, pd.DataFrame):
            for row in _frame_to_rows(item):
                row.setdefault("symbol", str(symbol))
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
    return _stock_a_daily_valuation_metrics_frame(rows)


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _stock_a_daily_valuation_metrics_frame(_frame_to_rows(frame))


def _frame_to_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [_normalize_row(row) for row in frame.to_dict(orient="records")]


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        RAW_TO_STANDARD_FIELD.get(str(key), str(key)): _json_scalar(value)
        for key, value in row.items()
        if str(key) in RAW_TO_STANDARD_FIELD
        or RAW_TO_STANDARD_FIELD.get(str(key), str(key)) in STANDARD_FIELD_NAMES
    }
    for date_column in ("trade_date", "report_date", "stat_date"):
        if date_column in normalized:
            normalized[date_column] = _date_text(normalized[date_column])
    if "symbol" in normalized and normalized["symbol"] is not None:
        normalized["symbol"] = str(normalized["symbol"])
    return normalized


def _stock_a_daily_valuation_metrics_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    columns = [name for name, _, _, _ in STOCK_A_VALUATION_METRICS_FIELDS]
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
