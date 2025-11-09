# CLAUDE.md

这个文件为在此存储库中工作的 Claude Code (claude.ai/code) 提供指导。

## 项目概述

Claudable 是一个基于 Next.js 的 Web 应用构建器，它将 Claude Code 的高级 AI 代理能力与 Lovable 的简单直观应用构建体验相结合。用户只需描述应用想法，Claudable 就能即时生成代码并显示工作应用的实时预览。

## 架构概述

Claudable 是一个 monorepo 结构的项目，包含：

### 前端 (`apps/web/`)
- **技术栈**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **主要特性**: 
  - 实时聊天界面与多个 AI 代理交互
  - 项目管理和设置界面
  - 与 GitHub/Vercel/Supabase 的服务集成
  - 深色模式支持和响应式设计

### 后端 (`apps/api/`)
- **技术栈**: FastAPI, SQLAlchemy, Python 3.10+
- **核心功能**:
  - WebSocket 实时通信
  - 多 CLI 代理适配器 (Claude Code, Cursor CLI, Codex CLI, Gemini CLI, Qwen Code)
  - 项目生命周期管理
  - GitHub、Vercel、Supabase 服务集成
  - SQLite (开发) / PostgreSQL (生产) 数据库

### 脚本和工具 (`scripts/`)
- 自动环境设置和端口检测
- Python 虚拟环境管理
- 数据库备份和重置工具

## 开发命令

### 主要命令
```bash
# 启动完整开发环境 (前端 + 后端)
npm run dev

# 分别启动服务
npm run dev:web    # 仅前端 (默认 http://localhost:3000)
npm run dev:api    # 仅后端 (默认 http://localhost:8080)

# 项目设置
npm install        # 完整安装，包括 Python 依赖和环境配置
npm run setup      # 等同于 npm install
npm run clean      # 清理所有依赖和虚拟环境
```

### 数据库管理
```bash
npm run db:backup  # 创建 SQLite 数据库备份
npm run db:reset   # 重置数据库到初始状态 (危险操作!)
```

### 前端开发
```bash
cd apps/web
npm run build      # 构建生产版本
npm run start      # 启动生产服务器
```

### 类型检查
项目包含 TypeScript 类型检查脚本：
```bash
# 手动运行类型检查 (位于 scripts/type_check.sh)
npx tsc --noEmit
```

## 关键架构模式

### CLI 适配器模式
- 统一接口支持多个 AI 代理 (Claude Code, Cursor CLI, Codex CLI, Gemini CLI, Qwen Code)
- 每个适配器位于 `apps/api/app/services/cli/adapters/`
- 通过 `CLIManager` 和 `UnifiedManager` 统一管理

### WebSocket 通信
- 实时双向通信支持聊天和项目更新
- WebSocket 管理器位于 `apps/api/app/core/websocket/manager.py`
- 前端通过 React hooks 管理 WebSocket 连接

### 服务导向架构
后端按功能模块组织：
- `api/projects/` - 项目 CRUD 操作
- `api/chat/` - 聊天和 AI 交互
- `api/github.py` - GitHub 集成
- `api/vercel.py` - Vercel 部署
- `services/` - 核心业务逻辑

## 环境配置

### 自动配置
- 端口自动检测：如果默认端口被占用，自动分配下一个可用端口
- 环境文件自动生成 (`.env`)
- Python 虚拟环境自动创建和激活

### 手动配置 (如需要)
```bash
# 前端环境设置
cd apps/web
npm install

# 后端环境设置
cd apps/api
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 数据库

### 开发环境
- SQLite 数据库位于 `data/cc.db`
- 首次运行时自动创建
- 支持自动迁移

### 生产环境
- 支持 PostgreSQL
- 可通过 Supabase 集成配置

## 集成服务

### GitHub
- 自动仓库创建和管理
- 代码提交和推送
- 需要 Personal Access Token

### Vercel
- 一键部署到 Vercel
- 自动 CI/CD 设置
- 需要 Vercel API Token

### Supabase
- PostgreSQL 数据库
- 认证系统
- 需要项目 URL 和 API Keys

## 开发最佳实践

### 代码组织
- 前端组件位于 `apps/web/components/`
- 后端模型位于 `apps/api/app/models/`
- 共享类型定义使用 TypeScript interfaces

### 样式系统
- 使用 Tailwind CSS 进行样式管理
- 支持深色模式 (`darkMode: 'class'`)
- 自定义主题颜色和 bolt 品牌色彩

### 错误处理
- 后端使用 FastAPI 异常处理
- 前端使用 React Error Boundaries
- WebSocket 连接自动重连机制

## 故障排除

### 端口占用
应用会自动检测并使用可用端口，检查 `.env` 文件查看分配的端口。

### 权限错误
不要使用 `sudo` 运行 Claude Code。如果在 WSL 中遇到权限问题：
```bash
sudo chown -R $(whoami):$(whoami) ~/Claudable
```

### 依赖冲突
```bash
npm run clean  # 清理所有依赖
npm install    # 重新安装
```

## 重要文件路径

- `package.json` - 主要脚本和工作区配置
- `apps/web/package.json` - 前端依赖和脚本
- `apps/api/requirements.txt` - Python 依赖
- `apps/api/app/main.py` - FastAPI 应用入口
- `apps/web/app/layout.tsx` - Next.js 根布局
- `scripts/` - 各种自动化脚本