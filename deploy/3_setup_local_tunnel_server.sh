#!/usr/bin/env bash
# =============================================================
# Configure the Aliyun server as a public entrypoint for a local
# Chat-Quant instance connected through an SSH reverse tunnel.
#
# Run locally from the repository root:
#   bash deploy/3_setup_local_tunnel_server.sh
#
# It reuses deploy/server.config and writes the remote Nginx file:
#   /etc/nginx/conf.d/${SERVICE_NAME}.conf
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/server.config"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[x] Missing config file: ${CONFIG_FILE}" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

TUNNEL_REMOTE_HOST="${TUNNEL_REMOTE_HOST:-127.0.0.1}"
TUNNEL_REMOTE_PORT="${TUNNEL_REMOTE_PORT:-18080}"
ENABLE_CERTBOT="${ENABLE_CERTBOT:-true}"
PUBLIC_AUTH_ENABLED="${PUBLIC_AUTH_ENABLED:-false}"
PUBLIC_AUTH_USER="${PUBLIC_AUTH_USER:-friend}"
PUBLIC_AUTH_PASSWORD_FILE="${PUBLIC_AUTH_PASSWORD_FILE:-${SCRIPT_DIR}/public-auth.password}"
PUBLIC_AUTH_PASSWORD="${PUBLIC_AUTH_PASSWORD:-}"

if [[ -f "$PUBLIC_AUTH_PASSWORD_FILE" ]]; then
    PUBLIC_AUTH_PASSWORD="$(head -n 1 "$PUBLIC_AUTH_PASSWORD_FILE")"
fi

if [[ "$PUBLIC_AUTH_ENABLED" == "true" ]]; then
    if [[ ! "$PUBLIC_AUTH_USER" =~ ^[A-Za-z0-9._-]+$ ]]; then
        echo "[x] PUBLIC_AUTH_USER may only contain letters, numbers, dot, underscore, and dash." >&2
        exit 1
    fi

    if [[ -z "$PUBLIC_AUTH_PASSWORD" ]]; then
        echo "[x] PUBLIC_AUTH_ENABLED=true but no password was provided." >&2
        echo "    Put the password on the first line of ${PUBLIC_AUTH_PASSWORD_FILE}, or set PUBLIC_AUTH_PASSWORD." >&2
        exit 1
    fi
fi

PUBLIC_AUTH_PASSWORD_B64="$(printf '%s' "$PUBLIC_AUTH_PASSWORD" | base64 | tr -d '\n')"

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
fi

echo "==> Configuring local-tunnel Nginx on ${SSH_TARGET}:${SSH_PORT}"
echo "==> Domain: ${DOMAIN}"
echo "==> Remote tunnel upstream: http://${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}"
if [[ "$PUBLIC_AUTH_ENABLED" == "true" ]]; then
    echo "==> Public Basic Auth: enabled for user ${PUBLIC_AUTH_USER}"
else
    echo "==> Public Basic Auth: disabled"
fi

ssh "${SSH_OPTS[@]}" "$SSH_TARGET" \
    "SERVICE_NAME='${SERVICE_NAME}' DOMAIN='${DOMAIN}' SSL_EMAIL='${SSL_EMAIL}' TUNNEL_REMOTE_HOST='${TUNNEL_REMOTE_HOST}' TUNNEL_REMOTE_PORT='${TUNNEL_REMOTE_PORT}' ENABLE_CERTBOT='${ENABLE_CERTBOT}' PUBLIC_AUTH_ENABLED='${PUBLIC_AUTH_ENABLED}' PUBLIC_AUTH_USER='${PUBLIC_AUTH_USER}' PUBLIC_AUTH_PASSWORD_B64='${PUBLIC_AUTH_PASSWORD_B64}' bash -s" <<'REMOTE_SCRIPT'
set -euo pipefail

[[ $EUID -ne 0 ]] && { echo "[x] Please login as root or a sudo-capable user and run through sudo." >&2; exit 1; }

NGINX_CONF="/etc/nginx/conf.d/${SERVICE_NAME}.conf"
CERT_PATH="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/${DOMAIN}/privkey.pem"
UPSTREAM="http://${TUNNEL_REMOTE_HOST}:${TUNNEL_REMOTE_PORT}"
AUTH_FILE="/etc/nginx/${SERVICE_NAME}.htpasswd"

