---
title: SuperMind / MindGo
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: ["mindgo", "supermind", "data-source"]
sources: ["raw/articles/mindgo-api-docs-help-4.md", "raw/articles/mindgo-dataplatform-detail-docs.json.md", "raw/articles/jupyter-python-execution-pattern.md"]
confidence: high
---

# SuperMind / MindGo

SuperMind / MindGo 在本仓库中被视为一个复合数据源：它既有在线策略与研究环境里的 [[mindgo-api-docs]]，也有可浏览的数据平台字段字典 [[mindgo-data-dictionary]]，还可以通过 [[mindgo-jupyter-python-execution]] 在授权远程 Jupyter kernel 中执行 Python 取数脚本。

核心数据获取路径有三类：

| 路径 | 适合场景 | 代表入口 |
| --- | --- | --- |
| 策略/研究 API | 常规行情、证券信息、财务、问财、因子 | [[mindgo-api-docs]] |
| 数据平台字典 | 查字段、表含义、样例代码、样例数据 | [[mindgo-data-dictionary]] |
| 远程 Jupyter Python 执行 | 需要让本地脚本/Agent 调用远端 MindGo runtime | [[mindgo-jupyter-python-execution]] |

和一般 HTTP 数据源不同，很多 MindGo 能力依赖其远程运行环境，因此密钥、Jupyter kernel、会话路径和运行时内置函数是架构的一部分。相关安全边界见 [[mindgo-security-model]]。
