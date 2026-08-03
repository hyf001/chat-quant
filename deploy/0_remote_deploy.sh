#!/usr/bin/env bash
# =============================================================
# Chat-Quant remote bootstrap/deploy script
# Run locally. It logs in to the server with the password from
# deploy/server.password, pulls source code with git, then runs
# the server-side init and deploy scripts.
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/server.env"
PASSWORD_FILE="${SCRIPT_DIR}/server.password"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[x] Missing config file: ${CONFIG_FILE}" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

if [[ ! -f "$PASSWORD_FILE" ]]; then
    echo "[x] Missing password file: ${PASSWORD_FILE}" >&2
    echo "    Create it with the server login password on the first line." >&2
    exit 1
fi

if grep -q '^CHANGE_ME$' "$PASSWORD_FILE"; then
    echo "[x] Please replace CHANGE_ME in ${PASSWORD_FILE} with the server password." >&2
    exit 1
fi

if ! command -v sshpass >/dev/null 2>&1; then
    echo "[x] sshpass is required for password login." >&2
    echo "    macOS: brew install hudochenkov/sshpass/sshpass" >&2
    echo "    Linux: use your package manager, for example apt/dnf/yum install sshpass" >&2
    exit 1
fi

SSH_TARGET="${SERVER_USER}@${SERVER_IP}"
SSH_OPTS=(
    -p "${SSH_PORT}"
    -o StrictHostKeyChecking=accept-new
    -o ServerAliveInterval=30
)

echo "==> Connecting to ${SSH_TARGET}:${SSH_PORT}"
echo "==> Deploying ${REPO_URL} (${REPO_BRANCH}) to ${APP_DIR}"

sshpass -f "$PASSWORD_FILE" ssh "${SSH_OPTS[@]}" "$SSH_TARGET" \
    "APP_DIR='${APP_DIR}' APP_USER='${APP_USER}' SERVICE_NAME='${SERVICE_NAME}' DOMAIN='${DOMAIN}' SSL_EMAIL='${SSL_EMAIL}' REPO_URL='${REPO_URL}' REPO_BRANCH='${REPO_BRANCH}' bash -s" <<'REMOTE_SCRIPT'
set -euo pipefail

install_git() {
    if command -v git >/dev/null 2>&1; then
        return
    fi

    if command -v dnf >/dev/null 2>&1; then
        dnf install -y git
    elif command -v yum >/dev/null 2>&1; then
        yum install -y git
    elif command -v apt-get >/dev/null 2>&1; then
        apt-get update
        apt-get install -y git ca-certificates
    else
        echo "[x] Unsupported package manager. Please install git manually." >&2
        exit 1
    fi
}

install_git

mkdir -p "$(dirname "$APP_DIR")"

if [[ -d "${APP_DIR}/.git" ]]; then
    echo "==> Updating existing repository"
    git -C "$APP_DIR" fetch origin "$REPO_BRANCH"
    git -C "$APP_DIR" checkout "$REPO_BRANCH"
    git -C "$APP_DIR" pull --ff-only origin "$REPO_BRANCH"
elif [[ -e "$APP_DIR" && -n "$(find "$APP_DIR" -mindepth 1 -maxdepth 1 2>/dev/null)" ]]; then
    echo "[x] ${APP_DIR} exists and is not an empty git checkout." >&2
    exit 1
else
    echo "==> Cloning repository"
    rm -rf "$APP_DIR"
    git clone --branch "$REPO_BRANCH" "$REPO_URL" "$APP_DIR"
fi

export APP_DIR APP_USER SERVICE_NAME DOMAIN SSL_EMAIL
bash "${APP_DIR}/deploy/1_init_server.sh"
bash "${APP_DIR}/deploy/2_deploy.sh"
REMOTE_SCRIPT

echo "==> Done. Visit https://${DOMAIN}"

