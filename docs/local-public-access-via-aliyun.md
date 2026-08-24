# 本机运行并通过阿里云服务器暴露公网访问

本文适用于这种场景：

- Chat-Quant 继续运行在你的本机。
- 好友通过互联网访问你的域名。
- 阿里云服务器只作为公网入口和流量中转。
- 不要求你的本地网络有公网 IP，也不需要路由器端口转发。

## 方案结构

```text
好友浏览器
  -> http(s)://chatq.nanbende.com
  -> 阿里云 Nginx
  -> 阿里云本机端口 127.0.0.1:18080
  -> SSH 反向隧道
  -> 你的本机 127.0.0.1:18080
  -> 本机 Caddy
       /      -> apps/web/dist
       /api/* -> 127.0.0.1:12345
```

不要直接把 Vite 开发服务端口 `12346` 暴露给好友。当前前端在开发模式下会把 API 地址写成 `http://127.0.0.1:12345`，好友浏览器会访问他自己电脑的 `127.0.0.1:12345`，导致 API 不可用。

推荐做法是：前端使用 production build，API 使用本机 FastAPI，二者通过本机 Caddy 合并成一个统一入口 `127.0.0.1:18080`。

## 前置条件

本机需要：

- Node.js、npm、Python、uv 已按项目 README 安装好。
- 能 SSH 登录阿里云服务器。
- 可选：安装 Caddy。

阿里云服务器需要：

- 已安装 Nginx。
- 安全组开放 `80` 和 `443`。
- 域名 A 记录指向阿里云服务器公网 IP。

本文示例值：

```text
域名：chatq.nanbende.com
阿里云公网 IP：47.95.205.124
阿里云用户：root
本机统一入口：127.0.0.1:18080
本机 API：127.0.0.1:12345
```

按你的实际情况替换这些值。

## 推荐：直接使用脚本

本方案已经封装到 `deploy/` 目录。

首次配置阿里云服务器 Nginx：

```bash
bash deploy/3_setup_local_tunnel_server.sh
```

每次准备给好友访问时，在本机启动服务和 SSH 隧道：

```bash
bash deploy/4_start_local_tunnel.sh
```

请使用 `bash` 执行脚本，不要用 `sh`。启动脚本会逐项检查本地 dev 服务、Caddy 和 SSH 隧道；已经启动且健康的服务会跳过。启动完成后，好友可以访问 `deploy/server.config` 中 `DOMAIN` 对应的域名。

停止本机公开访问栈：

```bash
bash deploy/5_stop_local_tunnel.sh
```

脚本默认复用 `deploy/server.config` 中的 `SERVER_IP`、`SERVER_USER`、`SSH_PORT`、`SSH_KEY_PATH`、`DOMAIN`、`SERVICE_NAME` 和 `SSL_EMAIL`。

如果要覆盖隧道端口：

```bash
TUNNEL_REMOTE_PORT=18081 LOCAL_PROXY_PORT=18081 bash deploy/4_start_local_tunnel.sh
```

如果要让公网访问先输入密码：

```bash
printf '%s\n' '换成你的访问密码' > deploy/public-auth.password
PUBLIC_AUTH_ENABLED=true PUBLIC_AUTH_USER=friend bash deploy/3_setup_local_tunnel_server.sh
PUBLIC_AUTH_USER=friend bash deploy/4_start_local_tunnel.sh
```

`deploy/public-auth.password` 已被 git 忽略。脚本会在阿里云服务器上生成 `/etc/nginx/chat-quant.htpasswd`，并把认证加到公网 Nginx 入口；本地 Caddy 和 SSH 隧道端口不会额外加密码。

下面的章节是脚本背后的手动步骤，方便排查和理解。

## 1. 本机准备运行配置

确认项目根目录的 `config.json` 保持本机监听：

```json
{
  "database_path": "data/chat-quant.db",
  "api_host": "127.0.0.1",
  "api_port": 12345,
  "web_host": "127.0.0.1",
  "web_port": 12346
}
```

这里不需要改成 `0.0.0.0`。公网访问通过 SSH 隧道进入，不直接暴露本机端口。

## 2. 本机启动 Chat-Quant

在项目根目录执行：

```bash
npm run dev:web-start
```

确认 API 可用：

```bash
curl http://127.0.0.1:12345/api/health
```

构建前端静态文件：

```bash
npm --prefix apps/web run build
```

构建产物会生成在：

```text
apps/web/dist
```

## 3. 本机配置统一入口

推荐使用 Caddy。macOS 可用 Homebrew 安装：

```bash
brew install caddy
```

在项目根目录创建本机专用配置文件，例如 `.dev/Caddyfile.public-local`：

```caddyfile
http://127.0.0.1:18080 {
  root * /Users/huyufei/Documents/hyf/code/github/chat-quant/apps/web/dist
  encode gzip

  handle /api/* {
    reverse_proxy 127.0.0.1:12345
  }

  handle {
    try_files {path} /index.html
    file_server
  }
}
```

启动 Caddy：

```bash
caddy run --config .dev/Caddyfile.public-local
```

如果想让它在后台运行：

```bash
caddy start --config .dev/Caddyfile.public-local
```

本机验证：

```bash
curl http://127.0.0.1:18080/api/health
```

浏览器打开：

```text
http://127.0.0.1:18080
```

确认页面和 API 都正常后，再继续下一步。

## 4. 阿里云配置 Nginx

登录服务器：

```bash
ssh root@47.95.205.124
```

创建或编辑 Nginx 配置：

```bash
vim /etc/nginx/conf.d/chat-quant.conf
```

写入：

```nginx
server {
    listen 80;
    server_name chatq.nanbende.com;

    location / {
        proxy_pass http://127.0.0.1:18080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        client_max_body_size 50m;
    }
}
```

