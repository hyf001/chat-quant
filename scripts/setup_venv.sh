#!/bin/bash

###############################################################################
# Python 虚拟环境设置脚本
# 用途：创建虚拟环境并安装依赖
# 使用：./scripts/setup_venv.sh
###############################################################################

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Python 虚拟环境设置${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# 项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"
VENV_DIR="$API_DIR/.venv"
REQUIREMENTS_FILE="$API_DIR/requirements.txt"

# 指定 Python 版本
PYTHON_CMD="python3.12"

# 检查 Python 3.12
echo -e "${BLUE}[INFO]${NC} 检查 Python 3.12..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Python 3.12 未找到，尝试查找其他版本..."

    # 尝试 python3
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
        if [[ "$PYTHON_VERSION" == "3.12" ]]; then
            PYTHON_CMD="python3"
            echo -e "${GREEN}✓${NC} 找到 Python 3.12 (python3)"
        else
            echo -e "${RED}[ERROR]${NC} 系统 Python 版本是 $PYTHON_VERSION，不是 3.12"
            echo -e "${BLUE}[INFO]${NC} 请安装 Python 3.12："
            echo -e "${GREEN}  brew install python@3.12${NC}"
            exit 1
        fi
    else
        echo -e "${RED}[ERROR]${NC} 未找到 Python！"
        echo -e "${BLUE}[INFO]${NC} 请安装 Python 3.12："
        echo -e "${GREEN}  brew install python@3.12${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} 找到 Python 3.12"
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"
echo -e "${BLUE}[INFO]${NC} Python 路径: $(which $PYTHON_CMD)"
echo -e "${BLUE}[INFO]${NC} API 目录: $API_DIR"
echo -e "${BLUE}[INFO]${NC} 虚拟环境目录: $VENV_DIR"
echo ""

# 步骤 1: 创建虚拟环境
if [[ -d "$VENV_DIR" ]]; then
    echo -e "${YELLOW}[WARNING]${NC} 虚拟环境已存在: $VENV_DIR"
    read -p "是否删除并重新创建？[y/N]: " recreate
    if [[ "$recreate" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}[INFO]${NC} 删除旧的虚拟环境..."
        rm -rf "$VENV_DIR"
    else
        echo -e "${BLUE}[INFO]${NC} 使用现有虚拟环境"
    fi
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${BLUE}[INFO]${NC} 使用 $PYTHON_CMD 创建虚拟环境..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} 虚拟环境创建成功"
fi

# 步骤 2: 激活虚拟环境
echo -e "${BLUE}[INFO]${NC} 激活虚拟环境..."
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓${NC} 虚拟环境已激活"

# 验证虚拟环境中的 Python 版本
VENV_PYTHON_VERSION=$(python --version)
echo -e "${BLUE}[INFO]${NC} 虚拟环境 Python 版本: $VENV_PYTHON_VERSION"

# 步骤 3: 升级 pip
echo -e "${BLUE}[INFO]${NC} 升级 pip..."
pip install --upgrade pip setuptools wheel --quiet
echo -e "${GREEN}✓${NC} pip 升级完成"

# 步骤 4: 安装依赖
echo -e "${BLUE}[INFO]${NC} 安装项目依赖..."
echo -e "${BLUE}[INFO]${NC} 依赖文件: $REQUIREMENTS_FILE"
if pip install -r "$REQUIREMENTS_FILE"; then
    echo -e "${GREEN}✓${NC} 依赖安装成功"
else
    echo -e "${RED}[ERROR]${NC} 依赖安装失败"
    exit 1
fi

# 步骤 5: 验证关键包
echo ""
echo -e "${BLUE}[INFO]${NC} 验证关键包："
for pkg in fastapi uvicorn pandas sqlalchemy; do
    if python -c "import $pkg" 2>/dev/null; then
        version=$(python -c "import $pkg; print($pkg.__version__)" 2>/dev/null || echo "")
        echo -e "${GREEN}  ✓${NC} $pkg $version"
    else
        echo -e "${RED}  ✗${NC} $pkg"
    fi
done

# 完成
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ 虚拟环境设置完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${BLUE}[INFO]${NC} 激活虚拟环境："
echo -e "${GREEN}  source $VENV_DIR/bin/activate${NC}"
echo ""
echo -e "${BLUE}[INFO]${NC} 启动后端服务："
echo -e "${GREEN}  cd $API_DIR && python start_main.py${NC}"
echo ""
echo -e "${BLUE}[INFO]${NC} 或使用快捷脚本："
echo -e "${GREEN}  ./scripts/start_api.sh${NC}"
echo ""
