#!/bin/bash

# Claudable Docker 镜像构建脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
IMAGE_NAME="claudable"
IMAGE_TAG="latest"
REGISTRY=""

# 打印使用说明
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n, --name NAME       镜像名称 (默认: claudable)"
    echo "  -t, --tag TAG         镜像标签 (默认: latest)"
    echo "  -r, --registry REG    镜像仓库地址 (可选)"
    echo "  -h, --help           显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                                          # 构建 claudable:latest"
    echo "  $0 -t v1.0.0                               # 构建 claudable:v1.0.0"
    echo "  $0 -r registry.example.com -t v1.0.0       # 构建 registry.example.com/claudable:v1.0.0"
    exit 1
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            IMAGE_NAME="$2"
            shift 2
            ;;
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# 构建完整镜像名
if [ -n "$REGISTRY" ]; then
    FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
else
    FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
fi

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Claudable Docker Build${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Build Configuration:${NC}"
echo "  Project Root: ${PROJECT_ROOT}"
echo "  Image Name:   ${FULL_IMAGE_NAME}"
echo "  Dockerfile:   ${SCRIPT_DIR}/Dockerfile"
echo ""

# 检查Dockerfile是否存在
if [ ! -f "${SCRIPT_DIR}/Dockerfile" ]; then
    echo -e "${RED}Error: Dockerfile not found at ${SCRIPT_DIR}/Dockerfile${NC}"
    exit 1
fi

# 检查start.sh是否存在
if [ ! -f "${SCRIPT_DIR}/start.sh" ]; then
    echo -e "${RED}Error: start.sh not found at ${SCRIPT_DIR}/start.sh${NC}"
    exit 1
fi

# 确认构建
echo -e "${YELLOW}Ready to build. Continue? (y/n)${NC}"
read -r CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${YELLOW}Build cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${GREEN}Starting build...${NC}"
echo ""

# 开始构建
cd "${PROJECT_ROOT}"

docker build \
    -f "${SCRIPT_DIR}/Dockerfile" \
    -t "${FULL_IMAGE_NAME}" \
    --build-arg API_PORT=8000 \
    --build-arg WEB_PORT=3000 \
    .

BUILD_STATUS=$?

echo ""
if [ $BUILD_STATUS -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Build Successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Image Details:${NC}"
    docker images "${FULL_IMAGE_NAME}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. 测试镜像:"
    echo "     docker run -d -p 3000:3000 -p 8000:8000 --name claudable ${FULL_IMAGE_NAME}"
    echo ""
    echo "  2. 查看日志:"
    echo "     docker logs -f claudable"
    echo ""
    echo "  3. 推送到仓库:"
    if [ -n "$REGISTRY" ]; then
        echo "     docker push ${FULL_IMAGE_NAME}"
    else
        echo "     docker tag ${FULL_IMAGE_NAME} your-registry/${FULL_IMAGE_NAME}"
        echo "     docker push your-registry/${FULL_IMAGE_NAME}"
    fi
    echo ""
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  Build Failed!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "  1. 检查网络连接（npm和pip镜像源）"
    echo "  2. 检查基础镜像是否可用"
    echo "  3. 查看构建日志中的错误信息"
    exit 1
fi
