# Dockerfile vs Dockerfile.dev 差异说明

## 核心差异

两个Dockerfile的**构建逻辑完全相同**，唯一的差异是：

### 1. 基础镜像来源

| Dockerfile (生产) | Dockerfile.dev (开发) |
|------------------|---------------------|
| `hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17` | `python:3.12.10-slim` |
| `hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0` | `node:22.18.0-bullseye-slim` |

### 2. Python目录结构

**Dockerfile (生产环境)**
```dockerfile
# 内网镜像已经将Python组织在 /usr/local/python/ 目录下
COPY --from=python-builder /usr/local/python /usr/local/python
```

**Dockerfile.dev (开发环境)**
```dockerfile
# 公共镜像的Python在 /usr/local/ 下，需要手动重组到 /usr/local/python/
RUN mkdir -p /usr/local/python/bin /usr/local/python/lib /usr/local/python/include
COPY --from=python-builder /usr/local/bin/python* /usr/local/python/bin/
COPY --from=python-builder /usr/local/bin/pip* /usr/local/python/bin/
COPY --from=python-builder /usr/local/lib/python3.12 /usr/local/python/lib/python3.12
COPY --from=python-builder /usr/local/lib/libpython3.12.so* /usr/local/python/lib/
COPY --from=python-builder /usr/local/lib/libpython3.so /usr/local/python/lib/
COPY --from=python-builder /usr/local/include/python3.12 /usr/local/python/include/python3.12
```

### 3. 镜像源配置

| 配置 | Dockerfile (生产) | Dockerfile.dev (开发) |
|-----|-----------------|---------------------|
| NPM源 | `http://repositories.myhexin.com:8081/repository/npm-public/` | `https://registry.npmmirror.com` |
| PIP源 | `http://repositories-public.myhexin.com:8087/repository/pypi-public/simple` | `https://mirrors.aliyun.com/pypi/simple/` |

### 4. Python版本

| Dockerfile (生产) | Dockerfile.dev (开发) |
|-----------------|---------------------|
| Python 3.10 | Python 3.12 |
| `PYTHONPATH=/usr/local/python/lib/python3.10/site-packages` | `PYTHONPATH=/usr/local/python/lib/python3.12/site-packages` |

## 为什么有这些差异？

### Python目录结构差异
- **内网镜像**：已经定制化，Python统一安装在 `/usr/local/python/`
- **公共镜像**：遵循标准Linux约定，Python安装在 `/usr/local/bin`, `/usr/local/lib` 等

为了保持最终运行环境一致，`Dockerfile.dev` 需要手动将Python文件重新组织到 `/usr/local/python/` 目录。

### 镜像源差异
- **生产环境**：使用内网镜像源，速度快且稳定
- **开发环境**：使用公网镜像源，便于本地验证

## 最终效果

尽管构建过程有差异，但**最终镜像的目录结构完全相同**：

```
/usr/local/python/
├── bin/
│   ├── python
│   ├── python3
│   ├── python3.12
│   ├── pip
│   └── pip3
├── lib/
│   ├── python3.12/
│   ├── libpython3.12.so
│   └── libpython3.so
└── include/
    └── python3.12/
```

因此，使用 `Dockerfile.dev` 验证成功后，可以确信 `Dockerfile` 也能正常工作。

## 构建命令

```bash
# 开发环境验证
docker build -f docker/Dockerfile.dev -t claudable-dev:latest .

# 生产环境构建
docker build -f docker/Dockerfile -t claudable:latest .
```

两者的运行方式完全相同，因为最终目录结构和PATH配置都一致。
