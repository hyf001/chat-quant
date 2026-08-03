#!/usr/bin/env bash
# =============================================================
# Chat-Quant server initialization script
# Run as root on the server. Installs Python, Node.js, Nginx,
# Certbot, build tools, and creates the app user/directories.
# =============================================================

set -euo pipefail

APP_USER="${APP_USER:-chatquant}"
APP_DIR="${APP_DIR:-/opt/chat-quant}"
NODE_VERSION="${NODE_VERSION:-20}"
PYTHON_VERSION="${PYTHON_VERSION:-3.12.9}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
info() { echo -e "${BLUE}[→]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

[[ $EUID -ne 0 ]] && err "Please run as root."

echo "=============================================="
echo "      Chat-Quant server initialization"
echo "=============================================="

PKG_MANAGER=""
if command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
elif command -v yum >/dev/null 2>&1; then
    PKG_MANAGER="yum"
elif command -v apt-get >/dev/null 2>&1; then
    PKG_MANAGER="apt"
else
    err "Unsupported package manager. Expected dnf, yum, or apt-get."
fi

install_base_packages() {
    info "Installing base build tools"
    if [[ "$PKG_MANAGER" == "apt" ]]; then
        apt-get update
        DEBIAN_FRONTEND=noninteractive apt-get install -y \
            ca-certificates curl wget git vim tar xz-utils \
            build-essential make pkg-config \
            libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
            libsqlite3-dev libffi-dev liblzma-dev
    else
        "$PKG_MANAGER" install -y epel-release || true
        "$PKG_MANAGER" install -y \
            ca-certificates curl wget git vim tar xz \
            gcc gcc-c++ make pkgconfig \
            openssl-devel bzip2-devel libffi-devel \
            zlib-devel readline-devel sqlite-devel xz-devel
    fi
    log "Base tools installed"
}

install_python() {
    info "Installing Python ${PYTHON_VERSION}"
    if command -v python3.12 >/dev/null 2>&1; then
        warn "Python 3.12 already installed: $(python3.12 --version)"
        return
    fi

    local src_dir="/usr/local/src/Python-${PYTHON_VERSION}"
    cd /usr/local/src
    if [[ ! -d "$src_dir" ]]; then
        wget -c "https://mirrors.aliyun.com/python/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
            || wget -c "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"
        tar -xzf "Python-${PYTHON_VERSION}.tgz"
    fi

    cd "$src_dir"
    ./configure \
        --prefix=/usr/local \
        --enable-optimizations \
        --enable-shared \
        LDFLAGS="-Wl,-rpath /usr/local/lib"
    make -j"$(nproc)"
    make altinstall
    ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3
    ln -sf /usr/local/bin/pip3.12 /usr/local/bin/pip3
    log "Python installed: $(python3.12 --version)"
}

install_node() {
    info "Installing Node.js ${NODE_VERSION}"
    if command -v node >/dev/null 2>&1; then
        warn "Node.js already installed: $(node --version)"
        return
    fi

    if [[ "$PKG_MANAGER" == "apt" ]]; then
        curl -fsSL "https://deb.nodesource.com/setup_${NODE_VERSION}.x" | bash -
        DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
    else
        curl -fsSL "https://rpm.nodesource.com/setup_${NODE_VERSION}.x" | bash -
        "$PKG_MANAGER" install -y nodejs
    fi
    log "Node.js installed: $(node --version)"
}

install_nginx_certbot() {
    info "Installing Nginx and Certbot"
    if [[ "$PKG_MANAGER" == "apt" ]]; then
        DEBIAN_FRONTEND=noninteractive apt-get install -y nginx certbot
    else
        "$PKG_MANAGER" install -y nginx certbot
    fi

    systemctl enable nginx
    log "Nginx and Certbot installed"
}

create_app_user() {
    info "Creating app user and directories"
    if ! id "$APP_USER" >/dev/null 2>&1; then
        useradd -r -s /bin/bash -d "$APP_DIR" "$APP_USER"
        log "Created user: ${APP_USER}"
    else
        warn "User already exists: ${APP_USER}"
    fi

    mkdir -p "$APP_DIR" "$APP_DIR/data" "$APP_DIR/logs" /var/www/certbot
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"

    if command -v setsebool >/dev/null 2>&1; then
        setsebool -P httpd_can_network_connect 1 || true
    fi

    if command -v firewall-cmd >/dev/null 2>&1 && systemctl is-active --quiet firewalld; then
        firewall-cmd --permanent --add-service=http || true
        firewall-cmd --permanent --add-service=https || true
        firewall-cmd --reload || true
    fi
    log "App directories ready: ${APP_DIR}"
}

install_base_packages
install_python
install_node
install_nginx_certbot
create_app_user

echo "=============================================="
echo "  Server initialization complete"
echo "=============================================="

