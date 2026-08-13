#!/usr/bin/env bash
# =============================================================
# Chat-Quant app deployment/update script
# Run as root on the server from an existing git checkout.
# =============================================================

set -euo pipefail

APP_USER="${APP_USER:-chatquant}"
APP_DIR="${APP_DIR:-/opt/chat-quant}"
SERVICE_NAME="${SERVICE_NAME:-chat-quant}"
DOMAIN="${DOMAIN:-chatq.nanbende.com}"
SSL_EMAIL="${SSL_EMAIL:-}"
NGINX_CONF="/etc/nginx/conf.d/${SERVICE_NAME}.conf"
VENV_DIR="${APP_DIR}/.venv"
CONFIG_FILE="${APP_DIR}/config.json"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
info() { echo -e "${BLUE}[→]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

[[ $EUID -ne 0 ]] && err "Please run as root."
[[ ! -d "$APP_DIR/.git" ]] && err "${APP_DIR} is not a git checkout."

echo "=============================================="
echo "      Chat-Quant app deployment"
echo "=============================================="

cd "$APP_DIR"

if [[ ! -f "$CONFIG_FILE" ]]; then
    cat > "$CONFIG_FILE" <<EOF
{
  "database_path": "data/chat-quant.db",
  "api_host": "127.0.0.1",
  "api_port": 12345,
  "web_host": "127.0.0.1",
  "web_port": 12346
}
EOF
    log "Created runtime config: ${CONFIG_FILE}"
fi

read_config() {
    python3 "$APP_DIR/scripts/read-runtime-config.py" "$1"
}

API_HOST="$(read_config api_host)"
API_PORT="$(read_config api_port)"
WEB_HOST="$(read_config web_host)"
WEB_PORT="$(read_config web_port)"
log "Runtime config ready: ${CONFIG_FILE}"

info "Installing Python dependencies"
if [[ ! -d "$VENV_DIR" ]]; then
    python3.12 -m venv "$VENV_DIR"
    log "Created virtualenv: ${VENV_DIR}"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip wheel -i https://mirrors.aliyun.com/pypi/simple/
python -m pip install -e "$APP_DIR/apps/api" gunicorn -i https://mirrors.aliyun.com/pypi/simple/
deactivate
log "Python dependencies installed"

info "Building web frontend"
npm config set registry https://registry.npmmirror.com
if [[ -f "$APP_DIR/apps/web/package-lock.json" ]]; then
    npm --prefix "$APP_DIR/apps/web" ci
else
    npm --prefix "$APP_DIR/apps/web" install
fi
npm --prefix "$APP_DIR/apps/web" run build
log "Frontend built: ${APP_DIR}/apps/web/dist"

info "Configuring systemd service"
mkdir -p "$APP_DIR/logs" "$APP_DIR/data"
chown -R "$APP_USER:$APP_USER" "$APP_DIR/logs" "$APP_DIR/data"

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Chat-Quant FastAPI Backend
After=network.target

[Service]
Type=exec
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${VENV_DIR}/bin/gunicorn app.main:app \\
    --chdir ${APP_DIR}/apps/api \\
    --workers 2 \\
    --worker-class uvicorn.workers.UvicornWorker \\
    --bind ${API_HOST}:${API_PORT} \\
    --log-level info \\
    --access-logfile ${APP_DIR}/logs/access.log \\
    --error-logfile ${APP_DIR}/logs/error.log \\
    --timeout 300
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    log "Backend service started"
else
    journalctl -u "$SERVICE_NAME" -n 80 --no-pager || true
    err "Backend service failed to start."
fi

write_http_nginx_conf() {
    cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 302 https://\$host\$request_uri;
    }
}
EOF
}

write_https_nginx_conf() {
    cp "$APP_DIR/deploy/nginx.conf" "$NGINX_CONF"
    sed -i "s/YOUR_DOMAIN/${DOMAIN}/g" "$NGINX_CONF"
    sed -i "s|APP_DIR|${APP_DIR}|g" "$NGINX_CONF"
    sed -i "s|API_UPSTREAM|http://${API_HOST}:${API_PORT}|g" "$NGINX_CONF"
}

info "Configuring Nginx and HTTPS"
mkdir -p /var/www/certbot

CERT_PATH="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
if [[ ! -f "$CERT_PATH" ]]; then
    write_http_nginx_conf
    nginx -t
    systemctl restart nginx

    CERTBOT_ARGS=(certonly --webroot -w /var/www/certbot -d "$DOMAIN" --non-interactive --agree-tos)
    if [[ -n "$SSL_EMAIL" ]]; then
        CERTBOT_ARGS+=(-m "$SSL_EMAIL")
    else
        CERTBOT_ARGS+=(--register-unsafely-without-email)
    fi

    warn "Requesting Let's Encrypt certificate for ${DOMAIN}."
    warn "DNS A record must point to this server and ports 80/443 must be open."
    certbot "${CERTBOT_ARGS[@]}"
    log "SSL certificate issued"
fi

write_https_nginx_conf
nginx -t
systemctl reload nginx || systemctl restart nginx
log "Nginx HTTPS config active"

if command -v crontab >/dev/null 2>&1; then
    CRON_TMP="$(mktemp)"
    crontab -l 2>/dev/null | grep -v 'certbot renew --quiet' > "$CRON_TMP" || true
    echo "0 2 * * * certbot renew --quiet && systemctl reload nginx" >> "$CRON_TMP"
    crontab "$CRON_TMP"
    rm -f "$CRON_TMP"
    log "Certbot auto-renew cron installed"
fi

chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "=============================================="
echo "  Deployment complete"
echo "  URL: https://${DOMAIN}"
echo ""
echo "  Logs:    journalctl -u ${SERVICE_NAME} -f"
echo "  Restart: systemctl restart ${SERVICE_NAME}"
echo "  Nginx:   systemctl reload nginx"
echo "=============================================="
