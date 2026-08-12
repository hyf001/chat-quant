#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dev-common.sh"

stop_service "web" "$PID_DIR/web.pid"
stop_service "web api" "$PID_DIR/web-api.pid"
stop_port "web" "$WEB_PORT"
stop_port "web api" "$API_PORT"
