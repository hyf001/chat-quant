# CentOS 8 生产环境部署检查清单

## 一、基础镜像检查

### 1.1 Node.js 镜像检查
```bash
# 进入 Node.js 镜像检查
docker run -it --rm hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0 bash

# 在容器内执行以下命令：
node --version          # 应该是 v22.x
npm --version           # 应该有 npm
which bash              # 应该是 /bin/bash
which curl              # 检查是否有 curl（健康检查需要）
which ps                # 检查是否有 ps（启动脚本需要）
which kill              # 检查是否有 kill（启动脚本需要）
which tail              # 检查是否有 tail（启动脚本需要）
which nohup             # 检查是否有 nohup（启动脚本需要）
```

### 1.2 Python 镜像检查
```bash
# 进入 Python 镜像检查
docker run -it --rm hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17 bash

# 在容器内执行以下命令：
python --version        # 应该是 Python 3.10.17
pip --version           # 应该有 pip
ls -la /usr/local/python/   # 检查Python目录结构
echo $PATH              # 查看PATH配置
```

### 1.3 Python 目录结构验证
```bash
# 在 Python 镜像内检查目录结构
ls -la /usr/local/python/bin/
ls -la /usr/local/python/lib/
ls -la /usr/local/python/include/

# 应该能找到：
# /usr/local/python/bin/python
# /usr/local/python/bin/pip
# /usr/local/python/lib/python3.10/
```

## 二、必需的系统工具

### 2.1 启动脚本依赖的命令
以下命令必须存在于 **Node.js 基础镜像**中（因为最终镜像基于Node镜像）：

| 命令 | 用途 | 检查命令 |
|------|------|---------|
| `bash` | 启动脚本解释器 | `which bash` |
| `nohup` | 后台运行服务 | `which nohup` |
| `ps` | 进程检查 | `which ps` |
| `kill` | 停止进程 | `which kill` |
| `tail` | 查看日志 | `which tail` |
| `mkdir` | 创建目录 | `which mkdir` |
| `python` | 运行后端 | 复制后应该在 `/usr/local/python/bin/python` |
| `node` | 运行前端 | Node镜像自带 |
| `npm` | 运行前端 | Node镜像自带 |

### 2.2 健康检查依赖
```bash
# 健康检查使用 curl，如果镜像中没有，需要安装或修改健康检查方式
which curl
```

**如果没有 curl**，有两种解决方案：

**方案1**: 在Dockerfile中安装curl
```dockerfile
# 在 Dockerfile 的开始部分添加
RUN yum install -y curl && yum clean all
```

**方案2**: 修改健康检查为不依赖curl
```dockerfile
# 修改健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import http.client; conn = http.client.HTTPConnection('localhost', 3000); conn.request('GET', '/'); r = conn.getresponse(); exit(0 if r.status == 200 else 1)"
```

## 三、网络和镜像源检查

### 3.1 NPM 镜像源
```bash
# 在构建环境测试
curl -I http://repositories.myhexin.com:8081/repository/npm-public/

# 应该返回 HTTP 200 或 302
```

### 3.2 PIP 镜像源
```bash
# 在构建环境测试
curl -I http://repositories-public.myhexin.com:8087/repository/pypi-public/simple

# 应该返回 HTTP 200
```

### 3.3 端口可用性
确认以下端口在K8s环境中可以使用：
- **3000** - 前端服务
- **8000** - 后端服务

## 四、文件系统权限检查

### 4.1 关键目录写权限
以下目录需要在容器中可写：

| 目录 | 用途 | Dockerfile中的创建 |
|------|------|------------------|
| `/var/log/claudable/` | 服务日志 | ✅ RUN mkdir -p /var/log/claudable |
| `/app/data/` | 数据库和项目文件 | ✅ RUN mkdir -p /app/data/projects |
| `/app/apps/web/.next/` | Next.js构建缓存 | 运行时创建 |

**K8s环境注意事项**：
- 如果容器以非root用户运行，需要确保这些目录的权限正确
- 建议在Dockerfile中添加：
```dockerfile
RUN chmod 777 /var/log/claudable && \
    chmod 777 /app/data
```

### 4.2 持久化存储
**必须持久化的目录**（K8s需要挂载PV）：
- `/app/data/` - 包含数据库和用户项目文件

**可选持久化**：
- `/var/log/claudable/` - 日志文件

## 五、环境变量配置

### 5.1 必需的环境变量
以下环境变量已在Dockerfile中设置，K8s deployment可以覆盖：

```yaml
env:
- name: API_PORT
  value: "8000"
- name: WEB_PORT
  value: "3000"
- name: NODE_ENV
  value: "production"
- name: PYTHONUNBUFFERED
  value: "1"
```

### 5.2 可选的环境变量
如果需要自定义配置：

```yaml
- name: DATABASE_URL
  value: "sqlite:////app/data/cc.db"  # 或 PostgreSQL URL
```

## 六、构建前检查清单

