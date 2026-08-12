---
title: MindGo 文件与工具 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "files", "utilities"]
sources: ["raw/articles/mindgo-api-docs-help-4.md"]
confidence: high
---
# MindGo 文件与工具 API

工具函数位于 `help/4` 的“工具函数”部分，覆盖代码格式转换、文件读写、路径查询、复制/删除、消息推送、自选板块和文件加密。

这些函数和 远程 Jupyter 文件读写流程 容易混淆：

| 能力 | MindGo API | 远程 Jupyter 脚本 |
| --- | --- | --- |
| 在远程研究环境内读写 | `write_file` / `read_file` / `list_file` | `execute_code` 间接执行 |
| 本地与远程 Jupyter 同步 | 不适用 | 使用 Jupyter Contents API 或远程文件函数 |
| 删除远程文件 | `remove_file` | 通过代码或 Contents API，需谨慎 |

安全注意：删除、覆盖、同步远程文件前应先做 dry run 或显式确认，见 [[mindgo-security-model]]。
