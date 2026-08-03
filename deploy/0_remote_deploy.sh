#!/usr/bin/env bash
# =============================================================
# Chat-Quant remote bootstrap/deploy script
# Run locally. It logs in to the server with SSH key or password,
# pulls source code with git, then runs the server-side init and
# deploy scripts.
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

GITHUB_SSH_KEY_PATH="${GITHUB_SSH_KEY_PATH:-}"
SSH_TARGET="${SERVER_USER}@${SERVER_IP}"
SSH_OPTS=(
    -p "${SSH_PORT}"
    -o StrictHostKeyChecking=accept-new
    -o ServerAliveInterval=30
)

if [[ -n "${SSH_KEY_PATH:-}" ]]; then
    if [[ ! -f "$SSH_KEY_PATH" ]]; then
        echo "[x] Missing SSH key file: ${SSH_KEY_PATH}" >&2
        exit 1
    fi
    SSH_OPTS+=(-i "$SSH_KEY_PATH")
else
    if [[ ! -f "$PASSWORD_FILE" ]]; then
        echo "[x] Missing password file: ${PASSWORD_FILE}" >&2
        echo "    Create it with the server login password on the first line, or set SSH_KEY_PATH in ${CONFIG_FILE}." >&2
        exit 1
    fi

    if grep -q '^CHANGE_ME$' "$PASSWORD_FILE"; then
        echo "[x] Please replace CHANGE_ME in ${PASSWORD_FILE} with the server password." >&2
        exit 1
    fi

    if ! command -v sshpass >/dev/null 2>&1 && ! command -v expect >/dev/null 2>&1; then
        echo "[x] sshpass or expect is required for password login." >&2
        echo "    macOS usually includes expect at /usr/bin/expect." >&2
        echo "    macOS sshpass fallback: brew install hudochenkov/sshpass/sshpass" >&2
        echo "    Linux: use your package manager, for example apt/dnf/yum install sshpass or expect" >&2
        exit 1
    fi
fi

echo "==> Connecting to ${SSH_TARGET}:${SSH_PORT}"
echo "==> Deploying ${REPO_URL} (${REPO_BRANCH}) to ${APP_DIR}"

REMOTE_PAYLOAD="$(mktemp)"
trap 'rm -f "$REMOTE_PAYLOAD"' EXIT

cat > "$REMOTE_PAYLOAD" <<'REMOTE_SCRIPT'
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

if [[ -n "${GITHUB_SSH_KEY_PATH:-}" ]]; then
    export GIT_SSH_COMMAND="ssh -i ${GITHUB_SSH_KEY_PATH} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
fi

mkdir -p "$(dirname "$APP_DIR")"

if [[ -d "${APP_DIR}/.git" ]]; then
    echo "==> Updating existing repository"
    git config --global --add safe.directory "$APP_DIR" || true
    (
        cd "$APP_DIR"
        GIT_FETCH=(git fetch origin "$REPO_BRANCH")
        if command -v timeout >/dev/null 2>&1; then
            GIT_FETCH=(timeout 30 git fetch origin "$REPO_BRANCH")
        fi

        if "${GIT_FETCH[@]}"; then
            git checkout "$REPO_BRANCH"
            git merge --ff-only FETCH_HEAD
        elif [[ "$(git rev-parse --abbrev-ref HEAD)" == "$REPO_BRANCH" ]]; then
            echo "[!] Git fetch failed; continuing with existing ${REPO_BRANCH} checkout at $(git rev-parse HEAD)." >&2
        else
            echo "[x] Git fetch failed and current checkout is not ${REPO_BRANCH}." >&2
            exit 1
        fi
    )
elif [[ -e "$APP_DIR" && -n "$(find "$APP_DIR" -mindepth 1 -maxdepth 1 2>/dev/null)" ]]; then
    echo "[x] ${APP_DIR} exists and is not an empty git checkout." >&2
    exit 1
else
    echo "==> Cloning repository"
    rm -rf "$APP_DIR"
    git clone --branch "$REPO_BRANCH" "$REPO_URL" "$APP_DIR"
fi

export APP_DIR APP_USER SERVICE_NAME DOMAIN SSL_EMAIL

INIT_SCRIPT="${APP_DIR}/deploy/1_init_server.sh"
if [[ -n "${DEPLOY_INIT_B64:-}" ]]; then
    INIT_SCRIPT="$(mktemp)"
    printf %s "$DEPLOY_INIT_B64" | base64 -d > "$INIT_SCRIPT"
    chmod +x "$INIT_SCRIPT"
fi

DEPLOY_SCRIPT="${APP_DIR}/deploy/2_deploy.sh"
if [[ -n "${DEPLOY_SCRIPT_B64:-}" ]]; then
    DEPLOY_SCRIPT="$(mktemp)"
    printf %s "$DEPLOY_SCRIPT_B64" | base64 -d > "$DEPLOY_SCRIPT"
    chmod +x "$DEPLOY_SCRIPT"
fi

bash "$INIT_SCRIPT"
bash "$DEPLOY_SCRIPT"
REMOTE_SCRIPT

REMOTE_SCRIPT_B64="$(base64 < "$REMOTE_PAYLOAD" | tr -d '\n')"
DEPLOY_INIT_B64="$(base64 < "${SCRIPT_DIR}/1_init_server.sh" | tr -d '\n')"
DEPLOY_SCRIPT_B64="$(base64 < "${SCRIPT_DIR}/2_deploy.sh" | tr -d '\n')"
REMOTE_COMMAND="APP_DIR='${APP_DIR}' APP_USER='${APP_USER}' SERVICE_NAME='${SERVICE_NAME}' DOMAIN='${DOMAIN}' SSL_EMAIL='${SSL_EMAIL}' REPO_URL='${REPO_URL}' REPO_BRANCH='${REPO_BRANCH}' GITHUB_SSH_KEY_PATH='${GITHUB_SSH_KEY_PATH}' DEPLOY_INIT_B64='${DEPLOY_INIT_B64}' DEPLOY_SCRIPT_B64='${DEPLOY_SCRIPT_B64}' bash -lc 'printf %s ${REMOTE_SCRIPT_B64} | base64 -d | bash -s'"

if [[ -n "${SSH_KEY_PATH:-}" ]]; then
    ssh "${SSH_OPTS[@]}" "$SSH_TARGET" "$REMOTE_COMMAND"
elif command -v sshpass >/dev/null 2>&1; then
    sshpass -f "$PASSWORD_FILE" ssh "${SSH_OPTS[@]}" "$SSH_TARGET" "$REMOTE_COMMAND"
else
    EXPECT_SCRIPT="$(mktemp)"
    cat > "$EXPECT_SCRIPT" <<'EXPECT_SCRIPT_CONTENT'
        set timeout -1
        set password_file $env(EXPECT_PASSWORD_FILE)
        set fp [open $password_file r]
        set password [string trimright [gets $fp] "\r\n"]
        close $fp

        spawn {*}$argv
        expect {
            -re "(?i)are you sure you want to continue connecting" {
                send "yes\r"
                exp_continue
            }
            -re "(?i)password:" {
                send -- "$password\r"
                exp_continue
            }
            eof
        }

        set wait_result [wait]
        exit [lindex $wait_result 3]
EXPECT_SCRIPT_CONTENT
    EXPECT_PASSWORD_FILE="$PASSWORD_FILE" expect "$EXPECT_SCRIPT" ssh "${SSH_OPTS[@]}" "$SSH_TARGET" "$REMOTE_COMMAND"
    rm -f "$EXPECT_SCRIPT"
fi

echo "==> Done. Visit https://${DOMAIN}"
