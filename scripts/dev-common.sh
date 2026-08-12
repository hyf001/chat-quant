#!/usr/bin/env bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.dev"
PID_DIR="$STATE_DIR/pids"
LOG_DIR="$STATE_DIR/logs"

API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
WEB_HOST="${WEB_HOST:-127.0.0.1}"
WEB_PORT="${WEB_PORT:-5173}"
DESKTOP_API_HOST="${DESKTOP_API_HOST:-127.0.0.1}"
DESKTOP_API_PORT="${DESKTOP_API_PORT:-${CHATQ_DESKTOP_API_PORT:-12345}}"

UV_CACHE_DIR="${UV_CACHE_DIR:-${TMPDIR:-/tmp}/chat-quant-uv-cache}"
WATCHFILES_FORCE_POLLING="${WATCHFILES_FORCE_POLLING:-true}"

mkdir -p "$PID_DIR" "$LOG_DIR" "$UV_CACHE_DIR"
export UV_CACHE_DIR
export WATCHFILES_FORCE_POLLING
export CHATQ_DESKTOP_API_PORT="$DESKTOP_API_PORT"

is_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1

  local pid
  pid="$(cat "$pid_file")"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

print_recent_log() {
  local log_file="$1"
  if [[ -f "$log_file" ]]; then
    tail -n 80 "$log_file" || true
  fi
}

wait_for_url() {
  local url="$1"
  local timeout_seconds="$2"
  local attempts=$((timeout_seconds * 4))

  for ((attempt = 1; attempt <= attempts; attempt += 1)); do
    if curl -fsS --max-time 1 "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.25
  done

  return 1
}

start_service() {
  local name="$1"
  local pid_file="$2"
  local log_file="$3"
  local ready_url="$4"
  local timeout_seconds="$5"
  shift 5

  if is_running "$pid_file"; then
    echo "$name already running (pid $(cat "$pid_file"))"
    return 0
  fi

  rm -f "$pid_file"
  echo "Starting $name..."
  (
    cd "$ROOT_DIR"
    nohup "$@" >"$log_file" 2>&1 &
    echo "$!" >"$pid_file"
  )

  local attempts=$((timeout_seconds * 4))
  for ((attempt = 1; attempt <= attempts; attempt += 1)); do
    if [[ -n "$ready_url" ]] && curl -fsS --max-time 1 "$ready_url" >/dev/null 2>&1; then
      echo "$name started (pid $(cat "$pid_file"), log $log_file)"
      return 0
    fi

    if ! is_running "$pid_file"; then
      rm -f "$pid_file"
      echo "$name failed to start. Recent log output:"
      print_recent_log "$log_file"
      return 1
    fi

    sleep 0.25
  done

  if [[ -z "$ready_url" ]]; then
    echo "$name started (pid $(cat "$pid_file"), log $log_file)"
    return 0
  fi

  echo "$name did not become ready at $ready_url. Recent log output:"
  print_recent_log "$log_file"
  return 1
}

process_tree() {
  local pid="$1"
  local child

  echo "$pid"
  for child in $(pgrep -P "$pid" 2>/dev/null || true); do
    process_tree "$child"
  done
}

stop_service() {
  local name="$1"
  local pid_file="$2"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name is not running (no pid file)"
    return 0
  fi

  local pid
  pid="$(cat "$pid_file")"
  if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
    echo "$name is not running (stale pid file)"
    rm -f "$pid_file"
    return 0
  fi

  local pids
  pids="$(process_tree "$pid" | awk '!seen[$0]++')"
  echo "Stopping $name (pid $pid)..."
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true

  for _ in {1..40}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$pid_file"
      echo "$name stopped"
      return 0
    fi
    sleep 0.25
  done

  echo "$name did not stop gracefully; forcing..."
  # shellcheck disable=SC2086
  kill -9 $pids 2>/dev/null || true
  rm -f "$pid_file"
  echo "$name stopped"
}

stop_port() {
  local name="$1"
  local port="$2"
  local pids

  pids="$(lsof -ti "tcp:$port" 2>/dev/null || true)"
  if [[ -z "$pids" ]]; then
    return 0
  fi

  echo "Stopping $name processes still listening on port $port..."
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true
}