### 6.1 Dockerfile 检查
```bash
# 在项目根目录执行
cat docker/Dockerfile

# 确认以下内容：
# ✅ 第2行: FROM hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17
# ✅ 第5行: FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0
# ✅ 第8行: FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0
# ✅ 第14行: COPY --from=python-builder /usr/local/python /usr/local/python
# ✅ 第33行: npm镜像源配置
# ✅ 第47-48行: pip镜像源配置
# ✅ 第66行: COPY docker/start.sh /app/start.sh
# ✅ 第67行: RUN chmod +x /app/start.sh
```

### 6.2 启动脚本检查
```bash
# 检查脚本权限
ls -la docker/start.sh
# 应该显示 -rwxr-xr-x（可执行）

# 检查脚本语法
bash -n docker/start.sh
# 没有输出表示语法正确
```

### 6.3 依赖文件检查
```bash
# 检查关键文件存在
ls -la apps/api/requirements.txt
ls -la apps/web/package.json
ls -la package.json
ls -la docker/start.sh

# 都应该存在
```

## 七、构建命令

### 7.1 完整构建命令
```bash
cd /path/to/Claudable

# 构建镜像
docker build -f docker/Dockerfile -t claudable:v1.0.0 .

# 构建时间预计: 10-20分钟
```

### 7.2 构建验证
```bash
# 检查镜像
docker images | grep claudable

# 应该看到新构建的镜像
# claudable  v1.0.0  <IMAGE_ID>  <TIME>  ~1.5-2GB
```

## 八、运行前测试（可选）

如果想在推送到K8s前本地测试：

```bash
# 运行容器
docker run -d \
  --name claudable-test \
  -p 3000:3000 \
  -p 8000:8000 \
  -e API_PORT=8000 \
  -e WEB_PORT=3000 \
  claudable:v1.0.0

# 等待启动（约30秒）
sleep 30

# 检查日志
docker logs claudable-test

# 应该看到：
# ========================================
#   All Services Started Successfully
# ========================================

# 测试服务
curl http://localhost:3000
curl http://localhost:8000/api/projects

# 清理
docker stop claudable-test
docker rm claudable-test
```

## 九、CentOS 8 特定检查

### 9.1 SELinux 状态
```bash
# 检查SELinux状态（如果启用可能影响文件权限）
getenforce

# 如果是 Enforcing，可能需要设置正确的SELinux上下文
```

### 9.2 防火墙规则
如果在虚拟机上测试：
```bash
# 检查端口是否开放
firewall-cmd --list-ports

# 如果需要开放端口
firewall-cmd --add-port=3000/tcp --permanent
firewall-cmd --add-port=8000/tcp --permanent
firewall-cmd --reload
```

## 十、常见问题预判

### 10.1 如果 curl 不存在
修改 `docker/Dockerfile` 第75-76行：
```dockerfile
# 方案1: 安装curl
RUN yum install -y curl && yum clean all

# 方案2: 使用Python健康检查（推荐）
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000'); exit(0)" || exit 1
```

### 10.2 如果权限问题
在 `docker/Dockerfile` 第62行后添加：
```dockerfile
# 设置目录权限，支持非root用户
RUN chmod -R 777 /var/log/claudable /app/data
```

### 10.3 如果Python路径不对
进入Python镜像验证：
```bash
docker run -it --rm hub-dev.hexin.cn/business-baseimage-python/python:v3.10.17 bash
ls -la /usr/local/python/
```

如果Python不在 `/usr/local/python/`，需要修改Dockerfile第14行的COPY路径。

## 十一、推送到镜像仓库

### 11.1 打标签
```bash
# 假设你的镜像仓库是 registry.example.com
docker tag claudable:v1.0.0 registry.example.com/claudable:v1.0.0
```

### 11.2 推送
```bash
docker push registry.example.com/claudable:v1.0.0
```

## 十二、K8s 部署注意事项

### 12.1 资源限制
建议配置：
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### 12.2 持久化卷
```yaml
volumeMounts:
- name: data
  mountPath: /app/data
- name: logs
  mountPath: /var/log/claudable

volumes:
- name: data
  persistentVolumeClaim:
    claimName: claudable-data-pvc
- name: logs
  emptyDir: {}
```

### 12.3 启动等待时间
```yaml
readinessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 60  # Next.js启动需要时间
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 90
  periodSeconds: 30
```

## 检查完成标准

- [ ] Node.js 基础镜像可访问
- [ ] Python 基础镜像可访问
- [ ] Python 目录在 `/usr/local/python/`
- [ ] 必需命令都存在（bash, nohup, ps, kill, tail）
- [ ] curl 存在或健康检查已修改
- [ ] NPM 镜像源可访问
- [ ] PIP 镜像源可访问
- [ ] 端口 3000 和 8000 可用
- [ ] 所有文件和脚本存在
- [ ] Dockerfile 语法正确
- [ ] 构建成功并能运行
- [ ] K8s PV/PVC 已配置

完成以上检查后，可以安全地发布到生产环境！
