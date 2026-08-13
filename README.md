# Chat-Quant

Chat-Quant 是一个基于自然语言对话的股票分析与策略验证工作台。项目将前端工作台、FastAPI 后端、Claude Agent SDK、AKShare 数据源、策略资产管理和 Backtrader 回测能力组合在一起，用于支持股票查询、策略生成、策略版本沉淀和回测结果复盘。

> 当前项目处于本地开发阶段，功能与产品边界可参考 `docs/prd.md`、`docs/概要设计说明书.md` 和各模块详细设计文档。

## 核心能力

- 对话式股票分析：通过 Web 工作台向后端发起会话请求，并由 Agent 运行时处理分析任务。
- 策略资产管理：支持策略创建、版本切换、归档、软删除和元数据维护。
- 策略回测：基于 Backtrader 执行回测，保存回测记录和风险指标。
- 本地项目上下文：通过项目目录解析业务项目，便于把策略和回测记录沉淀到具体工作空间。
- 多端入口：提供 Web 开发入口和 Electron 桌面端打包入口。

## 技术栈

- Monorepo：根目录统一管理脚本，Python 使用 `uv` workspace。
- API：FastAPI、SQLAlchemy、aiosqlite、Pydantic。
- Agent：`claude-agent-sdk`，插件目录位于 `plugin/`。
- 数据与回测：AKShare、pandas、Backtrader。
- Web：React 19、Vite、TypeScript、Tailwind CSS、ECharts。
- Desktop：Electron、electron-builder，复用 Web 构建产物。

## 目录结构

```text
.
├── apps/
│   ├── api/              # FastAPI 后端应用
│   ├── web/              # Vite + React 前端工作台
│   └── desktop/          # Electron 桌面端
├── cli/                  # chatq-strategy 策略管理 CLI
├── data/                 # 本地 SQLite 数据库与项目数据
├── deploy/               # 服务器部署脚本与 Nginx 配置
├── docs/                 # PRD、概要设计、详细设计和数据字典
├── plugin/               # Agent SDK 插件与技能
├── scripts/              # 本地开发启动/停止脚本
└── tests/                # 跨模块测试
```

## 环境要求

- Python `>=3.12`
- Node.js `>=20`
- `uv`
- `npm`

首次拉取后安装依赖：

```bash
uv sync --project apps/api --all-groups
npm --prefix apps/web install
npm --prefix apps/desktop install
```

## 本地配置

所有本地运行配置都写在根目录 `config.json`：

```json
{
  "database_path": "data/chat-quant.db",
  "api_host": "127.0.0.1",
  "api_port": 12345,
  "web_host": "127.0.0.1",
  "web_port": 12346
}
```

系统配置、Agent 参数和模型供应商配置保存在 SQLite，可在 Web 设置页维护。

Web 开发服务、FastAPI 后端和桌面端 sidecar 都只读取这个配置文件里的同名配置项。

## 开发启动

启动 Web 开发环境（API + Vite）：

```bash
npm run dev:web-start
```

默认地址：

- API：`http://127.0.0.1:12345`
- Web：`http://127.0.0.1:12346`
- 健康检查：`http://127.0.0.1:12345/api/health`

启动脚本会把进程号和日志写入 `.dev/`：

```bash
tail -f .dev/logs/web-api.log
tail -f .dev/logs/web.log
```

停止本地服务：

```bash
npm run dev:web-stop
```

启动桌面端开发环境：

```bash
npm run dev:desktop-start
```

桌面端日志位于 `.dev/logs/desktop.log`，停止命令为：

```bash
npm run dev:desktop-stop
```

如需改端口，编辑 `config.json` 中的 `api_port` 和 `web_port`，Web 版和桌面版会使用同一组配置。


## 常用 API

所有业务接口默认挂在 `/api` 前缀下。

- `GET /api/health`：健康检查。
- `/api/chat`：对话请求。
- `/api/chat-sessions`：会话管理。
- `/api/projects`：本地项目解析和项目管理。
- `/api/strategies`：策略资产与版本管理。
- `/api/backtests`：回测记录查询。
- `/api/model-providers`：模型供应商配置。
- `/api/config`：运行配置。
- `/api/runtime`：运行时信息。

