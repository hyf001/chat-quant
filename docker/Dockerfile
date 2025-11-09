# ==================== 第一阶段：Python镜像 ====================
FROM hub-dev.hexin.cn/business-baseimage-python/python:v3.12.10 AS python-builder

# ==================== 第二阶段：Node.js镜像 ====================
FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0 AS node-builder

# ==================== 第三阶段：构建最终镜像 ====================
FROM hub-dev.hexin.cn/business-baseimage-frontend/node:v22.12.0

# 设置工作目录
WORKDIR /app

# 从Python镜像复制Python环境到 /usr/local/python
COPY --from=python-builder /usr/local/python /usr/local/python

# 设置环境变量
ENV PATH=/usr/local/python/bin:/usr/local/bin:/usr/bin:$PATH \
    PYTHONPATH=/usr/local/python/lib/python3.10/site-packages \
    PYTHONUNBUFFERED=1 \
    API_PORT=8080 \
    WEB_PORT=3000

# 验证Python和Node环境
RUN python --version && node --version && npm --version

# 复制项目文件
COPY . /app/

# ==================== 安装依赖 ====================

# 配置npm镜像源
RUN npm config set registry "http://repositories.myhexin.com:8081/repository/npm-public/"

#安装claude_code
RUN npm install -g @anthropic-ai/claude-code

# 安装根目录依赖（跳过postinstall脚本，因为容器中不需要虚拟环境）
RUN npm install

# 安装前端依赖
RUN cd /app/apps/web && npm install
ENV NODE_ENV=production

# 配置pip镜像源并安装Python依赖
WORKDIR /app/apps/api
RUN pip config set global.index-url http://repositories-public.myhexin.com:8087/repository/pypi-public/simple && \
    pip config set global.trusted-host repositories-public.myhexin.com

# 安装Python依赖（直接安装到容器的Python环境）
RUN pip install --no-cache-dir -r requirements.txt

# 验证关键Python包
RUN python -c "import fastapi; import uvicorn; import sqlalchemy; print('Python dependencies OK')"

# ==================== 准备运行环境 ====================

# 创建日志目录和数据目录
RUN mkdir -p /var/log/claudable

# 创建 cbas 用户来运行应用（Claude Agent SDK 不允许 root 运行）
RUN groupadd -r cbas && useradd -r -g cbas -d /app -s /bin/bash cbas
# 设置目录权限，确保 cbas 用户可以访问
RUN chown -R cbas:cbas /app /var/log/claudable

# 复制启动脚本
COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh
COPY docker/start-services.sh /app/start-services.sh
RUN chmod +x /app/start-services.sh

# 回到应用根目录
WORKDIR /app

# 暴露端口
EXPOSE 3000 8080


# 启动服务
CMD ["/app/start.sh"]
