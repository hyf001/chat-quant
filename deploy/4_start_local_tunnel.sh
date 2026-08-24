#!/usr/bin/env bash
# =============================================================
# Start local Chat-Quant services, expose them through a local
# Caddy entrypoint, and keep an SSH reverse tunnel open to Aliyun.
#
# Run locally from the repository root:
#   bash deploy/4_start_local_tunnel.sh
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/server.config"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[x] Missing config file: ${CONFIG_FILE}" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

read_config() {
    (cd "$ROOT_DIR" && python3 "$ROOT_DIR/scripts/read-runtime-config.py" "$1")
}

API_HOST="$(read_config api_host)"
API_PORT="$(read_config api_port)"
LOCAL_PROXY_HOST="${LOCAL_PROXY_HOST:-127.0.0.1}"
LOCAL_PROXY_PORT="${LOCAL_PROXY_PORT:-18080}"
TUNNEL_REMOTE_HOST="${TUNNEL_REMOTE_HOST:-127.0.0.1}"
TUNNEL_REMOTE_PORT="${TUNNEL_REMOTE_PORT:-18080}"
START_CHATQ="${START_CHATQ:-true}"
BUILD_WEB="${BUILD_WEB:-true}"
START_CADDY="${START_CADDY:-true}"
LOCAL_HEALTH_TIMEOUT_SECONDS="${LOCAL_HEALTH_TIMEOUT_SECONDS:-60}"
REMOTE_HEALTH_TIMEOUT_SECONDS="${REMOTE_HEALTH_TIMEOUT_SECONDS:-60}"
CHECK_PUBLIC_URL="${CHECK_PUBLIC_URL:-true}"
CLEAN_REMOTE_TUNNEL="${CLEAN_REMOTE_TUNNEL:-true}"
PUBLIC_AUTH_USER="${PUBLIC_AUTH_USER:-friend}"
PUBLIC_AUTH_PASSWORD_FILE="${PUBLIC_AUTH_PASSWORD_FILE:-${SCRIPT_DIR}/public-auth.password}"
PUBLIC_AUTH_PASSWORD="${PUBLIC_AUTH_PASSWORD:-}"

if [[ -f "$PUBLIC_AUTH_PASSWORD_FILE" ]]; then
    PUBLIC_AUTH_PASSWORD="$(head -n 1 "$PUBLIC_AUTH_PASSWORD_FILE")"
fi

PUBLIC_AUTH_CURL_ARGS=()
if [[ -n "$PUBLIC_AUTH_PASSWORD" ]]; then
    PUBLIC_AUTH_CURL_ARGS=(-u "${PUBLIC_AUTH_USER}:${PUBLIC_AUTH_PASSWORD}")
fi

STATE_DIR="${ROOT_DIR}/.dev"
PID_DIR="${STATE_DIR}/pids"
LOG_DIR="${STATE_DIR}/logs"
CADDY_FILE="${STATE_DIR}/Caddyfile.public-local"
CADDY_PID_FILE="${PID_DIR}/local-tunnel-caddy.pid"
CADDY_LOG_FILE="${LOG_DIR}/local-tunnel-caddy.log"
SSH_PID_FILE="${PID_DIR}/local-tunnel-ssh.pid"
SSH_LOG_FILE="${LOG_DIR}/local-tunnel-ssh.log"
WEB_DIST_DIR="${ROOT_DIR}/apps/web/dist"

mkdir -p "$PID_DIR" "$LOG_DIR"
export NO_PROXY="127.0.0.1,localhost,${NO_PROXY:-}"
export no_proxy="127.0.0.1,localhost,${no_proxy:-}"

SSH_TARGET="${SERVER_USER}@${SERVER_IP}"
SSH_OPTS=(
    -p "${SSH_PORT}"
    -o StrictHostKeyChecking=accept-new
    -o BatchMode=yes
    -o ConnectTimeout=10
    -o ServerAliveInterval=30
    -o ServerAliveCountMax=3
    -o ExitOnForwardFailure=yes
)

if [[ -n "${SSH_KEY_PATH:-}" ]]; then
    if [[ ! -f "$SSH_KEY_PATH" ]]; then
        echo "[x] Missing SSH key file: ${SSH_KEY_PATH}" >&2
        exit 1
    fi
    SSH_OPTS+=(-i "$SSH_KEY_PATH")
