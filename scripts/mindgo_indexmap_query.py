#!/usr/bin/env python3
"""Fetch MindGo indexmap data through the remote Jupyter runtime.

The MindGo ``get_arsenal_api`` helper only exists inside the authorized
MindGo/SuperMind runtime. This script reads Jupyter settings from the repo
``.env``, executes a read-only ``query_index`` call remotely, then saves the
raw JSON and a best-effort tabular CSV locally.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
PORTABLE_MCP_ROOT = REPO_ROOT / "docs" / "mindgo" / "mindgo-mcp-portable"
sys.path.insert(0, str(PORTABLE_MCP_ROOT))

from supermind_mcp.config import resolve_config  # noqa: E402
from supermind_mcp.jupyter_api import JupyterAPI  # noqa: E402
from supermind_mcp.jupyter_ws import execute_code_ws  # noqa: E402

DEFAULT_QUERY_ID = "982"
DEFAULT_POD = "cbas-babel-frondend-pod"
DEFAULT_NOTEBOOK_PATH = "deepsolo_v3/少标的分时实时.ipynb"
MARKER_START = "MINDGO_INDEXMAP_JSON_START"
MARKER_END = "MINDGO_INDEXMAP_JSON_END"


@dataclass(frozen=True)
class ParsedIndexmap:
    raw: dict[str, Any]
    rows: list[dict[str, Any]]
    titles: list[dict[str, Any]]


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)
    if not args.notebook_path:
        args.notebook_path = (
            os.getenv("MINDGO_INTRADAY_NOTEBOOK_PATH") or DEFAULT_NOTEBOOK_PATH
        )

    try:
        result = asyncio.run(fetch_indexmap(args))
    except Exception as exc:  # noqa: BLE001
        print(redact(str(exc)), file=sys.stderr)
        return 1

    raw_path = args.output_dir / f"indexmap_{args.query_id}_{args.base_day}.json"
    csv_path = args.output_dir / f"indexmap_{args.query_id}_{args.base_day}.csv"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(
        json.dumps(result.raw, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    df = pd.DataFrame(result.rows)
    if not df.empty:
        df.insert(0, "trade_date", args.base_day)
        df.insert(1, "query_id", args.query_id)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"query_id: {args.query_id}")
    print(f"base_day: {args.base_day}")
    print(f"rows: {len(df)}")
    print(f"raw_json: {raw_path}")
    print(f"csv: {csv_path}")
    if not df.empty:
        print(df.head(args.preview_rows).to_string(index=False))
    else:
        print("No tabular rows were recognized. Check raw_json for the returned shape.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch MindGo indexmap/query_index data through remote Jupyter."
    )
    parser.add_argument("--query-id", default=DEFAULT_QUERY_ID, help="indexmap queryId")
    parser.add_argument(
        "--base-day",
        default=datetime.now().strftime("%Y%m%d"),
        help="Trading date in YYYYMMDD format. Defaults to today.",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=REPO_ROOT / ".env",
        help="Path to .env containing JUPYTER_URL/JUPYTER_TOKEN.",
    )
    parser.add_argument(
        "--notebook-path",
        default=None,
        help="Remote notebook/session path used to create or reuse a kernel.",
    )
    parser.add_argument(
        "--kernel-id",
        default=None,
        help="Reuse an existing Jupyter kernel id instead of creating/finding a session.",
    )
    parser.add_argument("--pod", default=DEFAULT_POD, help="Arsenal pod name.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "data" / "mindgo",
        help="Directory for JSON and CSV outputs.",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--preview-rows", type=int, default=10)
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_env_value(value.strip())
        if key and key not in os.environ:
            os.environ[key] = value


def strip_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


async def fetch_indexmap(args: argparse.Namespace) -> ParsedIndexmap:
    config = resolve_config()
    async with JupyterAPI(config) as api:
        kernel_id = args.kernel_id or await find_or_create_kernel(
            api,
            normalize_remote_path(args.notebook_path),
        )
        execution = await execute_code_ws(
            kernel_id,
            remote_query_code(
                query_id=args.query_id,
                base_day=args.base_day,
                pod=args.pod,
            ),
            timeout=args.timeout,
        )

    if execution.error:
        raise RuntimeError("Remote MindGo execution failed: " + json.dumps(execution.error))

    stdout = "".join(execution.stdout)
    payload = extract_marked_json(stdout)
    if payload.get("error"):
        raise RuntimeError("Remote MindGo query failed: " + json.dumps(payload, ensure_ascii=False))

    raw = payload.get("raw")
    if not isinstance(raw, dict):
        raise RuntimeError("Remote MindGo query did not return a JSON object")
    return parse_indexmap(raw)


async def find_or_create_kernel(api: JupyterAPI, notebook_path: str) -> str:
    sessions = await api.client.get("/api/sessions")
    ensure_success(sessions.status_code, "listing Jupyter sessions")
    for session in sessions.json():
        if session.get("path") == notebook_path:
            kernel_id = (session.get("kernel") or {}).get("id")
            if kernel_id:
                return str(kernel_id)

    response = await api.client.post(
        "/api/sessions",
        json={
            "path": notebook_path,
            "type": "notebook",
            "name": notebook_path.rsplit("/", 1)[-1],
            "kernel": {"name": "python3"},
        },
    )
    ensure_success(response.status_code, "creating Jupyter session")
    kernel_id = (response.json().get("kernel") or {}).get("id")
    if not kernel_id:
        raise RuntimeError(f"Could not create kernel for notebook path: {notebook_path}")
    return str(kernel_id)


def ensure_success(status_code: int, action: str) -> None:
    if status_code >= 400:
        raise RuntimeError(f"Jupyter API returned HTTP {status_code} while {action}")


def normalize_remote_path(path: str) -> str:
    return path.strip().strip("/")


def remote_query_code(*, query_id: str, base_day: str, pod: str) -> str:
    return f"""
