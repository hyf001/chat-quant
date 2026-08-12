#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dev-common.sh"

stop_service "desktop" "$PID_DIR/desktop.pid"
stop_port "desktop api" "$DESKTOP_API_PORT"
