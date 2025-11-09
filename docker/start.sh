#!/bin/bash

# Claudable 服务启动脚本
# 用于在K8s容器中启动前端和后端服务

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志目录
LOG_DIR="/var/log/claudable"
BACKEND_LOG="${LOG_DIR}/backend.log"
FRONTEND_LOG="${LOG_DIR}/frontend.log"

# 数据目录
DATA_DIR="/data/claudable/data"

# 确保数据目录存在
if [ ! -d "${DATA_DIR}" ]; then
    echo "创建数据目录: ${DATA_DIR}"
    mkdir -p "${DATA_DIR}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Claudable Service Startup${NC}"
echo -e "${GREEN}========================================${NC}"

# 打印环境信息
echo -e "${YELLOW}Environment Information:${NC}"
echo "  Python: $(python --version)"
echo "  Node.js: $(node --version)"
echo "  NPM: $(npm --version)"
echo "  Working Directory: $(pwd)"
echo "  API Port: ${API_PORT:-8000}"
echo "  Web Port: ${WEB_PORT:-3000}"
echo ""

cp /app/scripts/readiness.sh /opt

rm -rf /usr/local/python/lib/python3.12/site-packages/claude_agent_sdk/_internal/transport/subprocess_cli.py
cp /app/scripts/python/subprocess_cli.py /usr/local/python/lib/python3.12/site-packages/claude_agent_sdk/_internal/transport

# 数据目录用户改为cbas
chown -R cbas:cbas ${DATA_DIR}

# 使用cbas用户执行后续脚本
exec su cbas -c "bash /app/start-services.sh"