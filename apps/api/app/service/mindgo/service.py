from __future__ import annotations

import math
from typing import Any

import pandas as pd

from app.core.config import Settings, get_settings
from app.schema.mindgo import (
    MindgoConnectionConfig,
    MindgoConnectionTestRequest,
    MindgoConnectionTestResponse,
    MindgoDatasetDuckDBQueryRequest,
    MindgoDatasetListResponse,
    MindgoDatasetQueryRequest,
    MindgoDatasetQueryResponse,
    MindgoDatasetSchema,
    MindgoDatasetSummary,
    MindgoDatasetSyncRequest,
    MindgoDatasetSyncResult,
    MindgoFieldSpec,
)
from app.service.mindgo.jupyter_runner import (
    DEFAULT_MINDGO_AUTH_SCHEME,
    DEFAULT_MINDGO_NOTEBOOK_PATH,
    MindgoJupyterConfig,
    MindgoJupyterRunner,
)
from app.service.mindgo.protocol import MindgoDatasetAdapter
from app.service.mindgo.stock_a_daily_price.constants import STOCK_A_DAILY_PRICE_DATASET_ID
from app.service.mindgo.stock_a_daily_price.adaptor import (
    StockADailyPriceAdapter,
)
from app.service.mindgo.storage import MindgoDatasetStorage

MINDGO_CONNECTION_TEST_MARKER_START = "MINDGO_CONNECTION_TEST_JSON_START"
MINDGO_CONNECTION_TEST_MARKER_END = "MINDGO_CONNECTION_TEST_JSON_END"


class MindgoDatasetNotFoundError(ValueError):
    def __init__(self, dataset_id: str) -> None:
        super().__init__(f"MindGo dataset not found: {dataset_id}")
        self.dataset_id = dataset_id


async def list_datasets() -> MindgoDatasetListResponse:
    summaries = []
    for dataset_id in _dataset_ids():
        schema = await _schema_for_dataset(dataset_id)
        summaries.append(
            MindgoDatasetSummary(
                id=dataset_id,
                name=schema.name,
                category_path=schema.category_path,
                description=schema.description,
                storage=schema.storage,
            )
        )
    return MindgoDatasetListResponse(datasets=summaries)


async def get_schema(dataset_id: str) -> MindgoDatasetSchema:
    return await _schema_for_dataset(dataset_id)


async def test_connection(request: MindgoConnectionTestRequest) -> MindgoConnectionTestResponse:
    _ = request
    settings = _fresh_settings()
    connection = _connection_from_settings(settings)
    if not connection.url.strip():
        return MindgoConnectionTestResponse(ok=False, message="请填写 Notebook 地址")
    if not (connection.token or "").strip():
        return MindgoConnectionTestResponse(ok=False, message="请填写访问 Token")
    if connection.execution_mode != "jupyter":
        return MindgoConnectionTestResponse(ok=False, message="暂只支持 Jupyter 执行方式")
    runner = _runner_from_connection(connection)
    if runner is None:
        return MindgoConnectionTestResponse(ok=False, message="连接参数不完整")
    try:
        payload = await runner.run_json(
            _connection_test_code(),
            marker_start=MINDGO_CONNECTION_TEST_MARKER_START,
            marker_end=MINDGO_CONNECTION_TEST_MARKER_END,
        )
    except Exception as error:  # noqa: BLE001
        return MindgoConnectionTestResponse(ok=False, message=f"连接失败：{error}")
    if payload.get("ok") is True:
        return MindgoConnectionTestResponse(ok=True, message="MindGo Jupyter 连接可用")
    return MindgoConnectionTestResponse(ok=False, message="连接失败：远端返回异常")


async def query_dataset(
    dataset_id: str,
    request: MindgoDatasetQueryRequest,
) -> MindgoDatasetQueryResponse:
    adapter = _adapter_for_dataset(dataset_id)
    schema = await adapter.get_schema()
    frame = await adapter.query_from_mindgo(request)
    return _frame_query_response(
        dataset_id,
        frame,
        columns=schema.result_schema,
        page=request.page,
        page_size=request.page_size,
    )