fi

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

    if ! is_pid_running "$pid_file"; then
        rm -f "$pid_file"
        return 0
    fi

    local pid
    pid="$(cat "$pid_file")"
    local pids
    pids="$(process_tree "$pid" | awk '!seen[$0]++')"
    echo "==> Stopping stale ${name} (pid ${pid})"
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true

    for _ in {1..40}; do
        if ! kill -0 "$pid" 2>/dev/null; then
            rm -f "$pid_file"
            return 0
        fi
        sleep 0.25
    done

    echo "==> Forcing stale ${name} to stop"
    # shellcheck disable=SC2086
    kill -9 $pids 2>/dev/null || true
    rm -f "$pid_file"
}

local_entrypoint_ready() {
    curl --noproxy '*' -fsS --max-time 1 -H "Host: ${DOMAIN}" "http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}/api/health" | grep -q 'chat-quant-api'
}

remote_entrypoint_ready() {
    ssh "${SSH_OPTS[@]}" "$SSH_TARGET" \
        "curl --noproxy '*' -fsS --max-time 2 -H 'Host: ${DOMAIN}' http://${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}/api/health | grep -q 'chat-quant-api'" \
        >/dev/null 2>&1
}

find_local_proxy_pid() {
    lsof -ti "tcp:${LOCAL_PROXY_PORT}" 2>/dev/null | awk 'NR == 1 { print } END { exit 0 }'
}

find_local_caddy_pid() {
    local pid
    pid="$(find_local_proxy_pid)"
    if [[ -z "$pid" ]]; then
        return 0
    fi

    local command
    command="$(ps -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$command" == *"caddy"* ]]; then
        echo "$pid"
    fi
}

find_ssh_tunnel_pid() {
    ps -axo pid=,command= | awk \
        -v reverse="-R ${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}:${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}" \
        -v target="$SSH_TARGET" \
        'index($0, "ssh ") && index($0, reverse) && index($0, target) && !found { print $1; found = 1 } END { exit 0 }'
}

cleanup_remote_tunnel_listener() {
    ssh "${SSH_OPTS[@]}" "$SSH_TARGET" \
        "TUNNEL_REMOTE_HOST='${TUNNEL_REMOTE_HOST}' TUNNEL_REMOTE_PORT='${TUNNEL_REMOTE_PORT}' bash -s" <<'REMOTE_SCRIPT'
set -euo pipefail

if ! command -v ss >/dev/null 2>&1; then
    echo "[!] Cannot inspect remote tunnel listener because ss is unavailable." >&2
    exit 0
fi

listener_lines="$(
    ss -H -ltnp "sport = :${TUNNEL_REMOTE_PORT}" 2>/dev/null | awk \
        -v endpoint="${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}" \
        -v endpoint6="[${TUNNEL_REMOTE_HOST}]:${TUNNEL_REMOTE_PORT}" \
        '$4 == endpoint || $4 == endpoint6'
)"

if [[ -z "$listener_lines" ]]; then
    exit 0
fi

pids="$(printf '%s\n' "$listener_lines" | sed -n 's/.*"sshd",pid=\([0-9][0-9]*\).*/\1/p' | sort -u)"
if [[ -z "$pids" ]]; then
    echo "[!] Remote ${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT} is in use, but not by sshd:" >&2
    printf '%s\n' "$listener_lines" >&2
    exit 1
fi

for pid in $pids; do
    echo "==> Stopping stale remote SSH tunnel listener (pid ${pid})"
    kill "$pid" 2>/dev/null || true
done

for _ in {1..40}; do
    if ! ss -H -ltnp "sport = :${TUNNEL_REMOTE_PORT}" 2>/dev/null | awk \
        -v endpoint="${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}" \
        -v endpoint6="[${TUNNEL_REMOTE_HOST}]:${TUNNEL_REMOTE_PORT}" \
        '$4 == endpoint || $4 == endpoint6' | grep -q .; then
        exit 0
    fi
    sleep 0.25
done

for pid in $pids; do
    echo "==> Forcing stale remote SSH tunnel listener to stop (pid ${pid})"
    kill -9 "$pid" 2>/dev/null || true
