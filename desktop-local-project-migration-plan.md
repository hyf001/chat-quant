# Desktop Local Project Migration Plan

## 背景与目标

当前版本已转向本地桌面程序，原有偏服务端/多用户的模型需要收敛为单机本地项目模型。

目标：

1. 彻底去掉用户概念，不再需要 `user_id`、`X-User-Id`、默认用户、用户隔离和用户权限判断。
2. Project 与本地路径一一对应，一个本地目录只能对应一个 project。
3. Claude Agent SDK 的运行目录、历史读取目录和 project 本地路径保持一致。
4. 构建策略、回测、会话等业务资产仍然保存 `project_id`，但 `project_id` 由平台内部根据本地路径解析，不再要求用户或 skill 手动传。
5. 不再保留 `PROJECT_HOME` 或“项目根目录池”的概念。项目目录由用户选择；首次安装或没有任何 project 时，引导用户创建或打开一个 project。

## 核心原则

### Project 身份

`project.local_path` 是 project 的真实身份来源。

建议：

```text
project.id = "project_" + hash(canonical_abs_path)
project.local_path = canonical_abs_path
```

约束：

- `projects.local_path` 必须唯一。
- `local_path` 必须是规范化后的绝对路径。
- 同一路径重复打开时返回同一个 project。
- 删除 project 只表示从应用项目列表移除，不删除本地目录。
- 应用首次安装时，如果没有任何 project，不自动创建默认 project，而是进入空状态引导。
- 用户通过“新建 project”或“打开本地文件夹”完成第一个 project 注册。

### Claude Agent SDK 目录关系

同一个 project 下，这几个值必须完全一致：

```text
project.local_path
  = AgentExecutionCommand.project_dir
  = ClaudeAgentOptions.cwd
  = get_session_messages(..., directory=...)
  = get_session_info(..., directory=...)
```

这不是实现细节，而是功能正确性的基础。Claude Agent SDK 的 `cwd` 会影响：

- Bash/Read/Write 等工具的默认工作目录。
- Claude Code project settings、`.claude/`、skills/commands 的加载范围。
- SDK session resume 和 transcript 的 project directory 分区。
- Agent 看到的 `pwd`。

本地文档依据：

- `docs/claude-agent-sdk/python.md` 中 `ClaudeAgentOptions.cwd` 的说明是 `Current working directory`。
- `docs/claude-agent-sdk/claude-code-features.md` 说明 `<cwd>` 是通过 `cwd` option 传入的工作目录，project settings、`.claude/` 等 project-level inputs 都按 `<cwd>` 解析。
- `docs/claude-agent-sdk/typescript.md` 的 Bash 工具说明写明 working directory 会在命令之间持久。

因此，只要后端启动 SDK 时设置：

```text
ClaudeAgentOptions.cwd = project.local_path
```

Agent 通过 Bash 执行 CLI 时，CLI 的 `os.getcwd()` 就应当是当前 project path。CLI 不需要再读取另一个环境变量来判断当前 project。

不能再使用：

```text
PROJECT_HOME / safe_project_dir_segment(project_id)
```

作为运行目录或 SDK history directory。

`PROJECT_HOME`、`default_project_id` 和任何通过 project id 推导目录的逻辑都应删除。

## 数据库改造

### projects

调整为：

```text
id
local_path
name
description
created_at
updated_at
deleted_at
```

删除：

```text
user_id
```

新增：

```text
UNIQUE(local_path)
INDEX(updated_at)
INDEX(deleted_at)
```

### chat_sessions

保留：

```text
project_id
```

删除：

```text
user_id
```

调整：

- `project_id` 语义改为指向本地 project。
- 读取 SDK messages/info 时，必须通过 `project_id -> project.local_path` 得到 directory。
- `sdk_project_key` 如果只用于旧的 project directory 分区，应评估废弃；如果保留，应与 `local_path` 对齐。

### strategies / strategy_backtests

保留：

```text
project_id
```

删除：

```text
user_id
```

调整：

- 策略列表按 `project_id` 过滤。
- 策略创建需要 `project_id`，但由 API/CLI 内部解析，不由用户或 skill 直接传命令行参数。
- 回测记录继续归属到 `project_id`。

