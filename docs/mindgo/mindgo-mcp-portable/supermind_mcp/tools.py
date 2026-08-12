"""Tool functions exposed by the MCP server."""

from __future__ import annotations

from typing import Any

from .download import download_files as _download_files
from .intraday_realtime import stock_intraday_realtime as _stock_intraday_realtime
from .intraday_realtime import stock_intraday_realtime_batch as _stock_intraday_realtime_batch
from .jupyter_api import jupyter_api
from .jupyter_ws import execute_code_ws
from .sync import sync_files as _sync_files


async def list_kernels(
    url: str | None = None,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """List active Jupyter kernels."""

    async with jupyter_api(url=url, token=token) as api:
        return await api.list_kernels()


async def create_kernel(
    kernel_name: str = "python3",
    path: str | None = None,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Create a new Jupyter kernel."""

    async with jupyter_api(url=url, token=token) as api:
        return await api.create_kernel(kernel_name=kernel_name, path=path)


async def execute_code(
    kernel_id: str,
    code: str,
    url: str | None = None,
    token: str | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Execute Python code in a kernel and return stdout, stderr, result, and images."""

    result = await execute_code_ws(
        kernel_id=kernel_id,
        code=code,
        url=url,
        token=token,
        timeout=timeout,
    )
    return result.model_dump()


async def interrupt_kernel(
    kernel_id: str,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Interrupt a running Jupyter kernel."""

    async with jupyter_api(url=url, token=token) as api:
        return await api.interrupt_kernel(kernel_id)


async def delete_kernel(
    kernel_id: str,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Delete a Jupyter kernel."""

    async with jupyter_api(url=url, token=token) as api:
        return await api.delete_kernel(kernel_id)


async def sync_files(
    remote_path: str = "",
    local_path: str = ".",
    dry_run: bool = False,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Sync a local directory to Jupyter Contents API."""

    result = await _sync_files(
        remote_path=remote_path,
        local_path=local_path,
        dry_run=dry_run,
        url=url,
        token=token,
    )
    return result.model_dump()


async def download_files(
    remote_path: str = "",
    local_path: str = ".",
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Download a file or directory from Jupyter Contents API."""

    result = await _download_files(
        remote_path=remote_path,
        local_path=local_path,
        url=url,
        token=token,
    )
    return result.model_dump()


async def stock_intraday_realtime(
    stockcode: str,
    trade_date: str,
    end_time: str | None = None,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch latest 1m intraday bars for one A-share stock from MindGo get_price."""

    return await _stock_intraday_realtime(
        stockcode=stockcode,
        trade_date=trade_date,
        end_time=end_time,
        url=url,
        token=token,
    )


async def stock_intraday_realtime_batch(
    stockcodes: list[str],
    trade_date: str,
    end_time: str | None = None,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch latest 1m intraday bars for a small A-share stock list from MindGo get_price."""

    return await _stock_intraday_realtime_batch(
        stockcodes=stockcodes,
        trade_date=trade_date,
        end_time=end_time,
        url=url,
        token=token,
    )
