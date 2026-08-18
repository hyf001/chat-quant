from __future__ import annotations

import math
from typing import Any

import pandas as pd

from app.core.config import Settings, get_settings
from app.schema.mindgo import (
    MindgoConnectionConfig,
    MindgoConnectionTestRequest,
    MindgoConnectionTestResponse,
    MindgoFieldSpec,
    MindgoSourceListResponse,
    MindgoSourceQueryRequest,
    MindgoSourceQueryResponse,
    MindgoSourceSchema,
    MindgoSourceSummary,
    MindgoSourceSyncRequest,
    MindgoSourceSyncResult,
)
from app.service.datasource.mindgo.index_a_daily_price.adaptor import (
    IndexADailyPriceAdapter,
)
from app.service.datasource.mindgo.index_a_daily_price.constants import (
    INDEX_A_DAILY_PRICE_SOURCE_ID,
)
from app.service.datasource.mindgo.jupyter_runner import (
    DEFAULT_MINDGO_AUTH_SCHEME,
    DEFAULT_MINDGO_NOTEBOOK_PATH,
    MindgoJupyterConfig,
    MindgoJupyterRunner,
)
from app.service.datasource.mindgo.protocol import MindgoSourceAdapter
from app.service.datasource.mindgo.stock_a_adjust_factor.adaptor import (
    StockAAdjustFactorAdapter,
)
from app.service.datasource.mindgo.stock_a_adjust_factor.constants import (
    STOCK_A_ADJUST_FACTOR_SOURCE_ID,
)
from app.service.datasource.mindgo.stock_a_daily_price.adaptor import (
    StockADailyPriceAdapter,
)
from app.service.datasource.mindgo.stock_a_daily_price.constants import (
    STOCK_A_DAILY_PRICE_SOURCE_ID,
)
from app.service.datasource.mindgo.storage import MindgoSourceStorage

MINDGO_CONNECTION_TEST_MARKER_START = "MINDGO_CONNECTION_TEST_JSON_START"
MINDGO_CONNECTION_TEST_MARKER_END = "MINDGO_CONNECTION_TEST_JSON_END"


class MindgoSourceNotFoundError(ValueError):
    def __init__(self, source_id: str) -> None:
        super().__init__(f"MindGo source not found: {source_id}")
        self.source_id = source_id


async def list_sources() -> MindgoSourceListResponse:
    summaries = []
    for source_id in _source_ids():
        schema = await _schema_for_source(source_id)
        summaries.append(
            MindgoSourceSummary(
                id=source_id,
                name=schema.name,
                name_zh=schema.name_zh,
                name_en=schema.name_en,
                category_path=schema.category_path,
                category_path_en=schema.category_path_en,
                description=schema.description,
                storage=schema.storage,
            )
        )
    return MindgoSourceListResponse(sources=summaries)


async def get_source_schema(source_id: str) -> MindgoSourceSchema:
    return await _schema_for_source(_canonical_source_id(source_id))


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


async def query_source(
    source_id: str,
    request: MindgoSourceQueryRequest,
) -> MindgoSourceQueryResponse:
    canonical_source_id = _canonical_source_id(source_id)
    adapter = _adapter_for_source(canonical_source_id)
    schema = await adapter.get_source_schema()
    frame = await adapter.query_from_mindgo(request)
    return _frame_query_response(
        canonical_source_id,
        frame,
        columns=schema.result_schema,
        page=request.page,
        page_size=request.page_size,
    )


async def sync_source(
    source_id: str,
    request: MindgoSourceSyncRequest,
) -> MindgoSourceSyncResult:
    adapter = _adapter_for_source(_canonical_source_id(source_id))
    return await adapter.sync(request)


def _source_ids() -> tuple[str, ...]:
    return (
        STOCK_A_DAILY_PRICE_SOURCE_ID,
        STOCK_A_ADJUST_FACTOR_SOURCE_ID,
        INDEX_A_DAILY_PRICE_SOURCE_ID,
    )


async def _schema_for_source(source_id: str) -> MindgoSourceSchema:
    adapter = _adapter_for_source(source_id, allow_missing_runner=True)
    return await adapter.get_source_schema()


def _adapter_for_source(
    source_id: str,
    *,
    allow_missing_runner: bool = False,
) -> MindgoSourceAdapter:
    source_id = _canonical_source_id(source_id)
    settings = _fresh_settings()
    connection = _connection_from_settings(settings)
    runner = None if allow_missing_runner else _runner_from_connection(connection)
    storage = _storage_from_settings(settings)
    if source_id == STOCK_A_DAILY_PRICE_SOURCE_ID:
        return StockADailyPriceAdapter(runner, storage=storage)
    if source_id == STOCK_A_ADJUST_FACTOR_SOURCE_ID:
        return StockAAdjustFactorAdapter(runner, storage=storage)
    if source_id == INDEX_A_DAILY_PRICE_SOURCE_ID:
        return IndexADailyPriceAdapter(runner, storage=storage)
    raise MindgoSourceNotFoundError(source_id)


def _canonical_source_id(source_id: str) -> str:
    stripped = source_id.strip()
    if stripped in _source_ids():
        return stripped
    raise MindgoSourceNotFoundError(source_id)


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


def _storage_from_settings(settings: Settings) -> MindgoSourceStorage:
    return MindgoSourceStorage(settings.mindgo_storage_root)


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
    source_id: str,
    frame: pd.DataFrame,
    *,
    columns: list[MindgoFieldSpec],
    page: int,
    page_size: int,
) -> MindgoSourceQueryResponse:
    rows = _frame_to_json_rows(frame)
    total = len(rows)
    start = (page - 1) * page_size
    end = start + page_size
    return MindgoSourceQueryResponse(
        source_id=source_id,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=math.ceil(total / page_size) if total else 0,
        columns=columns,
        rows=rows[start:end],
    )


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