## 后端 API 改造

### 删除用户依赖

删除或废弃：

```text
get_user_id
UserId
X-User-Id
default_user_id
ChatSessionAccessError
ProjectAccessError
```

所有 API 不再读取用户 header，不再做用户隔离判断。

### Project API

建议新增/调整：

```text
GET  /api/projects
GET  /api/projects/{project_id}
POST /api/projects/open
POST /api/projects/create
POST /api/projects/resolve
PATCH /api/projects/{project_id}
DELETE /api/projects/{project_id}
```

`POST /api/projects/open`

```json
{
  "local_path": "/Users/me/quant/demo"
}
```

行为：

- 规范化路径。
- 校验目录存在且可读写。
- 已存在则返回已有 project。
- 不存在则按产品决策返回错误，或由 create 接口负责创建。

`POST /api/projects/create`

```json
{
  "local_path": "/Users/me/quant/demo"
}
```

行为：

- 创建本地目录。
- 注册 project。
- 返回 project。

`POST /api/projects/resolve`

```json
{
  "local_path": "/Users/me/quant/demo"
}
```

行为：

- 用于 CLI 根据当前目录解析内部 `project_id`。
- 找到则返回 project。
- 找不到时可返回 404，或按产品决策自动注册。建议初期自动注册，桌面体验更顺。

### 首次安装空状态

首次安装或首次启动时，如果 `projects` 表为空，应用进入引导状态。

要求：

- 不自动创建默认 project。
- 引导用户选择“新建 project”或“打开本地文件夹”。
- 新建 project 时由用户选择目录位置和名称，应用创建该目录并注册 project。
- 打开本地文件夹时，应用注册用户选择的目录。
- 两条路径都使用同一套 `projects.local_path` 模型，不引入 `PROJECT_HOME`、默认父目录或路径推导规则。

### Chat API

创建/发送消息时仍需要 `project_id`：

```json
{
  "message": "...",
  "project_id": "project_xxx",
  "chat_session_id": null
}
```

后端流程：

```text
project_id
-> 查询 project.local_path
-> AgentExecutionCommand.project_dir = project.local_path
-> ClaudeAgentOptions.cwd = project.local_path
```

历史读取：

```text
chat_session_id
-> chat_session.project_id
-> project.local_path
-> get_session_messages(directory=project.local_path)
```

### Strategy API

API payload 应保留 `project_id`：

```json
{
  "project_id": "project_xxx",
  "name": "策略名称",
  "source_code": "...",
  "strategy_mode": "single_symbol",
  "risk_notes": []
}
```

但去掉：

```json
{
  "user_id": "..."
}
```

列表接口建议显式传 project：

```text
GET /api/strategies?project_id=project_xxx
```

或保留当前 `/api/strategies`，但必须有明确的当前 project 上下文，不再靠 `X-Project-Id` 默认值。

## Agent Runtime 改造

### AgentExecutionCommand

当前包含：

```text
user_id
project_id
project_dir
```

建议改为：

```text
project_id
project_dir
chat_session_id
user_message_id
context
sdk_session_id
should_finalize_initial_title
request_id
deadline_seconds
user_prompt
```

说明：

- `user_id` 删除。
- `project_id` 可作为后端内部关联字段保留，用于 ChatSession/Strategy/Backtest 落库和会话索引同步。
- `project_id` 不传给 Claude Agent SDK，不注入 system prompt，不写入 env，不要求 skill/CLI 手动传。
- `project_dir` 必须是 canonical absolute path，并且必须来自 `project.local_path`。
- `project_dir` 是 Agent Runtime 真正需要的 project 上下文；构建 SDK options 时只用它设置 `ClaudeAgentOptions.cwd`。
- `should_finalize_initial_title` 保留，因为当前 `_sync_chat_session_index` 依赖它决定首轮回答后是否同步标题。

### Runtime 调用边界

`ChatApplicationService` 负责解析 project：

```text
request.project_id
-> ProjectService require project
-> project.local_path
-> AgentExecutionCommand.project_dir
```

