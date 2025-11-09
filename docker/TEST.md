# Claudable 本地验证指南

## 概述

本文档描述如何在本地环境验证 Docker 镜像构建和运行。

## 前置条件

1. 安装 Docker Desktop
2. 确保 Docker 服务正在运行
3. 网络可以访问国内镜像源（淘宝npm源、阿里云pip源）

## 验证步骤

### 1. 准备基础镜像

开发环境使用的公共镜像：
- Node.js: `node:22.18.0-bullseye-slim`
- Python: `python:3.12.10-slim`

```bash
# 拉取镜像（如果本地没有）
docker pull node:22.18.0-bullseye-slim
docker pull python:3.12.10-slim

# 验证镜像
docker images | grep -E "node|python"
```

### 2. 构建开发镜像

```bash
# 进入项目目录
cd /Users/yddyf/Documents/code/claudable-20251013/Claudable

# 使用构建脚本（推荐）
./docker/build-dev.sh

# 或手动构建
docker build -f docker/Dockerfile.dev -t claudable-dev:latest .
```

**构建过程说明：**
- ✅ 从 Python 镜像复制 Python 环境
- ✅ 使用淘宝npm源安装前端依赖
- ✅ 使用阿里云pip源安装后端依赖
- ✅ 验证依赖安装成功
- ⏱️ 预计时间：5-10分钟（首次构建）

### 3. 运行容器

```bash
# 启动容器
docker run -d \
  --name claudable-dev \
  -p 3000:3000 \
  -p 8000:8000 \
  -e API_PORT=8000 \
  -e WEB_PORT=3000 \
  claudable-dev:latest

# 查看容器状态
docker ps | grep claudable-dev
```

### 4. 查看启动日志

```bash
# 查看容器主日志（启动脚本输出）
docker logs -f claudable-dev

# 应该看到类似输出：
# ========================================
#   Claudable Service Startup
# ========================================
# Environment Information:
#   Python: Python 3.12.10
#   Node.js: v22.18.0
#   ...
# ✓ Backend started (PID: xxx)
# ✓ Frontend started (PID: xxx)
# All Services Started Successfully
```

### 5. 查看服务日志

```bash
# 查看后端日志
docker exec -it claudable-dev tail -f /var/log/claudable/backend.log

# 查看前端日志（新开一个终端）
docker exec -it claudable-dev tail -f /var/log/claudable/frontend.log
```

### 6. 测试服务

```bash
# 测试前端（应该返回HTML）
curl http://localhost:3000

# 测试后端（应该返回JSON）
curl http://localhost:8000/api/projects

# 在浏览器中访问
open http://localhost:3000
```

### 7. 进入容器调试

```bash
# 进入容器
docker exec -it claudable-dev bash

# 在容器内执行命令
python --version        # 验证Python
node --version          # 验证Node.js
ps aux | grep -E "uvicorn|node"  # 查看进程
ls -la /var/log/claudable/       # 查看日志文件
exit
```

### 8. 清理环境

```bash
# 停止容器
docker stop claudable-dev

# 删除容器
docker rm claudable-dev

# （可选）删除镜像
docker rmi claudable-dev:latest
```

## 验证检查清单

- [ ] Docker镜像构建成功
- [ ] 容器启动成功，无报错
- [ ] 后端服务正常运行（端口8000）
- [ ] 前端服务正常运行（端口3000）
- [ ] 可以访问前端页面 http://localhost:3000
- [ ] 可以访问后端API http://localhost:8000/api/projects
- [ ] 日志正常输出到 /var/log/claudable/
- [ ] Python环境正常（无虚拟环境依赖）
- [ ] Node.js环境正常

## 常见问题

### 问题1: 镜像构建失败

**症状**: npm install 或 pip install 失败

**解决方案**:
```bash
# 检查网络连接
ping registry.npmmirror.com
ping mirrors.aliyun.com

# 手动测试镜像源
npm config get registry
pip config list
```

### 问题2: 容器启动后立即退出

**症状**: docker ps 看不到运行中的容器

**解决方案**:
```bash
# 查看容器日志
docker logs claudable-dev

# 查看退出状态
docker ps -a | grep claudable-dev

# 以交互模式运行调试
docker run -it --rm claudable-dev:latest /bin/bash
```

### 问题3: 端口已被占用

**症状**: Error: bind: address already in use

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :3000
lsof -i :8000

# 停止占用端口的服务
# 或使用不同的端口
docker run -d -p 3001:3000 -p 8001:8000 --name claudable-dev claudable-dev:latest
```

### 问题4: Python依赖缺失

**症状**: ModuleNotFoundError: No module named 'xxx'

**解决方案**:
```bash
# 进入容器检查
docker exec -it claudable-dev python -c "import fastapi; import uvicorn"

# 查看已安装的包
docker exec -it claudable-dev pip list

# 如果缺失，可能是构建时网络问题，需要重新构建
docker rmi claudable-dev:latest
./docker/build-dev.sh
```

### 问题5: 前端编译错误

**症状**: 前端日志显示编译错误

**解决方案**:
```bash
# 查看详细错误
docker exec -it claudable-dev cat /var/log/claudable/frontend.log

# 进入容器手动运行
docker exec -it claudable-dev bash
cd /app/apps/web
npm run dev
```

## 镜像对比

| 特性 | 开发镜像 (Dockerfile.dev) | 生产镜像 (Dockerfile) |
|------|---------------------------|----------------------|
| Node基础镜像 | node:22.18.0-bullseye-slim | hub-dev.hexin.cn/...node:v22.12.0 |
| Python基础镜像 | python:3.12.10-slim | hub-dev.hexin.cn/...python:v3.10.17 |
| NPM源 | 淘宝镜像 (npmmirror.com) | 内网镜像 (myhexin.com) |
| PIP源 | 阿里云镜像 (aliyun.com) | 内网镜像 (myhexin.com) |
| 网络要求 | 公网 | 内网 |
| 用途 | 本地验证 | K8s生产部署 |

## 性能基准

**预期指标**（参考值）：
- 镜像构建时间：5-10分钟（首次）
- 镜像大小：~1.5-2GB
- 容器启动时间：10-30秒
- 内存占用：~500MB-1GB
- CPU占用：低（空闲状态）

## 成功标志

当看到以下输出时，说明验证成功：

```
========================================
  All Services Started Successfully
========================================

Service Status:
  Backend:  http://0.0.0.0:8000 (PID: xxx)
  Frontend: http://0.0.0.0:3000 (PID: xxx)

Logs:
  Backend:  /var/log/claudable/backend.log
  Frontend: /var/log/claudable/frontend.log

Container is ready!
```

并且可以正常访问：
- ✅ http://localhost:3000 - 前端页面
- ✅ http://localhost:8000/api/projects - 后端API

## 下一步

验证成功后：
1. 确认生产环境的基础镜像和镜像源配置
2. 使用 `docker/Dockerfile` 构建生产镜像
3. 推送镜像到K8s镜像仓库
4. 使用 `docker/README.md` 中的K8s配置进行部署

## 技术支持

如遇到问题：
1. 查看日志文件
2. 进入容器调试
3. 检查网络和镜像源
4. 参考本文档的常见问题部分
