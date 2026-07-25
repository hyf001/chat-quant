#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.dev"
PID_DIR="$STATE_DIR/pids"
LOG_DIR="$STATE_DIR/logs"
API_PID_FILE="$PID_DIR/api.pid"
WEB_PID_FILE="$PID_DIR/web.pid"
API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-5173}"
API_HOST="${API_HOST:-127.0.0.1}"
WEB_HOST="${WEB_HOST:-127.0.0.1}"

mkdir -p "$PID_DIR" "$LOG_DIR"

is_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid="$(cat "$pid_file")"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

start_service() {
  local name="$1"
  local pid_file="$2"
  local log_file="$3"
  shift 3

  if is_running "$pid_file"; then
    echo "$name already running (pid $(cat "$pid_file"))"
    return
  fi

  rm -f "$pid_file"
  echo "Starting $name..."
  (
    cd "$ROOT_DIR"
    "$@"
  ) >"$log_file" 2>&1 &
  echo "$!" >"$pid_file"
  echo "$name started (pid $(cat "$pid_file"), log $log_file)"
}

start_service \
  "api" \
  "$API_PID_FILE" \
  "$LOG_DIR/api.log" \
  uv run --project apps/api uvicorn app.main:app --reload --app-dir apps/api --host "$API_HOST" --port "$API_PORT"

start_service \
  "web" \
  "$WEB_PID_FILE" \
  "$LOG_DIR/web.log" \
  npm --prefix apps/web run dev -- --host "$WEB_HOST" --port "$WEB_PORT"

echo
echo "Dev services are running:"
echo "  API: http://$API_HOST:$API_PORT/api/health"
echo "  Web: http://$WEB_HOST:$WEB_PORT"
echo
echo "Logs:"
echo "  tail -f $LOG_DIR/api.log"
echo "  tail -f $LOG_DIR/web.log"
echo
echo "Stop with: npm run dev:stop"
