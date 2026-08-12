"""MindGo realtime intraday data helper."""

from __future__ import annotations

import json
import math
import os
import ssl
import uuid
from datetime import datetime
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

import httpx
import certifi
import websockets
from zoneinfo import ZoneInfo

from .config import resolve_config


DEFAULT_NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"
MARKER_START = "MINDGO_INTRADAY_REALTIME_JSON_START"
MARKER_END = "MINDGO_INTRADAY_REALTIME_JSON_END"
SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


async def stock_intraday_realtime(
    *,
    stockcode: str,
    trade_date: str,
    end_time: str | None = None,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch 1m intraday bars for one stock from MindGo get_price.

    Input stockcode accepts 000001.SZ or plain 000001. trade_date must be YYYYMMDD.
    end_time defaults to the current Shanghai trading minute for today, or 15:00 for
    historical dates.
    """

    code = _normalize_stockcode(stockcode)
    date = _clean_date(trade_date)
    if not code:
        raise ValueError("stockcode must be a 6-digit A-share code, e.g. 000001.SZ")
    if not date:
        raise ValueError("trade_date must be YYYYMMDD")
    target_end = _normalize_bar_time(end_time) or _default_end_time(date)
    result = await stock_intraday_realtime_batch(
        stockcodes=[code],
        trade_date=date,
        end_time=target_end,
        url=url,
        token=token,
    )
    items = result.get("items") if isinstance(result.get("items"), list) else []
    return items[0] if items else {
        "stockcode": code,
        "trade_date": date,
        "end_time": target_end,
        "rows": [],
        "message": "MindGo returned no rows",
    }


async def stock_intraday_realtime_batch(
    *,
    stockcodes: list[str],
    trade_date: str,
    end_time: str | None = None,
    url: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch 1m intraday bars for a small stock list from MindGo get_price."""

    codes = []
    for raw in stockcodes:
        code = _normalize_stockcode(raw)
        if code and code not in codes:
            codes.append(code)
    date = _clean_date(trade_date)
    if not codes:
        raise ValueError("stockcodes must include at least one valid stock code")
    if not date:
        raise ValueError("trade_date must be YYYYMMDD")
    target_end = _normalize_bar_time(end_time) or _default_end_time(date)
    config = resolve_config(url=url, token=token)
    notebook_path = _notebook_path()
    kernel_id = await _find_or_create_kernel(
        config.url, config.token, config.auth_scheme, notebook_path
    )
    output = await _execute_code(
        config.url,
        config.token,
        config.auth_scheme,
        kernel_id,
        _remote_code(codes, date, target_end),
    )
    if output.get("error"):
        raise RuntimeError(json.dumps(output["error"], ensure_ascii=False))
    payload = _parse_marker_json("".join(output.get("stdout") or []))
    if payload.get("error"):
        raise RuntimeError(str(payload["error"]))
    item_map = payload.get("items") if isinstance(payload.get("items"), dict) else {}
    items = [_payload_item(code, date, target_end, item_map.get(code) if isinstance(item_map.get(code), list) else []) for code in codes]
    return {
        "trade_date": date,
        "start_time": "09:30",
        "end_time": target_end,
        "source": "mindgo_get_price",
        "notebook_path": notebook_path,
        "item_count": len(items),
        "items": items,
    }


async def _find_or_create_kernel(
    url: str, token: str, auth_scheme: str, notebook_path: str
) -> str:
    headers = {"Authorization": f"{auth_scheme} {token}"}
    async with httpx.AsyncClient(
        base_url=url,
        headers=headers,
        timeout=httpx.Timeout(30.0, connect=10.0),
        follow_redirects=True,
    ) as client:
        response = await client.get("/api/sessions")
        response.raise_for_status()
        for session in response.json():
            if session.get("path") == notebook_path:
                kernel_id = (session.get("kernel") or {}).get("id")
                if kernel_id:
                    return str(kernel_id)
        response = await client.post(
            "/api/sessions",
            json={
                "path": notebook_path,
                "type": "notebook",
                "name": notebook_path.rsplit("/", 1)[-1],
                "kernel": {"name": "python3"},
            },
        )
        response.raise_for_status()
        kernel_id = (response.json().get("kernel") or {}).get("id")
        if not kernel_id:
            raise RuntimeError(f"Cannot create kernel for {notebook_path}")
        return str(kernel_id)


def _notebook_path() -> str:
    return (
        os.getenv("MINDGO_INTRADAY_NOTEBOOK_PATH") or DEFAULT_NOTEBOOK_PATH
    ).strip().strip("/") or DEFAULT_NOTEBOOK_PATH


async def _execute_code(
    url: str,
    token: str,
    auth_scheme: str,
    kernel_id: str,
    code: str,
) -> dict[str, Any]:
    msg_id = uuid.uuid4().hex
    message = {
        "header": {
            "msg_id": msg_id,
            "username": "supermind-mcp",
            "session": uuid.uuid4().hex,
            "msg_type": "execute_request",
            "version": "5.3",
        },
        "parent_header": {},
        "metadata": {},
        "content": {
            "code": code,
            "silent": False,
            "store_history": False,
            "user_expressions": {},
            "allow_stdin": False,
            "stop_on_error": True,
        },
        "channel": "shell",
        "buffers": [],
    }
    result: dict[str, Any] = {"stdout": [], "stderr": [], "result": None, "error": None}
    ws_url = _kernel_ws_url(url, token, kernel_id)
    async with websockets.connect(
        ws_url,
        additional_headers={"Authorization": f"{auth_scheme} {token}"},
        ssl=_ws_ssl_context(ws_url),
    ) as websocket:
        await websocket.send(json.dumps(message))
        while True:
            payload = json.loads(await websocket.recv())
            if (payload.get("parent_header") or {}).get("msg_id") != msg_id:
                continue
            msg_type = (payload.get("header") or {}).get("msg_type")
            content = payload.get("content") or {}
            if msg_type == "stream":
                target = "stderr" if content.get("name") == "stderr" else "stdout"
                result[target].append(str(content.get("text") or ""))
            elif msg_type == "execute_result":
                data = content.get("data") or {}
                result["result"] = data.get("text/plain") if isinstance(data, dict) else data
            elif msg_type == "error":
                result["error"] = {
                    "ename": content.get("ename"),
                    "evalue": content.get("evalue"),
                    "traceback": content.get("traceback", []),
                }
            elif msg_type == "execute_reply":
                if content.get("status") == "error" and not result.get("error"):
                    result["error"] = {
                        "ename": content.get("ename"),
                        "evalue": content.get("evalue"),
                        "traceback": content.get("traceback", []),
                    }
                return result


def _remote_code(stockcodes: list[str], trade_date: str, end_time: str) -> str:
    return f"""
import json
import math
import traceback

import pandas as pd

TRADE_DATE = {json.dumps(trade_date)}
STOCK_LIST = {json.dumps(stockcodes, ensure_ascii=False)}
START_TIME = TRADE_DATE + " 09:30"
END_TIME = TRADE_DATE + " {end_time}"
FIELDS = ["close", "high", "low", "open", "volume", "turnover"]


def _json_value(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    try:
        if hasattr(value, "item"):
            value = value.item()
    except Exception:
        pass
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _time_text(value):
    if hasattr(value, "strftime"):
        return value.strftime("%H:%M")
    text = str(value)
    if len(text) >= 16 and ":" in text:
        return text[-8:-3]
    return text[:5]


def _frame(value, field):
    if isinstance(value, dict):
        data = value.get(field)
    else:
        try:
            data = value[field]
        except Exception:
            data = getattr(value, field, None)
    if data is None:
        return None
    try:
        return pd.DataFrame(data)
    except Exception:
        return None


def _cell(frame, ts, stock):
    if frame is None or frame.empty:
        return None
    candidates = [stock, stock.split(".")[0]]
    for candidate in candidates:
        if candidate in frame.columns:
            try:
                return _json_value(frame.loc[ts, candidate])
            except Exception:
                pass
    if len(frame.columns) == 1:
        try:
            return _json_value(frame.loc[ts, frame.columns[0]])
        except Exception:
            return None
    return None


payload = {{"schema_version": 1, "source": "mindgo_get_price", "trade_date": TRADE_DATE, "start_time": "09:30", "end_time": {json.dumps(end_time)}, "items": {{}}}}
try:
    value = get_price(STOCK_LIST, START_TIME, END_TIME, "1m", FIELDS, True, None, 0, is_panel=1)
    frames = {{field: _frame(value, field) for field in FIELDS}}
    all_times = []
    for frame in frames.values():
        if frame is None:
            continue
        for item in list(frame.index):
            if item not in all_times:
                all_times.append(item)
    for stock in STOCK_LIST:
        rows = []
        for ts in sorted(all_times):
            row = {{
                "stockcode": stock,
                "trade_date": TRADE_DATE,
                "bar_time": _time_text(ts),
                "open": _cell(frames.get("open"), ts, stock),
                "high": _cell(frames.get("high"), ts, stock),
                "low": _cell(frames.get("low"), ts, stock),
                "close": _cell(frames.get("close"), ts, stock),
                "volume": _cell(frames.get("volume"), ts, stock),
                "amount": _cell(frames.get("turnover"), ts, stock),
            }}
            if any(row.get(key) is not None for key in ("open", "high", "low", "close")):
                rows.append(row)
        payload["items"][stock] = rows
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=5)
print({json.dumps(MARKER_START)})
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print({json.dumps(MARKER_END)})
"""


def _payload_item(stockcode: str, trade_date: str, end_time: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = []
    for row in rows:
        bar_time = _normalize_bar_time(row.get("bar_time"))
        if not bar_time:
            continue
        normalized.append({
            "stockcode": stockcode,
            "trade_date": trade_date,
            "bar_time": bar_time,
            "open": _round_float(row.get("open"), 4),
            "high": _round_float(row.get("high"), 4),
            "low": _round_float(row.get("low"), 4),
            "close": _round_float(row.get("close"), 4),
            "volume": _round_float(row.get("volume"), 2),
            "amount": _round_float(row.get("amount"), 2),
        })
    normalized.sort(key=lambda item: item["bar_time"])
    return {
        "stockcode": stockcode,
        "trade_date": trade_date,
        "start_time": "09:30",
        "end_time": end_time,
        "as_of_time": normalized[-1]["bar_time"] if normalized else "",
        "source": "mindgo_get_price",
        "row_count": len(normalized),
        "rows": normalized,
        "summary": {
            "last_price": normalized[-1].get("close") if normalized else None,
            "high_since_open": max((row.get("high") or 0 for row in normalized), default=None),
            "low_since_open": min((row.get("low") or 0 for row in normalized), default=None),
            "total_volume": sum((row.get("volume") or 0 for row in normalized)),
            "total_amount": sum((row.get("amount") or 0 for row in normalized)),
        },
        "message": "" if normalized else "MindGo returned no rows",
    }


def _parse_marker_json(stdout: str) -> dict[str, Any]:
    start = stdout.find(MARKER_START)
    end = stdout.find(MARKER_END)
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError(f"Cannot parse realtime intraday output: {stdout[-1200:]}")
    payload = json.loads(stdout[start + len(MARKER_START):end].strip())
    if not isinstance(payload, dict):
        raise RuntimeError("Realtime intraday output is not a JSON object")
    return payload


def _kernel_ws_url(url: str, token: str, kernel_id: str) -> str:
    split = urlsplit(url.rstrip("/"))
    scheme = "wss" if split.scheme == "https" else "ws"
    base_path = split.path.rstrip("/")
    return urlunsplit((scheme, split.netloc, f"{base_path}/api/kernels/{kernel_id}/channels", urlencode({"token": token}), ""))


def _ws_ssl_context(ws_url: str) -> ssl.SSLContext | None:
    if urlsplit(ws_url).scheme != "wss":
        return None
    return ssl.create_default_context(cafile=certifi.where())


def _normalize_stockcode(value: str) -> str:
    text = str(value or "").strip().upper()
    if "." in text:
        code, suffix = text.split(".", 1)
        digits = "".join(ch for ch in code if ch.isdigit())
        market = suffix[:2]
        return f"{digits}.{market}" if len(digits) == 6 and market in {"SH", "SZ", "BJ"} else ""
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) != 6:
        return ""
    if digits.startswith("6"):
        return f"{digits}.SH"
    if digits.startswith(("8", "9")):
        return f"{digits}.BJ"
    return f"{digits}.SZ"


def _clean_date(value: str) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    return digits[:8] if len(digits) >= 8 else ""


def _normalize_bar_time(value: Any) -> str | None:
    text = str(value or "").strip()
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) >= 4:
        candidate = digits[-4:]
        hour = int(candidate[:2])
        minute = int(candidate[2:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    if len(text) >= 5 and text[2] == ":":
        return text[:5]
    return None


def _default_end_time(trade_date: str) -> str:
    now = datetime.now(SHANGHAI_TZ)
    if trade_date != now.strftime("%Y%m%d"):
        return "15:00"
    minute = now.hour * 60 + now.minute
    if minute < 9 * 60 + 30:
        return "09:30"
    if minute <= 11 * 60 + 30:
        return f"{now.hour:02d}:{now.minute:02d}"
    if minute < 13 * 60:
        return "11:30"
    if minute <= 15 * 60:
        return f"{now.hour:02d}:{now.minute:02d}"
    return "15:00"


def _round_float(value: Any, digits: int) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return round(number, digits)