import json
import math
import traceback

QUERY_ID = {json.dumps(str(query_id), ensure_ascii=False)}
BASE_DAY = {json.dumps(str(base_day), ensure_ascii=False)}
POD = {json.dumps(str(pod), ensure_ascii=False)}
MARKER_START = {json.dumps(MARKER_START)}
MARKER_END = {json.dumps(MARKER_END)}


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


def token_looks_invalid(value):
    text = str(value).lower()
    auth_words = [
        "unauthorized",
        "forbidden",
        "login",
        "expired",
        "invalid token",
        "token invalid",
        "token expired",
        "token失效",
        "token过期",
        "未登录",
        "登录失效",
        "认证失败",
        "权限",
    ]
    if any(word in text for word in auth_words):
        return True
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key).lower()
            if key_text in {{"status", "status_code", "code"}} and str(item) in {{"401", "403"}}:
                return True
            if token_looks_invalid(item):
                return True
    if isinstance(value, (list, tuple)):
        for item in value:
            if token_looks_invalid(item):
                return True
    return False


payload = {{"query_id": QUERY_ID, "base_day": BASE_DAY, "raw": None}}
try:
    def query_index():
        api = get_arsenal_api(POD)
        response = api.post(
            "/babel/api/query_index",
            files={{"queryId": (None, QUERY_ID), "baseDay": (None, BASE_DAY)}},
        )
        status_code = None
        try:
            status_code = response.status_code
        except Exception:
            pass
        return status_code, jsonable(response.json())

    def refresh_public_open_api_token():
        open_api = get_open_api("public")
        return jsonable(open_api.get_llminfo())

    status_code, raw = query_index()
    payload["status_code"] = status_code
    payload["raw"] = raw
    if token_looks_invalid(raw):
        payload["token_refresh"] = refresh_public_open_api_token()
        status_code, raw = query_index()
        payload["status_code"] = status_code
        payload["raw"] = raw
        payload["retried_after_token_refresh"] = True
except Exception as exc:
    payload["first_error"] = str(exc)
    try:
        payload["token_refresh"] = refresh_public_open_api_token()
        status_code, raw = query_index()
        payload["status_code"] = status_code
        payload["raw"] = raw
        payload["retried_after_token_refresh"] = True
    except Exception as retry_exc:
        payload["error"] = str(retry_exc)
        payload["traceback"] = traceback.format_exc(limit=8)