`ClaudeAgentRuntime` 只负责执行：

```text
AgentExecutionCommand.project_dir
-> ClaudeAgentOptions.cwd
```

Runtime 不再根据 `project_id` 推导路径，也不访问 `PROJECT_HOME`。

当前 `Path(command.project_dir).mkdir(...)` 应移出 chat 执行链路：

- 打开 project 时目录必须已存在。
- 新建 project 时由 Project API 创建目录。
- Agent Runtime 不应在发送消息时静默创建任意目录。

当前 `runtime_guards.py` 中通过字符串判断 `..` 的逻辑也应替换：

- project path 在 ProjectService 中完成 canonicalize 和读写校验。
- Runtime guard 只做轻量断言，例如 `project_dir` 非空、是绝对路径、目录存在。
- 不再用 `project_dir.split("/")` 这类字符串规则判断本地路径安全。

### System Prompt

删除：

```text
当前身份上下文：
- user_id: ...
- project_id: ...
```

替换为：

```text
当前项目上下文：
- 当前工作目录就是本地项目目录。
- 所有生成文件、策略源码和回测产物都应放在当前项目目录或平台指定输出目录内。
```

不建议默认把完整绝对路径写进 prompt。SDK `cwd` 已经提供运行上下文；Agent 需要时可以执行 `pwd`。

`build_system_prompt` 签名同步调整：

```text
build_system_prompt(context)
```

删除参数：

```text
user_id
project_id
```

### SDK env

建议注入：

```text
CHATQ_API_BASE_URL
```

不再注入：

```text
CHATQ_USER_ID
CHATQ_PROJECT_ID
CHATQ_PROJECT_PATH
```

CLI 的 project path 只来自进程当前工作目录。后端通过 `ClaudeAgentOptions.cwd = project.local_path` 保证 Agent 执行 Bash/CLI 时 `pwd` 就是当前 project path。

## CLI 与 Skill 改造

### CLI 用户界面

删除命令行参数：

```text
--user-id
--project-id
```

用户/skill 执行：

```bash
uv run python -m cli.chatq_strategy create \
  --name "策略名称" \
  --source-file ./strategy.py
```

CLI 内部解析当前 project：

```text
1. 读取 os.getcwd()。
2. 规范化为 canonical absolute path。
3. 调 POST /api/projects/resolve。
4. 得到 project_id。
5. 调策略 API 时在 request body 内带 project_id。
```

因此：

```text
API request payload: 需要 project_id
CLI user-facing args: 不需要 --project-id
Skill 文档: 不要求传 project id
```

### Skill 文档

更新 `plugin/skills/strategy_management/references/strategy-management.md`：

- 删除 `--user-id "$USER_ID"`。
- 删除 `--project-id "$PROJECT_ID"`。
- 明确 CLI 只从当前 `pwd` 解析 project。
- 不要求 Agent 知道内部 project id。
- Skill 执行 CLI 前不需要 `cd`，因为 Claude Agent SDK 已由后端设置 `cwd = project.local_path`；如 skill 明确改变过目录，则必须回到原始 `pwd` 后再执行策略 CLI。

旧描述：

```bash
uv run python -m cli.chatq_strategy list \
  --user-id "$USER_ID" \
  --project-id "$PROJECT_ID"
```

新描述：

```bash
uv run python -m cli.chatq_strategy list
```

策略创建同理。

## Electron 与前端改造

### Electron

在 preload/main 中增加本地目录选择能力：

```text
chatqDesktop.selectProjectDirectory()
chatqDesktop.createProjectDirectory()
```

主进程通过 `dialog.showOpenDialog` 选择目录，把路径返回给前端。

### 前端 API client

删除：

```text
API_USER_ID
VITE_CHATQ_USER_ID
X-User-Id
API_PROJECT_ID
VITE_CHATQ_PROJECT_ID
X-Project-Id
```

调整：

- 当前 project 由前端状态决定。
- 发送消息、策略列表、创建策略、回测时显式使用 active project。

### 前端类型

删除：

```text
Project.user_id
ChatSession.user_id
```

新增：

```text
Project.local_path
```

