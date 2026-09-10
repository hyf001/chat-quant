from __future__ import annotations

import base64
import io
import json
import math
import re
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from datetime import time as datetime_time
from pathlib import Path
from typing import Any, Protocol

import pandas as pd
import pyarrow.parquet as pyarrow_parquet

from app.core.config import get_settings
from app.core.logging import get_logger
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

logger = get_logger(__name__)

STOCK_A_MINUTE_PRICE_MARKER_START = "MINDGO_STOCK_A_MINUTE_PRICE_JSON_START"
STOCK_A_MINUTE_PRICE_MARKER_END = "MINDGO_STOCK_A_MINUTE_PRICE_JSON_END"
# Keep each MindGo request bounded while avoiding the overhead of one remote
# Jupyter execution per small group of securities.
STOCK_A_MINUTE_PRICE_BATCH_SIZE = 20
# 20-minute windows keep every Parquet payload (~1.8MB once base64 encoded)
# under the Jupyter IOPub burst budget (iopub_data_rate_limit=1MB/s over a 3s
# window) while cutting the daily full-universe get_price calls from 120 to 12.
STOCK_A_MINUTE_PRICE_WINDOW_MINUTES = 20
STOCK_A_MINUTE_PRICE_TIMEOUT_SECONDS = 300.0
# Payloads above the burst budget are streamed in paced chunks so that an
# oversized window degrades into a slower transfer instead of silent data loss.
STOCK_A_MINUTE_PRICE_SINGLE_PRINT_LIMIT_BYTES = 2_500_000
STOCK_A_MINUTE_PRICE_PRINT_CHUNK_BYTES = 65_536
STOCK_A_MINUTE_PRICE_PRINT_CHUNK_SLEEP_SECONDS = 0.11
STOCK_A_MINUTE_PRICE_INVALID_SECURITIES_FILENAME = "invalid_securities.json"
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

        params = _query_params(request)
        securities = params.get("securities")
        if isinstance(securities, str):
            security_list = [securities]
        elif isinstance(securities, (list, tuple)):
            security_list = list(securities)
        elif securities is None:
            security_list = []
        else:
            security_list = [securities]

        invalid_securities = self._load_invalid_securities()
        security_list = [
            str(symbol) for symbol in security_list if str(symbol) not in invalid_securities
        ]

        if not security_list:
            return _stock_a_minute_price_frame([])

        frames: list[pd.DataFrame] = []
        pending = security_list
        batch_number = 0
        while pending:
            batch = pending[:STOCK_A_MINUTE_PRICE_BATCH_SIZE]
            offset = len(security_list) - len(pending)
            batch_number += 1
            batch_params = {
                **params,
                "securities": batch,
            }
            try:
                payload = await self._runner.run_json(
                    stock_a_minute_price_remote_code(batch_params),
                    marker_start=STOCK_A_MINUTE_PRICE_MARKER_START,
                    marker_end=STOCK_A_MINUTE_PRICE_MARKER_END,
                    timeout_seconds=STOCK_A_MINUTE_PRICE_TIMEOUT_SECONDS,
                )
            except Exception as exc:
                batch_number = offset // STOCK_A_MINUTE_PRICE_BATCH_SIZE + 1
                raise RuntimeError(
                    "MindGo minute query failed for batch "
                    f"{batch_number} ({len(batch)} securities, offset {offset}): {exc}"
                ) from exc
            if payload.get("error"):
                invalid_symbol = _invalid_security_from_error(payload)
                if invalid_symbol is not None:
                    invalid_securities.add(invalid_symbol)
                    self._save_invalid_securities(invalid_securities)
                    pending = [symbol for symbol in pending if symbol != invalid_symbol]
                    batch_number -= 1
                    continue
                raise RuntimeError(
                    "Remote MindGo query failed for batch "
                    f"{batch_number} ({len(batch)} securities): " + _remote_error_detail(payload)
                )
            frames.append(minute_price_frame_from_payload(payload))
            pending = pending[len(batch) :]

        if len(frames) == 1:
            return frames[0]
        return pd.concat(frames, ignore_index=True)

    def _invalid_securities_path(self) -> Path:
        return (
            self._storage.source_root(self.source_id)
            / STOCK_A_MINUTE_PRICE_INVALID_SECURITIES_FILENAME
        )

    def _load_invalid_securities(self) -> set[str]:
        path = self._invalid_securities_path()
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return set()
        return {str(symbol) for symbol in value} if isinstance(value, list) else set()

    def _save_invalid_securities(self, securities: set[str]) -> None:
        path = self._invalid_securities_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(sorted(securities), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        started_at = time.perf_counter()
        # Sync always covers the full stock universe from the snapshot table;
        # an optionally supplied securities parameter must not narrow the sync.
        sync_params = {key: value for key, value in request.params.items() if key != "securities"}
        sync_params["securities"] = _snapshot_info_securities()
        synced_count = 0
        fetched_windows = 0
        skipped_windows = 0
        for trading_day in _date_range(request.start_date, request.end_date):
            if trading_day.weekday() >= 5:
                continue
            for window_start, window_end in _minute_windows(trading_day):
                path = self._window_path(trading_day, window_start, window_end)
                # Window files are the checkpoint: a completed window is never
                # requested again when the same sync instance is retried.
                if path.exists():
                    skipped_windows += 1
                    continue
                window_started_at = time.perf_counter()
                logger.info(
                    "[a_stock_minute_price.sync] fetching window %s-%s (%s)",
                    window_start.strftime("%H:%M"),
                    window_end.strftime("%H:%M"),
                    trading_day.strftime("%Y%m%d"),
                )
                query_request = MindgoSourceQueryRequest(
                    params={
                        **sync_params,
                        "start_date": window_start.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_date": window_end.strftime("%Y-%m-%d %H:%M:%S"),
                        "bar_count": 0,
                    }
                )
                frame = await self._query_full_stock_window(query_request)
                write = MindgoPartitionedParquetWrite(
                    source_id=self.source_id,
                    partition_values={"trade_day": trading_day.strftime("%Y%m%d")},
                    path=path,
                    request=request,
                    options=ParquetWriteOptions(order_by=["trade_date", "symbol"]),
                )
                written_rows = await self._sync_writer.write(write, frame)
                synced_count += written_rows
                fetched_windows += 1
                logger.info(
                    "[a_stock_minute_price.sync] wrote window %s-%s (%s) rows=%s written=%s "
                    "elapsed_ms=%s",
                    window_start.strftime("%H:%M"),
                    window_end.strftime("%H:%M"),
                    trading_day.strftime("%Y%m%d"),
                    len(frame),
                    written_rows,
                    int((time.perf_counter() - window_started_at) * 1000),
                )
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        logger.info(
            "[a_stock_minute_price.sync] finished windows_fetched=%s windows_skipped=%s "
            "rows=%s elapsed_ms=%s",
            fetched_windows,
            skipped_windows,
            synced_count,
            elapsed_ms,
        )
        return MindgoSourceSyncResult(
            status="success",
            elapsed_ms=elapsed_ms,
            synced_count=synced_count,
        )

    async def _query_full_stock_window(
        self,
        request: MindgoSourceQueryRequest,
    ) -> pd.DataFrame:
        """Query one time window with all stocks, removing invalid symbols on error."""
        if self._runner is None:
            raise RuntimeError("MindGo Jupyter runner is not configured")
        params = _query_params(request)
        securities = [str(symbol) for symbol in params["securities"]]
        invalid = self._load_invalid_securities()
        securities = [symbol for symbol in securities if symbol not in invalid]
        while securities:
            payload = await self._runner.run_json(
                stock_a_minute_price_remote_code({**params, "securities": securities}),
                marker_start=STOCK_A_MINUTE_PRICE_MARKER_START,
                marker_end=STOCK_A_MINUTE_PRICE_MARKER_END,
                timeout_seconds=STOCK_A_MINUTE_PRICE_TIMEOUT_SECONDS,
            )
            if not payload.get("error"):
                return minute_price_frame_from_payload(payload)
            invalid_symbol = _invalid_security_from_error(payload)
            if invalid_symbol is None:
                raise RuntimeError("Remote MindGo query failed: " + _remote_error_detail(payload))
            invalid.add(invalid_symbol)
            self._save_invalid_securities(invalid)
            securities = [symbol for symbol in securities if symbol != invalid_symbol]
        return _stock_a_minute_price_frame([])

    def _window_path(
        self,
        trading_day: date,
        window_start: datetime,
        window_end: datetime,
    ) -> Path:
        return (
            self._storage.source_root(self.source_id)
            / f"trade_day={trading_day.strftime('%Y%m%d')}"
            / f"{window_start.strftime('%H%M%S')}_{window_end.strftime('%H%M%S')}.parquet"
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
    """Build the remote kernel cell that returns window data as base64 Parquet.

    The remote kernel serialises the tidy minute frame to Parquet instead of a
    JSON row array: it is ~8x smaller on the wire, it skips the pure-Python
    per-row conversion, and it keeps every window inside the Jupyter IOPub rate
    limit. The marked stdout region stays a JSON object so the existing
    ``run_json`` extraction path keeps working; the payload itself rides in the
    ``data_b64`` field.
    """
    params_json = json.dumps(params, ensure_ascii=False, sort_keys=True)
    standard_columns_json = json.dumps(
        [name for name, _, _ in STOCK_A_MINUTE_PRICE_FIELDS], ensure_ascii=False
    )
    number_columns_json = json.dumps(
        [name for name, _, value_type in STOCK_A_MINUTE_PRICE_FIELDS if value_type == "number"],
        ensure_ascii=False,
    )
    raw_to_standard_json = json.dumps(RAW_TO_STANDARD_FIELD, ensure_ascii=False)
    return f"""
import base64
import io
import json
import time
import traceback
from datetime import datetime

PARAMS_JSON = {params_json!r}
PARAMS = json.loads(PARAMS_JSON)
FIELDS = {json.dumps(DEFAULT_QUERY_FIELDS, ensure_ascii=False)}
STANDARD_COLUMNS = {standard_columns_json}
RAW_TO_STANDARD = {raw_to_standard_json}
NUMBER_COLUMNS = {number_columns_json}
TIME_COLUMNS = ("trade_date", "datetime", "date", "time", "trade_time")
MARKER_START = {json.dumps(STOCK_A_MINUTE_PRICE_MARKER_START)}
MARKER_END = {json.dumps(STOCK_A_MINUTE_PRICE_MARKER_END)}
PRINT_CHUNK_BYTES = {STOCK_A_MINUTE_PRICE_PRINT_CHUNK_BYTES}
PRINT_CHUNK_SLEEP_SECONDS = {STOCK_A_MINUTE_PRICE_PRINT_CHUNK_SLEEP_SECONDS}
SINGLE_PRINT_LIMIT_BYTES = {STOCK_A_MINUTE_PRICE_SINGLE_PRINT_LIMIT_BYTES}


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


def mindgo_end_datetime(value):
    result = mindgo_datetime(value)
    if result is not None and len(str(value).strip()) == 10:
        return result.replace(hour=23, minute=59, second=59)
    return result


def trade_date_text(series):
    import pandas as pd

    timestamps = pd.to_datetime(series, errors="coerce")
    text = timestamps.dt.strftime("%Y-%m-%d %H:%M:%S")
    if text.isna().all() and len(series):
        digits = series.astype("string").str.strip()
        parsed = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
        for width, fmt in ((8, "%Y%m%d"), (12, "%Y%m%d%H%M"), (14, "%Y%m%d%H%M%S")):
            mask = digits.str.len() == width
            if bool(mask.any()):
                parsed.loc[mask] = pd.to_datetime(digits.loc[mask], format=fmt, errors="coerce")
        text = parsed.dt.strftime("%Y-%m-%d %H:%M:%S")
    return text


def frame_with_time_column(frame):
    working = frame
    if not any(str(column) in TIME_COLUMNS for column in working.columns):
        working = working.reset_index()
        columns = [str(column) for column in working.columns]
        columns[0] = "trade_date"
        working.columns = columns
    return working


def symbol_frames_to_tidy(value):
    import pandas as pd

    parts = []
    for symbol, frame in value.items():
        if not hasattr(frame, "reset_index"):
            return None
        part = frame_with_time_column(frame).copy()
        part["symbol"] = str(symbol)
        parts.append(part)
    if not parts:
        return pd.DataFrame(columns=STANDARD_COLUMNS)
    return pd.concat(parts, ignore_index=True)


def panel_frames_to_tidy(value):
    import pandas as pd

    parts = []
    for field_name, frame in value.items():
        field_name = str(field_name)
        if field_name not in STANDARD_COLUMNS or not hasattr(frame, "melt"):
            continue
        working = frame.copy().reset_index()
        time_column = str(working.columns[0])
        long = working.melt(id_vars=[time_column], var_name="symbol", value_name=field_name)
        renames = dict()
        renames[time_column] = "trade_date"
        long = long.rename(columns=renames)
        parts.append(long)
    if not parts:
        return None
    merged = parts[0]
    for part in parts[1:]:
        merged = merged.merge(part, on=["trade_date", "symbol"], how="outer")
    return merged


def tidy_frame(value, securities):
    import pandas as pd

    if isinstance(value, dict):
        panel = panel_frames_to_tidy(value)
        if panel is not None:
            return panel
        tidy = symbol_frames_to_tidy(value)
        if tidy is not None:
            return tidy
        return pd.DataFrame(columns=STANDARD_COLUMNS)
    if hasattr(value, "reset_index") and hasattr(value, "columns"):
        frame = frame_with_time_column(value).copy()
        symbols = securities_symbols(securities)
        if len(symbols) == 1:
            frame["symbol"] = symbols[0]
        return frame
    if isinstance(value, list):
        return pd.DataFrame(value)
    raise TypeError("Unsupported MindGo stock minute result type: " + str(type(value)))


def finalize_tidy(frame):
    import pandas as pd

    out = pd.DataFrame(frame)
    out = out.rename(
        columns=dict(
            (str(key), RAW_TO_STANDARD.get(str(key), str(key))) for key in out.columns
        )
    )
    for column in STANDARD_COLUMNS:
        if column not in out.columns:
            out[column] = pd.NA
    out = out.loc[:, STANDARD_COLUMNS].copy()
    out["symbol"] = out["symbol"].astype("string").astype(object)
    out["trade_date"] = trade_date_text(out["trade_date"])
    for column in NUMBER_COLUMNS:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def frame_to_parquet_base64(frame):
    buffer = io.BytesIO()
    frame.to_parquet(buffer, compression="zstd", index=False)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


payload = dict(rows=0, data_b64="")
try:
    call_params = dict(PARAMS)
    securities = normalize_securities(call_params.get("securities"))
    fields = call_params.get("fields") or FIELDS
    fq = call_params.get("fq", "none")
    if fq == "none":
        fq = None
    get_price_params = dict(
        start_date=mindgo_datetime(call_params.get("start_date")),
        end_date=mindgo_end_datetime(call_params.get("end_date")),
        fre_step="1m",
        fields=fields,
        skip_paused=bool(call_params.get("skip_paused", False)),
        fq=fq,
        is_panel=False,
    )
    bar_count = int(call_params.get("bar_count") or 0)
    if bar_count > 0:
        get_price_params["bar_count"] = bar_count
    value = get_price(securities, **get_price_params)
    tidy = finalize_tidy(tidy_frame(value, securities))
    payload["rows"] = int(len(tidy))
    payload["data_b64"] = frame_to_parquet_base64(tidy)
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=8)

text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
print(MARKER_START)
if len(text) <= SINGLE_PRINT_LIMIT_BYTES:
    print(text)
else:
    for offset in range(0, len(text), PRINT_CHUNK_BYTES):
        print(text[offset:offset + PRINT_CHUNK_BYTES], end="")
        time.sleep(PRINT_CHUNK_SLEEP_SECONDS)
    print()
print(MARKER_END)
"""


def minute_price_frame_from_payload(payload: Mapping[str, Any]) -> pd.DataFrame:
    """Decode the base64 Parquet payload produced by the remote MindGo kernel."""
    encoded = payload.get("data_b64")
    if not isinstance(encoded, str) or not encoded:
        return _stock_a_minute_price_frame([])
    try:
        table = pyarrow_parquet.read_table(io.BytesIO(base64.b64decode(encoded)))
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("MindGo minute price payload is not valid Parquet") from exc
    frame = table.to_pandas()
    expected_rows = payload.get("rows")
    if isinstance(expected_rows, int) and expected_rows >= 0 and expected_rows != len(frame):
        raise RuntimeError(
            "MindGo minute price payload is incomplete: "
            f"header rows={expected_rows} parquet rows={len(frame)}"
        )
    return _coerce_minute_price_frame(frame)


def _coerce_minute_price_frame(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [name for name, _, _ in STOCK_A_MINUTE_PRICE_FIELDS]
    working = pd.DataFrame(frame)
    for column in columns:
        if column not in working.columns:
            working[column] = pd.NA
    working = working.loc[:, columns].reset_index(drop=True)
    working["symbol"] = working["symbol"].map(_json_scalar)
    working["trade_date"] = working["trade_date"].map(_json_scalar)
    for name, _, value_type in STOCK_A_MINUTE_PRICE_FIELDS:
        if value_type == "number":
            working[name] = pd.to_numeric(working[name], errors="coerce")
    return working


def _query_params(request: MindgoSourceQueryRequest) -> dict[str, Any]:
    params = dict(request.params)
    if not params.get("securities"):
        params["securities"] = _snapshot_info_securities()
    params.setdefault("fields", DEFAULT_QUERY_FIELDS)
    params.setdefault("fq", "none")
    params.setdefault("skip_paused", False)
    params.setdefault("bar_count", 0)
    return params


def _invalid_security_from_error(payload: Mapping[str, Any]) -> str | None:
    error = str(payload.get("error") or "")
    if "不存在" not in error:
        return None
    match = re.search(r"证券\[([^\]]+)\]不存在", error)
    return match.group(1).strip().upper() if match else None


def _remote_error_detail(payload: Mapping[str, Any]) -> str:
    """Render a remote failure without echoing the (potentially huge) data field."""
    detail = {"error": payload.get("error")}
    if payload.get("traceback"):
        detail["traceback"] = payload["traceback"]
    text = json.dumps(detail, ensure_ascii=False)
    error = str(payload.get("error") or "")
    if "get_price" in error and "not defined" in error:
        text += (
            " (the notebook kernel was restarted without running its setup cells; "
            "open the notebook, run the MindGo API cells, then retry)"
        )
    return text


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


def _date_range(start_date: date, end_date: date) -> list[date]:
    return [
        start_date + timedelta(days=offset) for offset in range((end_date - start_date).days + 1)
    ]


def _minute_windows(trading_day: date) -> list[tuple[datetime, datetime]]:
    windows: list[tuple[datetime, datetime]] = []
    for session_start, session_end in (
        (datetime_time(9, 30), datetime_time(11, 30)),
        (datetime_time(13, 0), datetime_time(15, 0)),
    ):
        start = datetime.combine(trading_day, session_start)
        end = datetime.combine(trading_day, session_end) - timedelta(seconds=1)
        while start <= end:
            window_end = min(
                start
                + timedelta(minutes=STOCK_A_MINUTE_PRICE_WINDOW_MINUTES)
                - timedelta(seconds=1),
                end,
            )
            windows.append((start, window_end))
            start = window_end + timedelta(seconds=1)
    return windows


def mindgo_parquet_partition_path(
    storage_root: Path | str,
    source_id: str,
    partition_values: Mapping[str, str],
) -> Path:
    return mindgo_source_partition_path(storage_root, source_id, partition_values)


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
