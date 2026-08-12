#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "MindGo MCP is not installed. Run $ROOT/scripts/setup.sh first." >&2
  exit 2
fi

exec "$PYTHON" "$ROOT/scripts/launch_mcp.py"