验证并重载 Nginx：

```bash
nginx -t
systemctl reload nginx
```

此时如果还没有建立 SSH 隧道，访问域名可能会显示 `502 Bad Gateway`，这是正常的。

## 5. 本机建立 SSH 反向隧道

回到你的本机，在项目根目录或任意目录执行：

```bash
ssh -i /Users/huyufei/Documents/hyf/doc/aliyun/ecs-key.pem \
  -N \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -R 127.0.0.1:18080:127.0.0.1:18080 \
  root@47.95.205.124
```

这条命令需要保持运行。

含义：

- 阿里云服务器上的 `127.0.0.1:18080`
- 转发到你本机的 `127.0.0.1:18080`
- 服务器上的 Nginx 再把公网请求代理给它

建立成功后，在阿里云服务器上可以验证：

```bash
curl http://127.0.0.1:18080/api/health
```

然后在浏览器访问：

```text
http://chatq.nanbende.com
```

## 6. 配置 HTTPS

如果服务器已经安装 Certbot，可以在阿里云服务器执行：

```bash
certbot --nginx -d chatq.nanbende.com
```

按提示完成后，Certbot 会自动修改 Nginx 配置并启用 HTTPS。

验证：

```bash
nginx -t
systemctl reload nginx
```

之后好友访问：

```text
https://chatq.nanbende.com
```

如果 Certbot 提示无法验证域名，检查：

- 域名 A 记录是否指向阿里云服务器公网 IP。
- 阿里云安全组是否放行 `80` 和 `443`。
- 服务器防火墙是否放行 HTTP/HTTPS。

## 7. 建议加访问密码

当前项目没有完整登录系统，设置页可能包含模型 API Key、数据源 token、运行配置等敏感信息。给好友试用时，不建议裸露到公网。

推荐直接用脚本开启阿里云 Nginx Basic Auth：

```bash
printf '%s\n' '换成你的访问密码' > deploy/public-auth.password
PUBLIC_AUTH_ENABLED=true PUBLIC_AUTH_USER=friend bash deploy/3_setup_local_tunnel_server.sh
```

之后再启动公网隧道：

```bash
PUBLIC_AUTH_USER=friend bash deploy/4_start_local_tunnel.sh
```

脚本会在服务器 `/etc/nginx/conf.d/chat-quant.conf` 的公网代理 `location /` 中加入：

```nginx
auth_basic "Chat-Quant";
auth_basic_user_file /etc/nginx/chat-quant.htpasswd;
```

如果你想手工验证公网认证是否生效：

```bash
curl -i https://chatq.nanbende.com/api/health
curl -u friend:你的访问密码 https://chatq.nanbende.com/api/health
```

第一条应该返回 `401 Unauthorized`，第二条应该返回 API 健康检查结果。

## 8. 让隧道更稳定

普通 `ssh -N -R ...` 适合手动试用。如果要长期给好友访问，建议使用 `autossh` 自动重连。

macOS 安装：

```bash
brew install autossh
```

启动：

```bash
autossh -M 0 -N \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -R 127.0.0.1:18080:127.0.0.1:18080 \
  root@47.95.205.124
```

如果本机休眠、断网、重启，隧道仍然会中断。恢复后需要重新启动 Chat-Quant、Caddy 和隧道。

## 9. 日常启动顺序

每次准备给好友使用时，优先使用脚本：

```bash
bash deploy/4_start_local_tunnel.sh
```

启动脚本会逐项检查：

- Chat-Quant 本地 dev 服务。
- 前端静态构建。
- 本机 Caddy 统一入口。
- SSH 反向隧道。

已经启动且健康的后台进程会跳过；PID 文件丢失但进程仍在时，脚本会尽量重新记录 PID。

## 10. 停止访问

停止公网访问和本机相关后台进程：

```bash
bash deploy/5_stop_local_tunnel.sh
```

停止脚本会按顺序停止 SSH 反向隧道、本机 Caddy，以及 `npm run dev:web-start` 启动的本地 Web/API 服务。

## 11. 常见问题

### 访问域名显示 502

在阿里云服务器检查隧道端口：

```bash
curl http://127.0.0.1:18080/api/health
```

如果失败，说明 SSH 反向隧道没有连上，或本机 `127.0.0.1:18080` 没有服务。

### 页面能打开但接口失败

本机检查 API：

```bash
curl http://127.0.0.1:12345/api/health
curl http://127.0.0.1:18080/api/health
```

第一个失败，说明 FastAPI 没启动。第二个失败，说明 Caddy 的 `/api/*` 反代配置有问题。

### 修改前端后好友看不到变化

重新构建前端：

```bash
npm --prefix apps/web run build
```

然后刷新浏览器。若浏览器缓存较重，可让好友强制刷新。

### SSH 隧道启动时报端口被占用

在阿里云服务器检查：

```bash
lsof -i tcp:18080
```

如果已有旧的 SSH 隧道进程，结束旧进程后重新连接。

### HTTPS 证书申请失败

检查：

- 域名是否解析到阿里云公网 IP。
- 阿里云安全组是否开放 `80`。
- Nginx 是否能正常响应 HTTP。

## 与 deploy 目录的关系

仓库里的 `deploy/nginx.conf` 和 `deploy/2_deploy.sh` 是给“项目完整部署在阿里云服务器”的模式准备的。

在那个模式下，Nginx 配置最终会写入：

```text
/etc/nginx/conf.d/chat-quant.conf
```

但本文方案中，项目不部署到阿里云服务器，阿里云只代理 SSH 隧道。因此服务器上的 Nginx 配置应使用本文的 `proxy_pass http://127.0.0.1:18080;`，不要直接照搬 `deploy/nginx.conf`。