done
REMOTE_SCRIPT
}

if [[ "$START_CHATQ" == "true" ]]; then
    echo "==> Checking local Chat-Quant dev services"
    (cd "$ROOT_DIR" && npm run dev:web-start)
else
    echo "==> Skipping Chat-Quant startup because START_CHATQ=${START_CHATQ}"
fi

if [[ "$BUILD_WEB" == "true" ]]; then
    echo "==> Building web frontend"
    (cd "$ROOT_DIR" && npm --prefix apps/web run build)
else
    echo "==> Skipping web build because BUILD_WEB=${BUILD_WEB}"
fi

if [[ "$START_CADDY" == "true" ]]; then
    if ! command -v caddy >/dev/null 2>&1; then
        echo "[x] Caddy is required for the local unified entrypoint." >&2
        echo "    Install on macOS with: brew install caddy" >&2
        exit 1
    fi

    cat > "$CADDY_FILE" <<EOF
:${LOCAL_PROXY_PORT} {
  root * ${WEB_DIST_DIR}
  encode gzip

  handle /api/* {
    reverse_proxy ${API_HOST}:${API_PORT}
  }

  handle {
    try_files {path} /index.html
    file_server
  }
}
EOF

    echo "==> Validating local Caddy config: ${CADDY_FILE}"
    caddy validate --config "$CADDY_FILE"

    if is_pid_running "$CADDY_PID_FILE"; then
        echo "==> Reloading local Caddy config (pid $(cat "$CADDY_PID_FILE"))"
        caddy reload --config "$CADDY_FILE" >>"$CADDY_LOG_FILE" 2>&1 || stop_pid_file "local Caddy" "$CADDY_PID_FILE"
    fi

    if is_pid_running "$CADDY_PID_FILE" && local_entrypoint_ready; then
        echo "==> Local Caddy already running (pid $(cat "$CADDY_PID_FILE"))"
    elif local_entrypoint_ready; then
        existing_proxy_pid="$(find_local_proxy_pid)"
        if [[ -n "$existing_proxy_pid" ]]; then
            echo "$existing_proxy_pid" > "$CADDY_PID_FILE"
            echo "==> Reloading local Caddy config (pid ${existing_proxy_pid})"
            caddy reload --config "$CADDY_FILE" >>"$CADDY_LOG_FILE" 2>&1 || true
            echo "==> Local entrypoint already responds on http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT} (pid ${existing_proxy_pid}); skipping Caddy startup"
        else
            echo "==> Local entrypoint already responds on http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}; skipping Caddy startup"
            rm -f "$CADDY_PID_FILE"
        fi
    else
        if is_pid_running "$CADDY_PID_FILE"; then
            stop_pid_file "local Caddy" "$CADDY_PID_FILE"
        fi

        if [[ -f "$CADDY_PID_FILE" ]]; then
            rm -f "$CADDY_PID_FILE"
        fi

        echo "==> Starting local Caddy on http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}"
        (
            cd "$ROOT_DIR"
            caddy start --config "$CADDY_FILE" >"$CADDY_LOG_FILE" 2>&1
        )
        new_caddy_pid="$(find_local_caddy_pid)"
        if [[ -n "$new_caddy_pid" ]]; then
            echo "$new_caddy_pid" > "$CADDY_PID_FILE"
        fi
    fi

    if local_entrypoint_ready; then
        echo "==> Local entrypoint is ready: http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}"
    else
        echo "==> Waiting for local entrypoint"
        local_attempts=$((LOCAL_HEALTH_TIMEOUT_SECONDS * 4))
        for ((attempt = 1; attempt <= local_attempts; attempt += 1)); do
            if local_entrypoint_ready; then
                echo "==> Local entrypoint is ready: http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}"
                break
            fi
            sleep 0.25
        done

        if ! local_entrypoint_ready; then
            echo "[x] Local entrypoint did not become ready. Recent Caddy log:" >&2
            tail -n 80 "$CADDY_LOG_FILE" >&2 || true
            echo "[x] Local entrypoint curl diagnostic:" >&2
            curl --noproxy '*' -v --max-time 3 -H "Host: ${DOMAIN}" "http://${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}/api/health" >&2 || true
            echo "[x] Direct API curl diagnostic:" >&2
            curl --noproxy '*' -v --max-time 3 "http://${API_HOST}:${API_PORT}/api/health" >&2 || true
            if is_pid_running "$CADDY_PID_FILE"; then
                stop_pid_file "local Caddy" "$CADDY_PID_FILE"
            fi
            exit 1
        fi
    fi
else
    echo "==> Skipping Caddy startup because START_CADDY=${START_CADDY}"
fi

echo "==> Checking SSH reverse tunnel"
if is_pid_running "$SSH_PID_FILE" && remote_entrypoint_ready; then
    echo "==> SSH reverse tunnel already running (pid $(cat "$SSH_PID_FILE"))"
elif remote_entrypoint_ready; then
    existing_ssh_pid="$(find_ssh_tunnel_pid)"
    if [[ -n "$existing_ssh_pid" ]]; then
        echo "$existing_ssh_pid" > "$SSH_PID_FILE"
        echo "==> SSH reverse tunnel already responds (pid ${existing_ssh_pid}); skipping SSH startup"
    else
        echo "==> Remote tunnel endpoint already responds on http://${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}; skipping SSH startup"
        rm -f "$SSH_PID_FILE"
    fi
else
    if is_pid_running "$SSH_PID_FILE"; then
        stop_pid_file "SSH reverse tunnel" "$SSH_PID_FILE"
    fi

    if [[ "$CLEAN_REMOTE_TUNNEL" == "true" ]]; then
        echo "==> Clearing stale remote SSH tunnel listeners"
        cleanup_remote_tunnel_listener
    fi

    rm -f "$SSH_PID_FILE"
    echo "==> Starting SSH reverse tunnel in background"
    echo "==> Remote ${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT} -> local ${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}"
    ssh "${SSH_OPTS[@]}" \
        -f \
        -N \
        -R "${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}:${LOCAL_PROXY_HOST}:${LOCAL_PROXY_PORT}" \
        "$SSH_TARGET" >>"$SSH_LOG_FILE" 2>&1

    new_ssh_pid="$(find_ssh_tunnel_pid)"
    if [[ -n "$new_ssh_pid" ]]; then
        echo "$new_ssh_pid" > "$SSH_PID_FILE"
    fi

    echo "==> Waiting for remote tunnel endpoint"
    remote_attempts=$((REMOTE_HEALTH_TIMEOUT_SECONDS * 4))
    for ((attempt = 1; attempt <= remote_attempts; attempt += 1)); do
        if remote_entrypoint_ready; then
            echo "==> SSH reverse tunnel is ready (pid $(cat "$SSH_PID_FILE"))"
            break
        fi
        sleep 0.25
    done

    if ! remote_entrypoint_ready; then
        echo "[x] SSH reverse tunnel did not become ready. Recent SSH log:" >&2
        tail -n 80 "$SSH_LOG_FILE" >&2 || true
        stop_pid_file "SSH reverse tunnel" "$SSH_PID_FILE"
        exit 1
    fi

    sleep 2
    if ! is_pid_running "$SSH_PID_FILE" || ! remote_entrypoint_ready; then
        echo "[x] SSH reverse tunnel became ready but did not stay alive. Recent SSH log:" >&2
        tail -n 80 "$SSH_LOG_FILE" >&2 || true
        stop_pid_file "SSH reverse tunnel" "$SSH_PID_FILE"
        exit 1
    fi
fi

echo "==> Public URL: https://${DOMAIN}"
if [[ "$CHECK_PUBLIC_URL" == "true" ]]; then
    if curl --noproxy '*' -fsS --max-time 10 "${PUBLIC_AUTH_CURL_ARGS[@]}" "https://${DOMAIN}/api/health" | grep -q 'chat-quant-api'; then
        echo "==> Public health check passed: https://${DOMAIN}/api/health"
    else
        echo "[!] Public health check failed: https://${DOMAIN}/api/health"
        echo "    Check Nginx config, HTTPS certificate, DNS, and Aliyun security group if friends cannot access it."
    fi
fi
echo "==> Logs:"
echo "    Caddy: ${CADDY_LOG_FILE}"
echo "    SSH:   ${SSH_LOG_FILE}"
echo "==> Stop all local public-access processes with:"
echo "    bash deploy/5_stop_local_tunnel.sh"
