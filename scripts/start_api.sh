#!/bin/bash

###############################################################################
# 后端服务启动脚本
# 用途：在虚拟环境中启动 FastAPI 后端服务
# 使用：./scripts/start_api.sh
###############################################################################

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}启动后端服务${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# 项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"
VENV_DIR="$API_DIR/.venv"

# 检查虚拟环境
if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${RED}[ERROR]${NC} 虚拟环境不存在: $VENV_DIR"
    echo -e "${BLUE}[INFO]${NC} 请先运行: ./scripts/setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
echo -e "${BLUE}[INFO]${NC} 激活虚拟环境..."
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓${NC} 虚拟环境已激活"

# 显示 Python 信息
echo -e "${BLUE}[INFO]${NC} Python: $(python --version)"
echo -e "${BLUE}[INFO]${NC} 工作目录: $API_DIR"
echo ""

# 检查环境变量文件
ENV_FILE="$PROJECT_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
    echo -e "${GREEN}✓${NC} 找到环境配置: $ENV_FILE"
else
    echo -e "${YELLOW}[WARNING]${NC} 未找到 .env 文件"
fi

# 启动服务
echo ""
echo -e "${BLUE}[INFO]${NC} 启动 FastAPI 服务..."
echo -e "${BLUE}[INFO]${NC} 访问地址: ${GREEN}http://localhost:8080${NC}"
echo -e "${BLUE}[INFO]${NC} API 文档: ${GREEN}http://localhost:8080/docs${NC}"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

# 进入 API 目录并启动
cd "$API_DIR"
python start_main.py
