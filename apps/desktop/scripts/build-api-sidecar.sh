#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DIST_DIR="$ROOT_DIR/apps/desktop/sidecars"
WORK_DIR="$ROOT_DIR/.dev/pyinstaller"

mkdir -p "$DIST_DIR" "$WORK_DIR"
rm -rf "$DIST_DIR/chat-quant-api" "$DIST_DIR/chat-quant-api.exe"

uv run --project "$ROOT_DIR/apps/api" pyinstaller \
  --clean \
  --noconfirm \
  --onedir \
  --name chat-quant-api \
  --hidden-import aiosqlite \
  --hidden-import aiosqlite.core \
  --collect-data akshare \
  --collect-binaries claude_agent_sdk \
  --collect-data claude_agent_sdk \
  --paths "$ROOT_DIR/apps/api" \
  --distpath "$DIST_DIR" \
  --workpath "$WORK_DIR" \
  "$ROOT_DIR/apps/api/app/desktop_entry.py"
