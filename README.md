# Chat-Quant

基于 `docs/概要设计说明书.md` 搭建的前后端脚手架。

## 开发启动

```bash
npm run dev:start
```

```bash
npm run dev:stop
```

API 默认运行在 `http://127.0.0.1:8000`，Web 默认运行在 `http://127.0.0.1:5173`。
后端健康检查：`GET /api/health`

## 运行配置

后端可在 `.env` 中配置默认身份和 Agent 运行参数：

```bash
CHATQ_DEFAULT_USER_ID=
CHATQ_DEFAULT_PROJECT_ID=
ANTHROPIC_MODEL=
ANTHROPIC_BASE_URL=
ANTHROPIC_AUTH_TOKEN=
```

前端可在 `apps/web/.env.local` 中配置请求上下文：

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_CHATQ_USER_ID=
VITE_CHATQ_PROJECT_ID=
```
