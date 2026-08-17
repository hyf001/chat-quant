#!/usr/bin/env bash
# =============================================================
# Stop the local public-access stack started by
# deploy/4_start_local_tunnel.sh:
#   - SSH reverse tunnel
#   - local Caddy entrypoint
#   - Chat-Quant local dev API/Web services
#
# Run locally from the repository root:
#   bash deploy/5_stop_local_tunnel.sh
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/server.config"

if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
fi

LOCAL_PROXY_PORT="${LOCAL_PROXY_PORT:-18080}"
LOCAL_PROXY_HOST="${LOCAL_PROXY_HOST:-127.0.0.1}"
TUNNEL_REMOTE_HOST="${TUNNEL_REMOTE_HOST:-127.0.0.1}"
TUNNEL_REMOTE_PORT="${TUNNEL_REMOTE_PORT:-18080}"
STOP_CHATQ="${STOP_CHATQ:-true}"

STATE_DIR="${ROOT_DIR}/.dev"
PID_DIR="${STATE_DIR}/pids"
CADDY_PID_FILE="${PID_DIR}/local-tunnel-caddy.pid"
SSH_PID_FILE="${PID_DIR}/local-tunnel-ssh.pid"
export NO_PROXY="127.0.0.1,localhost,${NO_PROXY:-}"
export no_proxy="127.0.0.1,localhost,${no_proxy:-}"

is_pid_running() {
    local pid_file="$1"
    [[ -f "$pid_file" ]] || return 1

    local pid
    pid="$(cat "$pid_file")"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

process_tree() {
    local pid="$1"
    local child

    echo "$pid"
    for child in $(pgrep -P "$pid" 2>/dev/null || true); do
        process_tree "$child"
    done
}

stop_pid_file() {
    local name="$1"
    local pid_file="$2"

    if [[ ! -f "$pid_file" ]]; then
        echo "==> ${name} is not running (no pid file)"
        return 0
    fi

    if ! is_pid_running "$pid_file"; then
        echo "==> ${name} is not running (stale pid file)"
        rm -f "$pid_file"
        return 0
    fi

    local pid
    pid="$(cat "$pid_file")"
    local pids
    pids="$(process_tree "$pid" | awk '!seen[$0]++')"

    echo "==> Stopping ${name} (pid ${pid})"
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true

    for _ in {1..40}; do
        if ! kill -0 "$pid" 2>/dev/null; then
            rm -f "$pid_file"
            echo "==> ${name} stopped"
            return 0
        fi
        sleep 0.25
    done

    echo "==> ${name} did not stop gracefully; forcing"
    # shellcheck disable=SC2086
    kill -9 $pids 2>/dev/null || true
    rm -f "$pid_file"
    echo "==> ${name} stopped"
}

find_local_caddy_pid() {
    local pid
    pid="$(lsof -ti "tcp:${LOCAL_PROXY_PORT}" 2>/dev/null | awk 'NR == 1 { print } END { exit 0 }')"
    if [[ -z "$pid" ]]; then
        return 0
    fi

    local command
    command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$command" == *"caddy"* ]]; then
        echo "$pid"
    fi
}

stop_extra_local_caddy_listeners() {
    local pids
    pids="$(lsof -ti "tcp:${LOCAL_PROXY_PORT}" 2>/dev/null || true)"
    if [[ -z "$pids" ]]; then
        return 0
    fi

    local pid
    for pid in $pids; do
        local command
        command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
        if [[ "$command" == *"caddy"* ]]; then
            echo "==> Stopping extra local Caddy listener on port ${LOCAL_PROXY_PORT} (pid ${pid})"
            kill "$pid" 2>/dev/null || true
        fi
    done
}

wait_for_local_proxy_port_clear() {
    for _ in {1..40}; do
        if ! lsof -ti "tcp:${LOCAL_PROXY_PORT}" >/dev/null 2>&1; then
            return 0
        fi
        sleep 0.25
    done
    return 1
}

find_ssh_tunnel_pid() {
    if [[ -z "${SERVER_USER:-}" || -z "${SERVER_IP:-}" ]]; then
        return 0
    fi

    local ssh_target="${SERVER_USER}@${SERVER_IP}"
    ps -axo pid=,command= | awk \
        -v reverse="-R ${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}:${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}" \
        -v target="$ssh_target" \
        'index($0, "ssh ") && index($0, reverse) && index($0, target) && !found { print $1; found = 1 } END { exit 0 }'
}

if ! is_pid_running "$SSH_PID_FILE"; then
    discovered_ssh_pid="$(find_ssh_tunnel_pid)"
    if [[ -n "$discovered_ssh_pid" ]]; then
        echo "$discovered_ssh_pid" > "$SSH_PID_FILE"
    fi
fi

if ! is_pid_running "$CADDY_PID_FILE"; then
    discovered_caddy_pid="$(find_local_caddy_pid)"
    if [[ -n "$discovered_caddy_pid" ]]; then
        echo "$discovered_caddy_pid" > "$CADDY_PID_FILE"
    fi
fi

stop_pid_file "SSH reverse tunnel" "$SSH_PID_FILE"
stop_pid_file "local Caddy" "$CADDY_PID_FILE"
stop_extra_local_caddy_listeners

if [[ "$STOP_CHATQ" == "true" ]]; then
    echo "==> Stopping local Chat-Quant dev services"
    (cd "$ROOT_DIR" && npm run dev:web-stop)
else
    echo "==> Skipping Chat-Quant dev service stop because STOP_CHATQ=${STOP_CHATQ}"
fi

if ! wait_for_local_proxy_port_clear; then
    echo "[!] Port ${LOCAL_PROXY_PORT} is still in use. Check with:"
    echo "    lsof -i tcp:${LOCAL_PROXY_PORT}"
fi

echo "==> Local public-access stack stopped"