## 策略 CLI

策略 CLI 位于 `cli/chatq_strategy.py`，通过业务 API 操作策略和回测。开发环境下建议显式指定 API 地址：

```bash
export CHATQ_API_BASE_URL=http://127.0.0.1:12345
```

常用命令：

```bash
uv run python -m cli.chatq_strategy list
uv run python -m cli.chatq_strategy protocol
uv run python -m cli.chatq_strategy create --name "双均线策略" --source-file path/to/strategy.py
uv run python -m cli.chatq_strategy versions <strategy_id>
uv run python -m cli.chatq_strategy backtest <strategy_id> --market CN --symbol 000001 --start 2024-01-01 --end 2024-12-31
```

CLI 会优先读取 `CHATQ_API_BASE_URL` 或 `CHATQ_API_BASE`；如果没有配置，会尝试读取桌面端运行时文件，最后回退到 `http://127.0.0.1:12345/api`。

## 测试与检查

后端测试：

```bash
uv run pytest
```

后端 lint：

```bash
npm run lint:api
```

前端类型检查：

```bash
npm run lint:web
```

前端构建：

```bash
npm --prefix apps/web run build
```

## 桌面端

桌面端基于 Electron 和 electron-builder，打包时会先完成三件事：

1. 使用 PyInstaller 把 FastAPI 后端打成 API sidecar。
2. 构建 `apps/web` 前端静态资源。
3. 由 electron-builder 生成 macOS 桌面端产物。

打包前先安装依赖：

```bash
uv sync --project apps/api --all-groups
npm --prefix apps/web install
npm --prefix apps/desktop install
```

开发模式会先构建 Web，再启动 Electron：

```bash
npm run dev:desktop-start
```

如果只是本地验证 Electron 应用结构，可以打包目录版本：

```bash
npm run pack:desktop
```

该命令会生成可直接运行的 `.app` 目录，产物位于 `apps/desktop/dist/`，但不会生成用于分发的安装包。

打包 macOS 分发版本需要在 macOS 上执行：

```bash
npm --prefix apps/desktop run dist
```

执行成功后，macOS 产物会输出到 `apps/desktop/dist/`，通常包括：

- `Chat Quant-<version>-<arch>.dmg`：给用户安装的磁盘镜像。
- `Chat Quant-<version>-<arch>-mac.zip`：压缩版应用包。
- `.blockmap`：electron-builder 生成的增量更新元数据。

Apple Silicon 机器默认会生成 `arm64` 产物；Intel Mac 默认会生成 `x64` 产物。API sidecar 由 PyInstaller 在本机环境构建，建议在目标架构对应的 Mac 上打包。

当前项目未配置 macOS 代码签名和公证，生成的 DMG/ZIP 适合本地测试或内部试用。正式对外分发前，需要补充 Apple Developer 证书、签名和公证配置，否则用户首次打开时可能会被 Gatekeeper 拦截。

桌面端 API sidecar 构建脚本位于 `apps/desktop/scripts/build-api-sidecar.sh`，sidecar 产物目录为 `apps/desktop/sidecars/`。

## 部署

服务器部署说明位于 `deploy/README.md`。根目录可执行：

```bash
bash deploy/0_remote_deploy.sh
```

部署脚本会在服务器上拉取仓库、安装运行环境、构建前后端、写入 `config.json`、配置 Nginx 与 HTTPS，并启动系统服务。

## 相关文档

- `docs/prd.md`：产品需求文档。
- `docs/概要设计说明书.md`：系统概要设计。
- `docs/详细设计-M1-会话与消息模块.md`：会话与消息模块。
- `docs/详细设计-M3-代码产物模块.md`：代码产物模块。
- `docs/详细设计-M5-策略资产模块.md`：策略资产模块。
- `docs/详细设计-M6-回测与风险结果模块.md`：回测与风险结果模块。
- `docs/akshare/数据字典/README.md`：AKShare 数据字典。
