---
name: strategy_management
description: 当需要在 Chat-Quant 中管理量化策略和回测时使用，包括创建策略、编辑策略、查看策略版本、切换版本、归档/删除策略、运行回测、查看回测记录，以及理解策略源码协议和回测框架。
---

# 策略管理与回测

使用本技能处理 Chat-Quant 中的策略生命周期和回测工作。优先按用户意图选择最小必要模块读取，避免一次性加载所有细节。

## 执行环境

当前项目 Python 环境位于仓库根目录的 `.venv`。执行策略管理命令时从 `/Users/huyufei/Documents/hyf/code/github/chat-quant` 运行，优先使用 `uv run ...` 或 `.venv/bin/python ...`，避免系统 Python 环境导致依赖不一致。

项目级策略命令需要传入业务项目路径，例如 `--project-path "<当前项目路径>"`。该路径来自 Agent 启动时的当前 `pwd` / `project.local_path`，不要用仓库根目录替代。

## 模块选择

- 策略创建或创建新版本：读取 [references/strategy-management.md](references/strategy-management.md) 和 [references/strategy-protocol.md](references/strategy-protocol.md)，先理解策略源码协议再提交。
- 策略查看、编辑、版本切换、归档、删除：读取 [references/strategy-management.md](references/strategy-management.md)。
- 回测执行、指定版本回测、回测记录查看、回测参数覆盖：读取 [references/backtesting.md](references/backtesting.md)。
- 编写或检查策略源码、解释参数协议、确认使用框架：读取 [references/strategy-protocol.md](references/strategy-protocol.md)。

## 通用流程

1. 先确认用户是在做策略管理、策略源码编写，还是回测。
2. 读取对应 reference 文件；创建策略或新版本时必须同时了解策略源码协议，不要默认加载无关模块。
3. 从仓库根目录执行项目提供的策略管理命令；`list`、`create` 等项目级命令显式传 `--project-path "<当前项目路径>"`。不确定参数时先运行 `uv run python -m cli.chatq_strategy --help` 或 `uv run python -m cli.chatq_strategy <command> --help`。
4. 对会创建资源的动作，记录返回的 `strategy_id`、`strategy_version_id`、`backtest_id`。
5. 修改策略后，优先用当前版本回测；需要历史对比时再指定版本。

## 可打开对象链接

策略管理命令返回 JSON 中如果包含 `artifacts[].display_token`，最终回答必须原样输出这些
`display_token`，不要改写链接、ID、括号或标题。`display_token` 会被前端识别并在右侧对象面板打开。

支持的对象链接包括：

- `[查看回测结果](chatq://backtest/sbt_xxx)`
- `[打开策略](chatq://strategy/str_xxx)`
- `[查看策略版本](chatq://strategy-version/stv_xxx)`
