# Dockerfile 差异对比

## 概述

`Dockerfile` 和 `Dockerfile.dev` 的结构完全相同，**唯一的差异**是基础镜像和镜像源配置。

## 差异对比表

| 配置项 | Dockerfile (生产) | Dockerfile.dev (开发) |
|--------|-------------------|----------------------|
| **第一阶段 Python镜像** | `hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17` | `python:3.12.10-slim` |
| **第二阶段 Node.js镜像** | `hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0` | `node:22.18.0-bullseye-slim` |
| **第三阶段基础镜像** | `hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0` | `node:22.18.0-bullseye-slim` |
| **NPM镜像源** | `http://repositories.myhexin.com:8081/repository/npm-public/` | `https://registry.npmmirror.com` |
| **PIP镜像源** | `http://repositories-public.myhexin.com:8087/repository/pypi-public/simple` | `https://mirrors.aliyun.com/pypi/simple/` |
| **PIP trusted-host** | `repositories-public.myhexin.com` | `mirrors.aliyun.com` |
| **PYTHONPATH** | `/usr/local/python/lib/python3.10/site-packages` | `/usr/local/python/lib/python3.12/site-packages` |

## 详细差异

### 1. 基础镜像

**Dockerfile (生产环境)**
```dockerfile
FROM hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17 AS python-builder
FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0 AS node-builder
FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0
```

**Dockerfile.dev (开发环境)**
```dockerfile
FROM python:3.12.10-slim AS python-builder
FROM node:22.18.0-bullseye-slim AS node-builder
FROM node:22.18.0-bullseye-slim
```

### 2. NPM镜像源

**Dockerfile (生产环境)**
```dockerfile
RUN npm config set registry "http://repositories.myhexin.com:8081/repository/npm-public/"
```

**Dockerfile.dev (开发环境)**
```dockerfile
RUN npm config set registry "https://registry.npmmirror.com"
```

### 3. PIP镜像源

**Dockerfile (生产环境)**
```dockerfile
RUN pip config set global.index-url http://repositories-public.myhexin.com:8087/repository/pypi-public/simple && \
    pip config set global.trusted-host repositories-public.myhexin.com
```

**Dockerfile.dev (开发环境)**
```dockerfile
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com
```

### 4. Python版本差异导致的PATH变化

**Dockerfile (生产环境 - Python 3.10)**
```dockerfile
ENV PATH=/usr/local/python/bin:/usr/local/bin:/usr/bin:$PATH \
    PYTHONPATH=/usr/local/python/lib/python3.10/site-packages
```

**Dockerfile.dev (开发环境 - Python 3.12)**
```dockerfile
ENV PATH=/usr/local/python/bin:/usr/local/bin:/usr/bin:$PATH \
    PYTHONPATH=/usr/local/python/lib/python3.12/site-packages
```

## 相同的部分

以下部分在两个Dockerfile中**完全相同**：

- ✅ 多阶段构建结构（3个阶段）
- ✅ Python环境复制方式：`COPY --from=python-builder /usr/local/python /usr/local/python`
- ✅ 工作目录设置
- ✅ 项目文件复制
- ✅ 依赖安装流程（npm install, pip install）
- ✅ 日志目录创建
- ✅ 数据目录创建
- ✅ 启动脚本复制
- ✅ 端口暴露（3000, 8000）
- ✅ 健康检查配置
- ✅ 启动命令（CMD ["/app/start.sh"]）

## 验证目的

使用 `Dockerfile.dev` 在本地验证的目的是：

1. **验证构建流程**：确保Dockerfile结构正确，能够成功构建
2. **验证依赖安装**：确保npm和pip依赖都能正确安装
3. **验证Python环境**：确认不使用虚拟环境，直接使用容器Python环境的方案可行
4. **验证服务启动**：确保start.sh脚本能正确启动前后端服务
5. **验证日志输出**：确认日志能正确输出到 /var/log/claudable/

## 使用场景

| Dockerfile | 使用场景 | 网络要求 |
|-----------|---------|---------|
| `Dockerfile` | K8s生产环境部署 | 内网（能访问 myhexin.com 镜像源） |
| `Dockerfile.dev` | 本地开发验证 | 公网（能访问淘宝npm源和阿里云pip源） |

## 切换方法

从开发验证切换到生产部署，只需：

```bash
# 开发环境构建
docker build -f docker/Dockerfile.dev -t claudable-dev:latest .

# 生产环境构建（验证成功后）
docker build -f docker/Dockerfile -t claudable:latest .
```

两者的运行方式完全相同，因为除了基础镜像和源地址，其他所有配置都一致。
