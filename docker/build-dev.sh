#!/bin/bash

# Claudable 开发环境 Docker 镜像构建脚本
# 使用本地公共镜像和国内镜像源进行验证

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
IMAGE_NAME="claudable-dev"
IMAGE_TAG="latest"

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Claudable Development Build${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Build Configuration:${NC}"
echo "  Project Root: ${PROJECT_ROOT}"
echo "  Image Name:   ${IMAGE_NAME}:${IMAGE_TAG}"
echo "  Dockerfile:   ${SCRIPT_DIR}/Dockerfile.dev"
echo ""
echo -e "${YELLOW}Using Public Images:${NC}"
echo "  Node.js:      node:22.18.0-bullseye-slim"
echo "  Python:       python:3.12.10-slim"
echo ""
echo -e "${YELLOW}Using Public Mirrors:${NC}"
echo "  NPM:          https://registry.npmmirror.com"
echo "  PIP:          https://mirrors.aliyun.com/pypi/simple/"
echo ""

# 检查Dockerfile是否存在
if [ ! -f "${SCRIPT_DIR}/Dockerfile.dev" ]; then
    echo -e "${RED}Error: Dockerfile.dev not found at ${SCRIPT_DIR}/Dockerfile.dev${NC}"
    exit 1
fi

# 检查start.sh是否存在
if [ ! -f "${SCRIPT_DIR}/start.sh" ]; then
    echo -e "${RED}Error: start.sh not found at ${SCRIPT_DIR}/start.sh${NC}"
    exit 1
fi

# 检查本地是否有所需镜像
echo -e "${YELLOW}Checking local images...${NC}"

if docker images node:22.18.0-bullseye-slim --format "{{.Repository}}:{{.Tag}}" | grep -q "node:22.18.0-bullseye-slim"; then
    echo -e "${GREEN}✓ Found node:22.18.0-bullseye-slim${NC}"
else
    echo -e "${YELLOW}⚠ node:22.18.0-bullseye-slim not found locally${NC}"
    echo -e "${YELLOW}  Pulling from Docker Hub...${NC}"
    docker pull node:22.18.0-bullseye-slim
fi

if docker images python:3.12.10-slim --format "{{.Repository}}:{{.Tag}}" | grep -q "python:3.12.10-slim"; then
    echo -e "${GREEN}✓ Found python:3.12.10-slim${NC}"
else
    echo -e "${YELLOW}⚠ python:3.12.10-slim not found locally${NC}"
    echo -e "${YELLOW}  Pulling from Docker Hub...${NC}"
    docker pull python:3.12.10-slim
fi

echo ""

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
    -f "${SCRIPT_DIR}/Dockerfile.dev" \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    --build-arg API_PORT=8000 \
    --build-arg WEB_PORT=3000 \
    --progress=plain \
    .

BUILD_STATUS=$?

echo ""
if [ $BUILD_STATUS -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Build Successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Image Details:${NC}"
    docker images "${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo ""
    echo "  1. 运行容器:"
    echo -e "     ${BLUE}docker run -d -p 3000:3000 -p 8000:8000 --name claudable-dev ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
    echo ""
    echo "  2. 查看启动日志:"
    echo -e "     ${BLUE}docker logs -f claudable-dev${NC}"
    echo ""
    echo "  3. 查看后端服务日志:"
    echo -e "     ${BLUE}docker exec -it claudable-dev tail -f /var/log/claudable/backend.log${NC}"
    echo ""
    echo "  4. 查看前端服务日志:"
    echo -e "     ${BLUE}docker exec -it claudable-dev tail -f /var/log/claudable/frontend.log${NC}"
    echo ""
    echo "  5. 测试服务:"
    echo -e "     ${BLUE}curl http://localhost:3000${NC}  (前端)"
    echo -e "     ${BLUE}curl http://localhost:8000/api/projects${NC}  (后端)"
    echo ""
    echo "  6. 停止并删除容器:"
    echo -e "     ${BLUE}docker stop claudable-dev && docker rm claudable-dev${NC}"
    echo ""
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  Build Failed!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "  1. 检查网络连接"
    echo "  2. 检查镜像源是否可访问"
    echo "  3. 查看构建日志中的错误信息"
    echo "  4. 确保本地镜像存在:"
    echo "     docker images | grep -E 'node|python'"
    exit 1
fi