if ! command -v nginx >/dev/null 2>&1; then
    echo "[x] Nginx is not installed on this server." >&2
    exit 1
fi

mkdir -p /etc/nginx/conf.d /var/www/certbot

setup_public_auth() {
    if [[ "$PUBLIC_AUTH_ENABLED" != "true" ]]; then
        return 0
    fi

    if [[ -z "${PUBLIC_AUTH_PASSWORD_B64:-}" ]]; then
        echo "[x] PUBLIC_AUTH_ENABLED=true but PUBLIC_AUTH_PASSWORD_B64 is empty." >&2
        exit 1
    fi

    if ! command -v openssl >/dev/null 2>&1; then
        echo "[x] openssl is required to generate the Nginx Basic Auth password hash." >&2
        exit 1
    fi

    auth_password="$(printf '%s' "$PUBLIC_AUTH_PASSWORD_B64" | base64 -d)"
    auth_hash="$(printf '%s' "$auth_password" | openssl passwd -apr1 -stdin)"
    printf '%s:%s\n' "$PUBLIC_AUTH_USER" "$auth_hash" > "$AUTH_FILE"
    chmod 644 "$AUTH_FILE"
    echo "==> Wrote public Basic Auth file: ${AUTH_FILE}"
}

render_auth_basic() {
    if [[ "$PUBLIC_AUTH_ENABLED" == "true" ]]; then
        cat <<EOF
        auth_basic "Chat-Quant";
        auth_basic_user_file ${AUTH_FILE};
EOF
    fi
}

if [[ -f "$NGINX_CONF" ]]; then
    BACKUP="${NGINX_CONF}.bak.$(date +%Y%m%d-%H%M%S)"
    cp "$NGINX_CONF" "$BACKUP"
    echo "==> Backed up existing Nginx config: ${BACKUP}"
fi

setup_public_auth

write_http_proxy_conf() {
    cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
$(render_auth_basic)
        proxy_pass ${UPSTREAM};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        client_max_body_size 50m;
    }
}
EOF
}

write_https_proxy_conf() {
    cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    ssl_certificate ${CERT_PATH};
    ssl_certificate_key ${KEY_PATH};
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;

    location / {
$(render_auth_basic)
        proxy_pass ${UPSTREAM};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        client_max_body_size 50m;
    }
}
EOF
}

if [[ -f "$CERT_PATH" && -f "$KEY_PATH" ]]; then
    echo "==> Existing certificate found. Writing HTTPS tunnel config."
    write_https_proxy_conf
else
    echo "==> No certificate found. Writing HTTP tunnel config first."
    write_http_proxy_conf
fi

nginx -t
systemctl reload nginx || systemctl restart nginx

if [[ "$ENABLE_CERTBOT" == "true" && ! -f "$CERT_PATH" ]]; then
    if command -v certbot >/dev/null 2>&1; then
        CERTBOT_ARGS=(certonly --webroot -w /var/www/certbot -d "$DOMAIN" --non-interactive --agree-tos)
        if [[ -n "${SSL_EMAIL:-}" ]]; then
            CERTBOT_ARGS+=(-m "$SSL_EMAIL")
        else
            CERTBOT_ARGS+=(--register-unsafely-without-email)
        fi

        echo "==> Requesting Let's Encrypt certificate for ${DOMAIN}"
        certbot "${CERTBOT_ARGS[@]}"
        echo "==> Certificate issued. Writing HTTPS tunnel config."
        write_https_proxy_conf
        nginx -t
        systemctl reload nginx || systemctl restart nginx
    else
        echo "[!] certbot is not installed. HTTP tunnel config is active."
    fi
fi

echo "==> Local-tunnel Nginx config is active: ${NGINX_CONF}"
echo "==> Public URL: https://${DOMAIN}"
echo "==> If the SSH tunnel is not running yet, Nginx may return 502."
REMOTE_SCRIPT

echo "==> Done. Start the local tunnel with:"
echo "    bash deploy/4_start_local_tunnel.sh"
