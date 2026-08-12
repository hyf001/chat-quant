#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if command -v python3 >/dev/null 2>&1; then
  SYSTEM_PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  SYSTEM_PYTHON="$(command -v python)"
else
  echo "Python 3.11+ is required. Install Python, then run this script again." >&2
  exit 2
fi

"$SYSTEM_PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else "Python 3.11+ is required")'

if command -v uv >/dev/null 2>&1; then
  echo "Installing locked dependencies with uv..."
  uv sync --extra dev --locked
else
  echo "uv not found; using Python venv + pip fallback."
  "$SYSTEM_PYTHON" -m venv .venv
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -e '.[dev]'
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from the secret-free template. Replace its placeholders before live tests."
fi

chmod +x scripts/setup.sh scripts/run_mcp.sh

echo "Running unit tests..."
.venv/bin/python -m pytest tests -q

echo "Running credential-free MCP protocol test..."
.venv/bin/python scripts/smoke_test.py --protocol --launcher

echo "Setup complete. Edit $ROOT/.env, then run:"
echo "  $ROOT/.venv/bin/python $ROOT/scripts/doctor.py --live"
echo "  $ROOT/.venv/bin/python $ROOT/scripts/smoke_test.py --live"
