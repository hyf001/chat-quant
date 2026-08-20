---
name: strategy_management
description: 当需要在 Chat-Quant 中管理量化策略和回测时使用，包括创建策略、编辑策略、查看策略版本、切换版本、归档/删除策略、运行回测、查看回测记录，以及理解策略源码协议和回测框架。
---

# 策略管理与回测

使用本技能处理 Chat-Quant 中的策略生命周期和回测工作。优先按用户意图选择最小必要模块读取，避免一次性加载所有细节。

## 执行环境

策略管理和回测通过 Claude Agent SDK 注入的 MCP 工具 `strategy` 完成，完整工具名是 `mcp__chatq__strategy`。不要用 Bash 或本地 HTTP 请求替代该工具。

工具调用统一使用一个 `command` 字符串，内容按 `chatq-strategy` CLI 子命令和 `--参数` 写法传入。当前业务项目上下文由后端绑定，不要传 `project_id`、`user_id`、`project_path` 或 API base URL。

## 模块选择

- 策略创建或创建新版本：读取 [references/strategy-management.md](references/strategy-management.md) 和 [references/strategy-protocol.md](references/strategy-protocol.md)，先理解策略源码协议再提交。
- 策略查看、编辑、版本切换、归档、删除：读取 [references/strategy-management.md](references/strategy-management.md)。
- 回测执行、指定版本回测、回测记录查看、回测参数覆盖：读取 [references/backtesting.md](references/backtesting.md)。
- 编写或检查策略源码、解释参数协议、确认使用框架：读取 [references/strategy-protocol.md](references/strategy-protocol.md)。
- 策略需要使用指数、财务、公告、新闻等平台数据集作为补充信号时：同时读取 [references/dataset-api.md](references/dataset-api.md)，先确认可用数据集、字段和示例 SQL。

## 通用流程

1. 先确认用户是在做策略管理、策略源码编写，还是回测。
2. 读取对应 reference 文件；创建策略或新版本时必须同时了解策略源码协议，不要默认加载无关模块。
3. 调用 MCP 工具 `mcp__chatq__strategy`，按 reference 中的 CLI-style `command` 传参。
4. 对会创建资源的动作，记录返回的 `strategy_id`、`strategy_version_id`、`backtest_id`。
5. 修改策略后，优先用当前版本回测；需要历史对比时再指定版本。
