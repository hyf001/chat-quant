# Chat-Quant

基于 `docs/概要设计说明书.md` 搭建的前后端脚手架。

## 开发启动

```bash
uv sync --project apps/api
uv run --project apps/api uvicorn app.main:app --reload --app-dir apps/api
```

```bash
npm install --prefix apps/web
npm --prefix apps/web run dev
```

后端健康检查：`GET /api/health`
