#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DIST_DIR="$ROOT_DIR/apps/desktop/sidecars"
WORK_DIR="$ROOT_DIR/.dev/pyinstaller"

mkdir -p "$DIST_DIR" "$WORK_DIR"

uv run --project "$ROOT_DIR/apps/api" pyinstaller \
  --clean \
  --noconfirm \
  --onefile \
  --name chat-quant-api \
  --hidden-import aiosqlite \
  --hidden-import aiosqlite.core \
  --paths "$ROOT_DIR/apps/api" \
  --distpath "$DIST_DIR" \
  --workpath "$WORK_DIR" \
  "$ROOT_DIR/apps/api/app/desktop_entry.py"
