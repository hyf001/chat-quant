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
DATA_DIR="/data/claudable"

# 检查Python依赖
echo -e "${YELLOW}Checking Python dependencies...${NC}"
if python -c "import fastapi, uvicorn, sqlalchemy" 2>/dev/null; then
    echo -e "${GREEN}✓ Python dependencies OK${NC}"
else
    echo -e "${RED}✗ Python dependencies missing${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Starting Services${NC}"
echo -e "${GREEN}========================================${NC}"

# 导出智能体初始数据
echo -e "${YELLOW}Exporting Agent Initial Data...${NC}"
# 确保脚本有执行权限
chmod +x /app/scripts/export-agent-initial-data.sh

# 导出数据分析智能体数据
EXPORT_LOG="${LOG_DIR}/export.log"
nohup /app/scripts/export-agent-initial-data.sh --agent-type data_analysis \
    > "${EXPORT_LOG}" 2>&1 &
EXPORT_PID=$!
echo -e "${GREEN}✓ Data Analysis export started (PID: ${EXPORT_PID})${NC}"
echo "  Log: ${EXPORT_LOG}"

# 导出财务数据分析智能体数据
FIN_EXPORT_LOG="${LOG_DIR}/export-fin.log"
nohup /app/scripts/export-agent-initial-data.sh --agent-type fin_data_analysis \
    > "${FIN_EXPORT_LOG}" 2>&1 &
FIN_EXPORT_PID=$!
echo -e "${GREEN}✓ Financial Analysis export started (PID: ${FIN_EXPORT_PID})${NC}"
echo "  Log: ${FIN_EXPORT_LOG}"
echo ""

# 启动前端服务
echo -e "${YELLOW}Starting Frontend Service...${NC}"
cd /app/apps/web

# 使用nohup启动前端，输出到日志文件
npm run build
nohup npm start -- --port ${WEB_PORT:-3000} \
    > "${FRONTEND_LOG}" 2>&1 &

FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: ${FRONTEND_PID})${NC}"
echo "  Log: ${FRONTEND_LOG}"
echo ""

# 等待前端启动
sleep 5

# 检查前端是否正常运行
if ps -p ${FRONTEND_PID} > /dev/null; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend failed to start${NC}"
    echo "Frontend logs:"
    tail -20 "${FRONTEND_LOG}"
    exit 1
fi

# 等待后端启动
sleep 3

# 启动后端服务
echo -e "${YELLOW}Starting Backend Service...${NC}"
cd /app/apps/api

# 使用nohup启动后端，输出到日志文件
python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${API_PORT:-8080} \
    --log-level info 

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  All Services Started Successfully${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Service Status:"
echo "  Backend:  http://0.0.0.0:${API_PORT:-8000} (PID: ${BACKEND_PID})"
echo "  Frontend: http://0.0.0.0:${WEB_PORT:-3000} (PID: ${FRONTEND_PID})"
echo ""
echo "Logs:"
echo "  Backend:  ${BACKEND_LOG}"
echo "  Frontend: ${FRONTEND_LOG}"
echo "  Export (Data Analysis):   ${EXPORT_LOG}"
echo "  Export (Financial):       ${FIN_EXPORT_LOG}"
echo ""
echo -e "${YELLOW}Container is ready!${NC}"
echo ""
