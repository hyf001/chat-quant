# Chat-Quant 部署说明

目标服务器：`47.95.205.124`

访问域名：`https://chatq.nanbende.com`

## 使用

1. 确认域名 `chatq.nanbende.com` 的 A 记录已解析到 `47.95.205.124`。
2. 确认 `deploy/server.env` 中的 `SSH_KEY_PATH` 指向服务器 root 登录密钥。
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

- `deploy/server.env`：服务器、SSH 密钥、域名、仓库、应用目录配置。
- `deploy/server.password`：服务器密码 fallback，本文件已被 `deploy/.gitignore` 忽略。
- `deploy/.env.production`：后端生产环境变量模板，首次部署会复制为 `/opt/chat-quant/.env`。
- `deploy/nginx.conf`：HTTPS Nginx 模板。
