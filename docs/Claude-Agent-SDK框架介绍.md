# Claude Agent SDK 框架介绍

## 1. 文档目的

本文用于统一 Chat-Quant 的智能体集成口径。系统已选用 `claude-agent-sdk` 作为现成智能体框架，因此后端不再自建 Agent loop、工具调度器、上下文执行循环或复杂任务编排引擎。Chat-Quant 的职责是把股票查询、代码产物、Python 执行、策略资产、回测结果等平台能力封装为 `chatq ...` 内部 CLI 命令，让 Agent 通过 SDK 自带 `Bash` 工具调用，并消费 SDK 输出的消息、工具调用和结果消息。

官方文档参考：

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Work with sessions](https://code.claude.com/docs/en/agent-sdk/sessions)
- [Persist sessions to external storage](https://code.claude.com/docs/en/agent-sdk/session-storage)
- [Agent Skills in the SDK](https://code.claude.com/docs/en/agent-sdk/skills)
- [Stream responses in real-time](https://code.claude.com/docs/en/agent-sdk/streaming-output)
- [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python)
- [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [Intercept and control agent behavior with hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features)

### 1.1 新增官方文档补充要点

| 官方文档 | 新增关键信息 | 对 Chat-Quant 的设计影响 |
|---|---|---|
| Sessions | SDK session 支持 resume，并可通过 SDK 读取历史 messages | ChatSession 只保存 `sdk_session_id` 和产品元数据；历史对话从 SDK session 读取 |
| Session storage | SDK 支持外部 SessionStore，用于把 transcript 持久化到共享存储 | 生产环境优先配置 SDK SessionStore；M1 不再复制一份 SDK message 表 |
| Agent Skills in the SDK | Skills 是 `.claude/skills/.../SKILL.md` 文件系统能力，由 SDK 发现和加载；`skills` option 只做可见性过滤 | M2 只配置 `skills`、`setting_sources`、`cwd`，不自建 skill loader，不手动拼接技能内容 |
| Streaming output | 开启 `include_partial_messages=True` 后会收到 `StreamEvent`；完整消息仍会以 `AssistantMessage`、`ResultMessage` 形式到达 | 前端实时输出用 `StreamEvent`；历史回放和资产定位仍使用完整 SDK messages |
| Python SDK reference | Python 类型包含 `StreamEvent`、`AssistantMessage`、`ResultMessage` 等 | M2 的 stream relay 应透传 SDK 原生类型，不定义平台事件协议 |

实现备注：

1. `skills` 是 SDK 原生 option。未指定时按 SDK 默认发现；指定列表时只控制哪些已发现 skills 可用。
2. Skills 通过 `setting_sources` 和 `cwd` 影响发现范围。生产环境应显式设置，避免加载不可控的本机配置。
3. `include_partial_messages=True` 只影响当前 turn 的实时 UI；它产生的 `StreamEvent` 是 raw streaming event，不应被保存成业务消息表。
4. SessionStore 是 SDK transcript 的持久层，条目按 SDK opaque JSON 保存。业务侧只保存 AssetLink 与 SDK session/message/tool_use 的引用。
5. Bash 内部 `chatq ...` CLI 是 command policy 管控的运行能力，不是 Chat/Agent API。

## 2. SDK 核心能力

`claude-agent-sdk` 把 Claude Code 的 Agent 能力作为 Python/TypeScript 库提供。它内置：

| 能力 | 说明 | 对 Chat-Quant 的意义 |
|---|---|---|
| Agent loop | SDK 负责多轮推理、工具调用、工具结果回填和最终结果生成 | 系统不实现自己的 `while tool_use` 循环 |
| 内置工具 | `Read`、`Write`、`Edit`、`Bash`、`Glob`、`Grep`、`WebSearch`、`WebFetch` 等 | 本项目首期使用 SDK 自带 `Bash` 调用 `chatq ...` CLI；其他内置工具按最小权限开放 |
| Skills | SDK 原生支持 `.claude/skills` 等 Claude Code skill 机制 | M2 只选择和配置允许使用的 SDK skills，由 SDK 原生机制加载 |
| 扩展工具机制 | SDK 另有扩展工具能力 | 本项目首期不采用，避免新增一套工具注册与部署面；平台能力统一走 CLI |
| 权限控制 | `allowed_tools` 预批准，`disallowed_tools` 移除或阻断工具，`permission_mode` 控制未命中规则时如何处理 | 必须同时使用 availability、allow、deny、hook，不能误把 `allowed_tools` 当唯一安全边界 |
| Hooks | `PreToolUse`、`PostToolUse`、`Stop`、`SessionStart`、`SessionEnd`、`UserPromptSubmit` 等 | 用于审计、阻断越权、注入上下文、脱敏日志 |
| Sessions | SDK session 可 resume/fork，保留已读文件、对话历史和分析上下文 | ChatSession 只记录 `sdk_session_id`、`project_key` 和产品元数据；历史消息从 SDK session 读取 |
| Session messages | Python 提供 `get_session_messages()`，TypeScript 提供 `getSessionMessages()` | 历史会话详情不需要再保存一份 SDKMessage/ContentBlock/Result 表 |
| SessionStore | SDK 可把 transcript 镜像到 S3、Redis、Postgres 或自定义后端 | 多机部署用 SDK SessionStore 作为 transcript 持久层，而不是 M1 自定义消息表 |
| 流式消息 | 可处理 `AssistantMessage`、`ResultMessage`，开启 partial streaming 时获得增量消息 | 前端对话流和工具进度按 SDK message/content block 语义渲染 |
| Claude Code 特性 | 可加载 `CLAUDE.md`、`.claude/skills`、hooks、plugins 等 | 生产环境建议显式设置 `setting_sources`，避免加载不可控本机配置 |

## 3. `query()` 与 `ClaudeSDKClient`

| 接口 | 适用场景 | Chat-Quant 建议 |
|---|---|---|
| `query()` | 单次或简单异步任务，迭代返回 SDK message | 可用于首期最小实现、后台工具验证、简单分析回合 |
| `ClaudeSDKClient` | 需要长连接、多次输入、hooks、交互式控制的应用 | 对话工作台主路径优先使用，便于承接连续追问、取消、审计和 Bash/CLI 工具调用 |

无论使用哪种接口，Chat-Quant 都不需要实现底层工具循环。应用只需要：

1. 构造 `ClaudeAgentOptions`。
2. 注入 system prompt、session resume、SDK skills、`Bash`/必要内置工具、权限、hooks、工作目录、Bash 命令白名单等。
3. 迭代接收 SDK messages，用于当前请求的实时流式展示。
4. 保存 SDK session id 到 ChatSession；历史详情通过 `get_session_messages()` 或 SessionStore 读取 SDK messages。
5. 只把代码、策略、回测等系统资产通过 AssetLink 关联到 `sdk_session_id`、SDK message uuid 或 SDK tool_use id。

## 3.1 Session messages 与存储取舍

官方文档说明，SDK 会自动把 session transcript 写到本地 JSONL；两个 SDK 都提供读取历史消息的函数：Python 是 `get_session_messages()`，TypeScript 是 `getSessionMessages()`。因此 Chat-Quant 不需要把 SDK message/content block/result 再投影成一套 M1 业务消息表。

多机部署或容器环境下，本地 `~/.claude/projects/` 不可靠，应配置 SDK `SessionStore`。`SessionStore` 由 SDK 调用 `append()` 和 `load()`，可以落到 Postgres/S3/Redis。这里的存储是 SDK transcript 的镜像，条目应按 SDK opaque JSON 保存；Chat-Quant 不解析为自有消息模型，只在读取详情或建立资产引用时使用 SDK message uuid、tool_use id 等稳定引用。

设计结论：

1. ChatSession 保存 `sdk_session_id`、`sdk_project_key`、标题、摘要、标签和当前焦点资产。
2. transcript 展示走 SDK `get_session_messages()`；使用外部 SessionStore 时，通过 SDK store/list/load 能力读取。
3. M1 不建 `sdk_messages`、`sdk_content_blocks`、`sdk_results` 表。
4. 必须持久化的业务关联只存 AssetLink：`chat_session_id`、`sdk_session_id`、`sdk_message_uuid`、`sdk_tool_use_id`、`asset_type`、`asset_id`。
5. 如果需要全文搜索或埋点，可后续增加只读索引/缓存，但它不是事实源，也不能替代 SDK session transcript。

## 4. Bash 平台能力边界

Chat-Quant 首期选择 Bash 内部可执行的 `chatq ...` CLI 作为平台能力边界：Agent 通过 SDK 自带 `Bash` 工具执行白名单内的命令；CLI 再通过 FastAPI 或内部应用服务调用 M1-M6。CLI 清单不是 Chat/Agent API，不对前端或外部调用方暴露；它只是 M2 构建 SDK 运行环境和 Hook 校验时使用的 command policy。

| 能力 | Bash 中允许的 CLI | 后端入口 |
|---|---|---|
| 保存代码产物 | `chatq artifact save-code` | M3 CodeArtifactService |
| 执行 Python 代码 | `chatq runtime execute` | M4 PythonRuntimeService |
| 生成 K 线/收益/回撤图表 | `chatq chart kline`、`chatq chart backtest` | M3/M4/M6 |
| 创建/校验策略版本 | `chatq strategy create`、`chatq strategy validate` | M5 StrategyAssetService |
| 创建/运行/查询回测 | `chatq backtest create`、`chatq backtest run`、`chatq backtest get` | M6 BacktestResultService |
| 关联会话资产 | `chatq conversation link-asset` | M1 ChatSessionService |

CLI 命令必须提供清晰描述、输入 schema、JSON/JSONL 输出、幂等键和错误码。Agent 看见的是受约束的 `chatq` 命令，而不是任意 shell 能力。

## 5. 权限与安全要点

1. `allowed_tools` 主要表示预批准；未列入的工具并不一定从上下文消失。若要彻底移除工具，需要使用 `tools` 限制内置工具可见性，或使用 `disallowed_tools`。
2. 对高风险能力必须使用 `PreToolUse` hook 做强制校验，例如越权路径、跨用户资产、真实交易关键词、外部写操作、超大回测。
3. `permission_mode="bypassPermissions"` 只能在强隔离环境使用；生产默认不使用。
4. 首期不启用额外 SDK 扩展工具；如果后续启用，必须先更新详细设计和权限模型。
5. Bash 只能执行 command policy 白名单内的 `chatq ...` 前缀；禁止 shell control operators、重定向到非授权目录、命令替换、后台执行和任意包安装。
6. CLI 返回失败时必须输出结构化 JSON 错误，让 Claude 能继续解释或改用其他路径。
7. Hook 和 CLI 处理器都必须脱敏 API key、token、cookie、密钥路径和过长 stdout/stderr。

## 6. 对 Chat-Quant 模块的影响

| 模块 | 调整后的定位 |
|---|---|
| M1 会话与消息 | 记录 ChatSession、SDK session id、产品元数据和 AssetLink；历史消息从 SDK session 读取 |
| M2 Claude Agent Runtime | 封装 SDK 配置、SessionStore、Bash/CLI 权限和流式消息透传，不自建 Agent loop |
| M3 代码产物 | 作为 `chatq artifact save-code` 的领域服务，保存代码和文件资产 |
| M4 Python 运行时 | 作为 `chatq runtime execute` 的领域服务，受控执行代码并返回 `ExecutionResult` |
| M5 策略资产 | 作为 `chatq strategy create/validate/get` 的领域服务，管理策略版本 |
| M6 回测与风险结果 | 作为 `chatq backtest create/run/get/compare` 的领域服务，管理回测运行和结果 |

## 7. 设计原则修订

1. 不再设计自研 Agent 任务中心、Agent 编排器或工具循环。
2. M2 不直接调用 M3-M6 业务服务来编排股票任务；Agent 通过 Bash 调用 `chatq ...`，CLI 调用对应应用服务。
3. 平台 CLI 必须有明确 schema、权限校验、幂等键、结构化返回和审计记录。
4. SDK session 负责智能体上下文连续性；ChatSessionContext 负责系统资产连续性。二者互补，不互相替代。
5. UI 的“读取上下文/调用工具/整理产物/生成回复”直接根据 SDK assistant text block、Bash tool_use、tool_result 和 ResultMessage 渲染。
