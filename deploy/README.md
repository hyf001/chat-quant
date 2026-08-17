# Chat-Quant 部署说明

目标服务器：`47.95.205.124`

访问域名：`https://chatq.nanbende.com`

## 两种部署模式

### 模式 A：完整部署到阿里云

项目代码、后端服务、前端静态资源都部署在阿里云服务器上。使用：

```bash
bash deploy/0_remote_deploy.sh
```

### 模式 B：本机运行，阿里云通过 SSH 隧道中转

项目继续运行在你的本机，阿里云服务器只负责公网 Nginx 入口。适合把本地开发中的 Web 临时给好友试用。

先配置阿里云 Nginx 为隧道代理模式：

```bash
bash deploy/3_setup_local_tunnel_server.sh
```

再在本机启动 Chat-Quant、Caddy 统一入口和 SSH 反向隧道：

```bash
bash deploy/4_start_local_tunnel.sh
```

请使用 `bash` 执行脚本，不要用 `sh`。启动脚本会逐项检查本地 dev 服务、Caddy 和 SSH 隧道；已经启动且健康的服务会跳过。启动完成后好友可以访问 `deploy/server.config` 中 `DOMAIN` 对应的域名，例如 `https://chatq.nanbende.com`。

停止本机公开访问栈：

```bash
bash deploy/5_stop_local_tunnel.sh
```

脚本复用 `deploy/server.config` 中的服务器、域名和 SSH key 配置。可用环境变量覆盖隧道端口：

```bash
TUNNEL_REMOTE_PORT=18081 LOCAL_PROXY_PORT=18081 bash deploy/4_start_local_tunnel.sh
```

完整说明见：`docs/local-public-access-via-aliyun.md`。

## 使用

1. 确认域名 `chatq.nanbende.com` 的 A 记录已解析到 `47.95.205.124`。
2. 确认 `deploy/server.config` 中的 `SSH_KEY_PATH` 指向服务器 root 登录密钥。
3. 在项目根目录执行：

```bash
bash deploy/0_remote_deploy.sh
```

脚本会通过 SSH 密钥登录服务器，在服务器上用 git 拉取 `https://github.com/hyf001/chat-quant.git`，然后自动安装 Python 3.12、Node.js 20、Nginx、Certbot，构建后端和前端，申请 HTTPS 证书并启动服务。

## 常用运维命令

```bash
ssh -i /Users/huyufei/Documents/hyf/doc/阿里云/ecs密钥对.pem root@47.95.205.124
journalctl -u chat-quant -f
systemctl restart chat-quant
systemctl reload nginx
```

## 配置文件

- `deploy/server.config`：服务器、SSH 密钥、域名、仓库、应用目录配置。
- `deploy/server.password`：服务器密码 fallback，本文件已被 `deploy/.gitignore` 忽略。
- `/opt/chat-quant/config.json`：运行配置，部署脚本会生成并供后端与前端构建共同使用。
- `deploy/nginx.conf`：HTTPS Nginx 模板。
