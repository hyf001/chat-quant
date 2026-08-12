#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dev-common.sh"

DESKTOP_PID_FILE="$PID_DIR/desktop.pid"

start_service \
  "desktop" \
  "$DESKTOP_PID_FILE" \
  "$LOG_DIR/desktop.log" \
  "http://$DESKTOP_API_HOST:$DESKTOP_API_PORT/api/health" \
  120 \
  npm --prefix apps/desktop run dev

echo
echo "Desktop dev app is running:"
echo "  Desktop API: http://$DESKTOP_API_HOST:$DESKTOP_API_PORT/api/health"
echo
echo "Logs:"
echo "  tail -f $LOG_DIR/desktop.log"
echo
echo "Stop with: npm run dev:desktop-stop"
