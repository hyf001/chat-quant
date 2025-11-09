# Claudable Docker 部署文档

## 概述

本文档描述如何在K8s环境中部署Claudable项目。

## 架构说明

- **基础镜像**: Node.js v22.12.0 + Python v3.10.17
- **前端**: Next.js 14 (端口: 3000)
- **后端**: FastAPI + Uvicorn (端口: 8000)
- **日志目录**: `/var/log/claudable/`
- **数据目录**: `/app/data/`

## 构建镜像

### 前置条件

确保在构建环境中可以访问：
- npm镜像源: `http://repositories.myhexin.com:8081/repository/npm-public/`
- pip镜像源: `http://repositories-public.myhexin.com:8087/repository/pypi-public/simple`

### 构建命令

```bash
# 在项目根目录执行
cd /path/to/Claudable

# 构建镜像
docker build -f docker/Dockerfile -t claudable:latest .

# 或指定版本
docker build -f docker/Dockerfile -t claudable:v1.0.0 .
```

### 构建参数（可选）

```bash
# 指定端口
docker build -f docker/Dockerfile \
  --build-arg API_PORT=8000 \
  --build-arg WEB_PORT=3000 \
  -t claudable:latest .
```

## 运行容器

### 本地测试

```bash
# 运行容器
docker run -d \
  --name claudable \
  -p 3000:3000 \
  -p 8000:8000 \
  -e API_PORT=8000 \
  -e WEB_PORT=3000 \
  -v /path/to/data:/app/data \
  claudable:latest

# 查看日志
docker logs -f claudable

# 进入容器查看服务日志
docker exec -it claudable tail -f /var/log/claudable/backend.log
docker exec -it claudable tail -f /var/log/claudable/frontend.log
```

### K8s部署

创建 `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: claudable
  namespace: your-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: claudable
  template:
    metadata:
      labels:
        app: claudable
    spec:
      containers:
      - name: claudable
        image: your-registry/claudable:latest
        ports:
        - containerPort: 3000
          name: frontend
        - containerPort: 8000
          name: backend
        env:
        - name: API_PORT
          value: "8000"
        - name: WEB_PORT
          value: "3000"
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /var/log/claudable
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: claudable-data
      - name: logs
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: claudable-service
  namespace: your-namespace
spec:
  selector:
    app: claudable
  ports:
  - name: frontend
    port: 3000
    targetPort: 3000
  - name: backend
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

## 目录结构

```
/app/
├── apps/
│   ├── web/           # 前端应用
│   └── api/           # 后端应用
├── data/              # 数据目录（需要持久化）
│   ├── cc.db         # SQLite数据库
│   └── projects/     # 项目文件
├── docker/
│   ├── Dockerfile    # 镜像构建文件
│   ├── start.sh      # 启动脚本
│   └── README.md     # 本文档
└── start.sh          # 容器内启动脚本

/var/log/claudable/
├── backend.log       # 后端日志
└── frontend.log      # 前端日志
```

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| API_PORT | 8000 | 后端服务端口 |
| WEB_PORT | 3000 | 前端服务端口 |
| NODE_ENV | production | Node.js环境 |
| PYTHONUNBUFFERED | 1 | Python输出不缓冲 |

## 健康检查

- **Liveness Probe**: HTTP GET `http://localhost:3000/`
- **Readiness Probe**: HTTP GET `http://localhost:3000/`
- **启动等待时间**: 60秒

## 日志查看

### 容器内查看

```bash
# 进入容器
docker exec -it claudable bash

# 查看后端日志
tail -f /var/log/claudable/backend.log

# 查看前端日志
tail -f /var/log/claudable/frontend.log
```

### K8s查看

```bash
# 查看Pod日志（启动脚本输出）
kubectl logs -f claudable-xxx -n your-namespace

# 查看后端日志
kubectl exec -it claudable-xxx -n your-namespace -- tail -f /var/log/claudable/backend.log

# 查看前端日志
kubectl exec -it claudable-xxx -n your-namespace -- tail -f /var/log/claudable/frontend.log
```

## 故障排查

### 容器启动失败

```bash
# 查看容器日志
docker logs claudable

# 进入容器检查
docker exec -it claudable bash
python --version
node --version
ps aux | grep -E "uvicorn|node"
```

### 服务无法访问

```bash
# 检查端口
netstat -tlnp | grep -E "3000|8000"

# 检查进程
ps aux | grep -E "uvicorn|node"

# 查看服务日志
tail -100 /var/log/claudable/backend.log
tail -100 /var/log/claudable/frontend.log
```

### Python依赖问题

```bash
# 验证Python环境
python -c "import fastapi, uvicorn, sqlalchemy"

# 查看已安装包
pip list

# 重新安装依赖（不推荐，应该重新构建镜像）
cd /app/apps/api
pip install -r requirements.txt
```

## 性能优化

### 生产环境建议

1. **前端构建优化**：在Dockerfile中添加 `npm run build`
2. **多阶段构建**：使用更小的基础镜像
3. **日志轮转**：配置logrotate
4. **资源限制**：合理设置K8s资源请求和限制

### 示例：启用前端生产构建

修改 `docker/Dockerfile`:

```dockerfile
# 安装前端依赖
WORKDIR /app/apps/web
RUN npm install

# 构建前端（启用此行）
RUN npm run build
```

修改 `docker/start.sh`:

```bash
# 使用生产模式启动
nohup npm run start -- --port ${WEB_PORT:-3000} \
    > "${FRONTEND_LOG}" 2>&1 &
```

## 版本信息

- **Node.js**: v22.12.0
- **Python**: v3.10.17
- **Next.js**: 14.2.5
- **FastAPI**: (见requirements.txt)

## 支持

如有问题，请查看：
1. 容器日志: `docker logs <container_id>`
2. 服务日志: `/var/log/claudable/*.log`
3. 环境检查: 运行 `python --version` 和 `node --version`
