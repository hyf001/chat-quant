#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dev-common.sh"

API_PID_FILE="$PID_DIR/web-api.pid"
WEB_PID_FILE="$PID_DIR/web.pid"

clear_stale_service_port "web api" "$API_PID_FILE" "$API_PORT"
clear_stale_service_port "web" "$WEB_PID_FILE" "$WEB_PORT"

start_service \
  "web api" \
  "$API_PID_FILE" \
  "$LOG_DIR/web-api.log" \
  "http://$API_HOST:$API_PORT/api/health" \
  60 \
  uv run --project apps/api uvicorn app.main:app --reload --reload-dir apps/api/app --app-dir apps/api --host "$API_HOST" --port "$API_PORT" --no-access-log

start_service \
  "web" \
  "$WEB_PID_FILE" \
  "$LOG_DIR/web.log" \
  "http://$WEB_HOST:$WEB_PORT" \
  30 \
  npm --prefix apps/web run dev -- --host "$WEB_HOST" --port "$WEB_PORT"

echo
echo "Web dev services are running:"
echo "  API: http://$API_HOST:$API_PORT/api/health"
echo "  Web: http://$WEB_HOST:$WEB_PORT"
echo
echo "Logs:"
echo "  tail -f $LOG_DIR/web-api.log"
echo "  tail -f $LOG_DIR/web.log"
echo
echo "Stop with: npm run dev:web-stop"