async def query_dataset_from_duckdb(
    dataset_id: str,
    request: MindgoDatasetDuckDBQueryRequest,
) -> MindgoDatasetQueryResponse:
    sql = request.sql.strip()
    if not sql:
        raise ValueError("SQL 不能为空")
    adapter = _adapter_for_dataset(dataset_id, allow_missing_runner=True)
    frame = await adapter.query_from_duckdb(sql)
    return _frame_query_response(
        dataset_id,
        frame,
        columns=_columns_from_frame(frame),
        page=request.page,
        page_size=request.page_size,
    )


async def sync_dataset(
    dataset_id: str,
    request: MindgoDatasetSyncRequest,
) -> MindgoDatasetSyncResult:
    adapter = _adapter_for_dataset(dataset_id)
    return await adapter.sync(request)


def _dataset_ids() -> tuple[str, ...]:
    return (STOCK_A_DAILY_PRICE_DATASET_ID,)


async def _schema_for_dataset(dataset_id: str) -> MindgoDatasetSchema:
    adapter = _adapter_for_dataset(dataset_id, allow_missing_runner=True)
    return await adapter.get_schema()


def _adapter_for_dataset(
    dataset_id: str,
    *,
    allow_missing_runner: bool = False,
) -> MindgoDatasetAdapter:
    if dataset_id != STOCK_A_DAILY_PRICE_DATASET_ID:
        raise MindgoDatasetNotFoundError(dataset_id)
    settings = _fresh_settings()
    connection = _connection_from_settings(settings)
    runner = None if allow_missing_runner else _runner_from_connection(connection)
    return StockADailyPriceAdapter(runner, storage=_storage_from_settings(settings))


def _fresh_settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()


def _connection_from_settings(settings: Settings | None = None) -> MindgoConnectionConfig:
    settings = settings or _fresh_settings()
    return MindgoConnectionConfig(
        execution_mode="jupyter",
        url=settings.mindgo_jupyter_url or "",
        auth_scheme=settings.mindgo_auth_scheme or DEFAULT_MINDGO_AUTH_SCHEME,
        token=settings.mindgo_jupyter_token,
        notebook_path=settings.mindgo_notebook_path,
        kernel_id=settings.mindgo_kernel_id,
        timeout_seconds=settings.mindgo_timeout_seconds,
    )


def _storage_from_settings(settings: Settings) -> MindgoDatasetStorage:
    return MindgoDatasetStorage(settings.mindgo_storage_root)


def _runner_from_connection(connection: MindgoConnectionConfig | None):
    if connection is None or not connection.url.strip():
        return None
    return MindgoJupyterRunner(
        MindgoJupyterConfig(
            url=connection.url.strip(),
            token=connection.token.strip() if connection.token else None,
            auth_scheme=connection.auth_scheme.strip() or "Bearer",
            notebook_path=connection.notebook_path.strip() or DEFAULT_MINDGO_NOTEBOOK_PATH,
            kernel_id=connection.kernel_id.strip() if connection.kernel_id else None,
            timeout_seconds=connection.timeout_seconds,
        )
    )


def _connection_test_code() -> str:
    return f"""
import json

print({MINDGO_CONNECTION_TEST_MARKER_START!r})
print(json.dumps({{"ok": True}}, ensure_ascii=False, separators=(",", ":")))
print({MINDGO_CONNECTION_TEST_MARKER_END!r})
"""


def _frame_to_json_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in frame.to_dict(orient="records"):
        rows.append({str(key): _json_value(value) for key, value in row.items()})
    return rows


def _frame_query_response(
    dataset_id: str,
    frame: pd.DataFrame,
    *,
    columns: list[MindgoFieldSpec],
    page: int,
    page_size: int,
) -> MindgoDatasetQueryResponse:
    rows = _frame_to_json_rows(frame)
    total = len(rows)
    start = (page - 1) * page_size
    end = start + page_size
    return MindgoDatasetQueryResponse(
        dataset_id=dataset_id,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=math.ceil(total / page_size) if total else 0,
        columns=columns,
        rows=rows[start:end],
    )


def _columns_from_frame(frame: pd.DataFrame) -> list[MindgoFieldSpec]:
    return [
        MindgoFieldSpec(
            name=str(column),
            label=str(column),
            value_type=_mindgo_field_type(frame[column]),
        )
        for column in frame.columns
    ]


def _mindgo_field_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    if pd.api.types.is_numeric_dtype(series):
        return "number"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    return "string"


def _json_value(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value
    if isinstance(value, list | tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if pd.isna(value):
        return None
    return str(value)