### 前端交互

首次进入：

```text
无 project
-> 显示空状态引导
-> 用户选择打开本地文件夹或新建 project
-> 用户选择目录
-> 调 /api/projects/open 或 /api/projects/create
-> 设置 activeProjectId
```

最近项目：

- 来自 `/api/projects`。
- 删除项目文案为“从列表移除”。
- Header 显示 project name 和 local path。

## 迁移策略

如果需要保留旧数据：

1. 给 `projects` 加 `local_path`。
2. 对旧 project 回填：

```text
local_path = 旧版本实际创建过的项目工作目录
```

3. 如果旧版本使用过 `PROJECT_HOME / safe_project_dir_segment(project.id)`，迁移脚本只作为一次性兼容逻辑读取旧配置，不把 `PROJECT_HOME` 保留为新版本概念。
4. 创建目录，或只记录路径。
5. 为 `local_path` 建唯一索引。
6. 删除或忽略各表 `user_id`。
7. 重建索引：

```text
projects(local_path)
projects(updated_at)
chat_sessions(project_id, updated_at)
strategies(project_id, updated_at)
```

如果没有正式数据需要保留，可选择一次性 reset 本地 SQLite schema，成本更低。

## 测试计划

### 后端

新增/更新测试：

- 同一路径重复 open 返回同一个 project。
- 不同路径返回不同 project。
- project `local_path` 被 canonicalize。
- 不存在或不可写路径返回明确错误。
- 创建 chat message 时，`AgentExecutionCommand.project_dir == project.local_path`。
- Claude SDK `options.cwd == project.local_path`。
- `get_session_messages(directory=project.local_path)`。
- `get_session_info(directory=project.local_path)`。
- system prompt 不包含 `user_id`。
- system prompt 不包含内部 `project_id`。
- 策略创建 API 保存正确 `project_id`。
- CLI 无 `--project-id` 时能通过当前 cwd 创建策略。

删除/改写测试：

- 用户 A 不能读取用户 B 会话。
- 按 user_id 过滤会话。
- 按 user_id 过滤项目。
- system prompt 注入 user/project id。

### 前端

新增/更新测试：

- 无项目时显示打开/新建目录入口。
- 选择目录后注册并激活 project。
- 请求不再发送 `X-User-Id`。
- 发送消息时使用 active project id。
- Header 显示 local path。

### CLI/Skill

新增/更新测试：

- `chatq_strategy create` 不需要 `--user-id` 和 `--project-id`。
- CLI 只使用 `os.getcwd()` 作为 project path 来源。
- Agent Runtime 启动 SDK 时设置 `ClaudeAgentOptions.cwd = project.local_path`。
- 在 fake SDK Bash/CLI 测试里确认 CLI 看到的 cwd 是 `project.local_path`。
- CLI 调 `/api/projects/resolve` 后，把返回的 `project_id` 写入策略创建 payload。

## 建议实施顺序

1. 实现 project path resolver 和 `projects.local_path` 数据模型。
2. 增加 `/api/projects/open`、`/api/projects/create`、`/api/projects/resolve`。
3. 移除后端用户依赖和相关权限判断。
4. 改 ChatApplicationService，让 `project_dir` 来自 `project.local_path`。
5. 改 SDK history 读取逻辑，统一使用 `project.local_path`。
6. 改 Strategy/Backtest service，删除 `user_id`，保留 `project_id`。
7. 改 CLI，删除 `--user-id`/`--project-id`，只用当前 cwd resolve project。
8. 改 skill 文档，删除手动传 project id 的说明。
9. 改前端 API client、类型和 project 打开流程。
10. 更新测试并跑完整后端/前端验证。

## 最终目标状态

用户和 Agent 看到的是：

```text
打开一个本地文件夹
在这个文件夹里聊天、写策略、跑回测
```

平台内部维护的是：

```text
local_path -> project_id
project_id -> chat sessions / strategies / backtests
```

Claude Agent SDK 使用的是：

```text
cwd = project.local_path
directory = project.local_path
```

这样既保留数据库层清晰的 project 归属，又让桌面版行为符合用户直觉。