print(MARKER_START)
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print(MARKER_END)
"""


def extract_marked_json(stdout: str) -> dict[str, Any]:
    start = stdout.find(MARKER_START)
    end = stdout.find(MARKER_END, start + len(MARKER_START))
    if start < 0 or end < 0:
        preview = stdout[-2000:] if stdout else "<empty stdout>"
        raise RuntimeError(f"Could not find MindGo JSON markers in stdout: {preview}")
    text = stdout[start + len(MARKER_START) : end].strip()
    return json.loads(text)


def parse_indexmap(raw: dict[str, Any]) -> ParsedIndexmap:
    titles = title_items(raw)
    label_by_key = {
        str(item["key"]): str(item.get("label") or item["key"])
        for item in titles
        if isinstance(item, dict) and item.get("key")
    }
    title_keys = [str(item["key"]) for item in titles if isinstance(item, dict) and item.get("key")]

    row_values = first_row_list(raw, title_keys=title_keys)
    rows: list[dict[str, Any]] = []
    for row in row_values:
        normalized = normalize_row(row, title_keys=title_keys)
        if normalized:
            rows.append(rename_row(normalized, label_by_key))
    return ParsedIndexmap(raw=raw, rows=rows, titles=titles)


def title_items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        titles = value.get("titles") or value.get("columns") or value.get("headers")
        if isinstance(titles, list):
            parsed = []
            for item in titles:
                if isinstance(item, dict) and item.get("key"):
                    parsed.append(item)
                elif isinstance(item, str):
                    parsed.append({"key": item, "label": item})
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


def first_row_list(value: Any, *, title_keys: list[str]) -> list[Any]:
    candidates = list(row_list_candidates(value, title_keys=title_keys))
    if not candidates:
        return []
    candidates.sort(key=lambda rows: row_score(rows, title_keys=title_keys), reverse=True)
    return candidates[0]


def row_list_candidates(value: Any, *, title_keys: list[str]) -> Iterable[list[Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"titles", "columns", "headers"}:
                continue
            if isinstance(child, list) and looks_like_rows(child, title_keys=title_keys):
                yield child
            yield from row_list_candidates(child, title_keys=title_keys)
    elif isinstance(value, list):
        if looks_like_rows(value, title_keys=title_keys):
            yield value
        for child in value:
            yield from row_list_candidates(child, title_keys=title_keys)


def looks_like_rows(value: list[Any], *, title_keys: list[str]) -> bool:
    if not value:
        return False
    sample = value[: min(5, len(value))]
    if all(isinstance(item, dict) for item in sample):
        return any(row_score([item], title_keys=title_keys) > 0 for item in sample)
    if title_keys and all(isinstance(item, list | tuple) for item in sample):
        return True
    return False


def row_score(rows: list[Any], *, title_keys: list[str]) -> int:
    score = len(rows)
    first = rows[0] if rows else None
    if isinstance(first, dict):
        keys = {str(key) for key in first}
        score += 100 * len(keys.intersection(title_keys))
        score += 20 * int(any(key.lower() in {"stockcode", "code", "symbol"} for key in keys))
        score += len(keys)
    elif isinstance(first, list | tuple):
        score += 50 * int(bool(title_keys))
        score += len(first)
    return score


def normalize_row(row: Any, *, title_keys: list[str]) -> dict[str, Any]:
    if isinstance(row, dict):
        return {str(key): value for key, value in row.items()}
    if isinstance(row, list | tuple) and title_keys:
        keys = title_keys[: len(row)]
        return {key: value for key, value in zip(keys, row, strict=False)}
    return {}


def rename_row(row: dict[str, Any], label_by_key: dict[str, str]) -> dict[str, Any]:
    renamed: dict[str, Any] = {}
    for key, value in row.items():
        label = label_by_key.get(key, key)
        column = unique_column_name(label, renamed)
        renamed[column] = value
    return renamed


def unique_column_name(label: str, row: dict[str, Any]) -> str:
    if label not in row:
        return label
    index = 2
    while f"{label}_{index}" in row:
        index += 1
    return f"{label}_{index}"


def redact(text: str) -> str:
    token = os.getenv("JUPYTER_TOKEN", "")
    if token:
        text = text.replace(token, "***")
    return re.sub(r"token=[^&\\s]+", "token=***", text)


if __name__ == "__main__":
    raise SystemExit(main())
