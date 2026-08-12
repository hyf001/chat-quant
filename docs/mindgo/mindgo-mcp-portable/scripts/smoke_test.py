#!/usr/bin/env python3
"""Exercise the portable server through the real MCP stdio protocol."""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from launch_mcp import bundle_root, load_env_file


EXPECTED_TOOLS = {
    "list_kernels",
    "create_kernel",
    "execute_code",
    "interrupt_kernel",
    "delete_kernel",
    "sync_files",
    "download_files",
    "stock_intraday_realtime",
    "stock_intraday_realtime_batch",
}


def result_text(result: object) -> str:
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            parts.append(str(text))
    return "\n".join(parts)


def redact(text: str, environment: dict[str, str]) -> str:
    token = environment.get("JUPYTER_TOKEN", "")
    if token:
        text = text.replace(token, "<redacted>")
    return re.sub(r"(?i)(token=)[^&\s]+", r"\1<redacted>", text)


async def run(args: argparse.Namespace) -> None:
    root = bundle_root()
    environment = load_env_file(root / ".env")
    if args.launcher and os.name == "nt":
        command = "powershell.exe"
        command_args = [
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(root / "scripts" / "run_mcp.ps1"),
        ]
    elif args.launcher:
        command = str(root / "scripts" / "run_mcp.sh")
        command_args = []
    else:
        command = sys.executable
        command_args = ["-m", "supermind_mcp.server"]
    parameters = StdioServerParameters(
        command=command,
        args=command_args,
        cwd=str(root),
        env=environment,
    )

    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            catalog = await session.list_tools()
            names = {tool.name for tool in catalog.tools}
            if names != EXPECTED_TOOLS:
                missing = sorted(EXPECTED_TOOLS - names)
                extra = sorted(names - EXPECTED_TOOLS)
                raise RuntimeError(f"tool catalog mismatch; missing={missing}, extra={extra}")
            print(f"PASS protocol initialize/tools-list: {len(names)} tools")

            if not args.live:
                return

            kernels = await session.call_tool("list_kernels", {})
            if getattr(kernels, "isError", False):
                raise RuntimeError("list_kernels failed: " + result_text(kernels))
            print("PASS live list_kernels")

            if args.stockcode:
                arguments = {
                    "stockcode": args.stockcode,
                    "trade_date": args.trade_date,
                }
                if args.end_time:
                    arguments["end_time"] = args.end_time
                stock = await session.call_tool("stock_intraday_realtime", arguments)
                if getattr(stock, "isError", False):
                    raise RuntimeError("stock_intraday_realtime failed: " + result_text(stock))
                print(f"PASS live stock_intraday_realtime: {args.stockcode} {args.trade_date}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--protocol", action="store_true", help="credential-free protocol check")
    mode.add_argument("--live", action="store_true", help="call the configured remote Jupyter server")
    parser.add_argument("--stockcode", help="optional A-share code for the live market-data test")
    parser.add_argument("--trade-date", help="YYYYMMDD trading date used with --stockcode")
    parser.add_argument("--end-time", help="optional HH:MM cutoff used with --stockcode")
    parser.add_argument("--launcher", action="store_true", help="start through scripts/run_mcp.*")
    args = parser.parse_args()
    if not args.protocol and not args.live:
        args.protocol = True
    if args.stockcode and (not args.live or not args.trade_date):
        parser.error("--stockcode requires --live and --trade-date")

    environment = load_env_file(bundle_root() / ".env")
    try:
        asyncio.run(run(args))
    except Exception as exc:
        print("FAIL " + redact(str(exc), environment), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
