#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_DIR="$ROOT_DIR/.dev/pids"
API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-5173}"

stop_service() {
  local name="$1"
  local pid_file="$2"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name is not running (no pid file)"
    return
  fi

  local pid
  pid="$(cat "$pid_file")"
  if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
    echo "$name is not running (stale pid file)"
    rm -f "$pid_file"
    return
  fi

  echo "Stopping $name (pid $pid)..."
  kill "$pid" 2>/dev/null || true

  for _ in {1..30}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$pid_file"
      echo "$name stopped"
      return
    fi
    sleep 0.2
  done

  echo "$name did not stop gracefully; forcing..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$pid_file"
  echo "$name stopped"
}

stop_service "web" "$PID_DIR/web.pid"
stop_service "api" "$PID_DIR/api.pid"

stop_port() {
  local name="$1"
  local port="$2"
  local pids
  pids="$(lsof -ti "tcp:$port" 2>/dev/null || true)"
  if [[ -z "$pids" ]]; then
    return
  fi

  echo "Stopping $name processes still listening on port $port..."
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true
}

stop_port "web" "$WEB_PORT"
stop_port "api" "$API_PORT"
