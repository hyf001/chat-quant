#!/usr/bin/env python3
"""Safe diagnostics for the portable MindGo MCP bundle."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

from launch_mcp import bundle_root, load_env_file


PLACEHOLDER_PARTS = ("example.com", "replace-with", "your-")


def is_configured(value: str | None) -> bool:
    text = str(value or "").strip().lower()
    return bool(text) and not any(part in text for part in PLACEHOLDER_PARTS)


def safe_origin(value: str) -> str:
    split = urlsplit(value)
    if not split.scheme or not split.netloc:
        return "<invalid URL>"
    return f"{split.scheme}://{split.netloc}/…"


def request_json(url: str, token: str, auth_scheme: str, path: str) -> object:
    request = Request(
        f"{url.rstrip('/')}{path}",
        headers={"Authorization": f"{auth_scheme} {token}", "Accept": "application/json"},
    )
    context = ssl.create_default_context()
    with urlopen(request, timeout=15, context=context) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="contact the configured Jupyter API")
    args = parser.parse_args()

    root = bundle_root()
    environment = load_env_file(root / ".env")
    print(f"[ok] bundle root: {root}")
    print(f"[ok] Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 11):
        print("[fail] Python 3.11+ is required", file=sys.stderr)
        return 1

    try:
        version = importlib.metadata.version("supermind-mcp")
    except importlib.metadata.PackageNotFoundError:
        print("[fail] supermind-mcp is not installed; run the setup script", file=sys.stderr)
        return 1
    print(f"[ok] supermind-mcp: {version}")

    url = environment.get("JUPYTER_URL", "")
    token = environment.get("JUPYTER_TOKEN", "")
    auth_scheme = environment.get("JUPYTER_AUTH_SCHEME", "Bearer") or "Bearer"
    notebook = environment.get(
        "MINDGO_INTRADAY_NOTEBOOK_PATH", "deepsolo_v3/少标的分时实时.ipynb"
    )

    print(f"[{'ok' if is_configured(url) else 'warn'}] JUPYTER_URL: " + (safe_origin(url) if is_configured(url) else "not configured"))
    print(f"[{'ok' if is_configured(token) else 'warn'}] JUPYTER_TOKEN: " + ("configured (hidden)" if is_configured(token) else "not configured"))
    print(f"[ok] intraday notebook path: {notebook}")

    if not args.live:
        print("[ok] local checks complete; use --live after configuring .env")
        return 0
    if not is_configured(url) or not is_configured(token):
        print("[fail] live check requires real JUPYTER_URL and JUPYTER_TOKEN values", file=sys.stderr)
        return 2

    try:
        kernels = request_json(url, token, auth_scheme, "/api/kernels")
        kernel_count = len(kernels) if isinstance(kernels, list) else "unknown"
        print(f"[ok] authenticated Jupyter API; active kernels: {kernel_count}")
    except HTTPError as exc:
        print(f"[fail] Jupyter API returned HTTP {exc.code}", file=sys.stderr)
        return 3
    except (URLError, TimeoutError, ssl.SSLError, ValueError) as exc:
        print(f"[fail] cannot reach Jupyter API: {type(exc).__name__}", file=sys.stderr)
        return 3

    notebook_path = "/api/contents/" + quote(notebook.strip("/"), safe="/")
    try:
        request_json(url, token, auth_scheme, notebook_path)
        print("[ok] configured intraday notebook exists")
    except HTTPError as exc:
        if exc.code == 404:
            print("[warn] configured notebook was not found; create it or change MINDGO_INTRADAY_NOTEBOOK_PATH")
        else:
            print(f"[warn] notebook check returned HTTP {exc.code}")
    except (URLError, TimeoutError, ssl.SSLError, ValueError) as exc:
        print(f"[warn] notebook check failed: {type(exc).__name__}")

    print("[ok] live doctor checks complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
