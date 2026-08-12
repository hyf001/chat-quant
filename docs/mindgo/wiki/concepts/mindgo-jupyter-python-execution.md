---
title: MindGo Jupyter Python 执行取数
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "jupyter", "workflow", "data-source"]
sources: ["raw/articles/jupyter-python-execution-pattern.md", "raw/code/jupyter-intraday-realtime-pattern.py.md", "raw/articles/mindgo-api-docs-help-4.md"]
confidence: high
---

# MindGo Jupyter Python 执行取数

这页只保留从 portable Jupyter 案例中抽象出的取数方法：在授权的远程 MindGo / SuperMind Jupyter kernel 中执行 Python 代码，用 MindGo 内置函数获取数据，再把结果标准化输出。

## 方法模型

1. 准备远程 Jupyter URL、token、认证方式和 notebook/kernel 路径。
2. 创建或复用 Python kernel。
3. 发送 Python 代码到 kernel 执行。
4. 代码中调用 [[mindgo-api-docs]] 的函数，例如 `get_price`、`get_all_securities`、`get_fundamentals`、`query_iwencai`、`get_arsenal_api`。
5. 将 DataFrame、dict 或 Panel 结果转成 JSON-friendly records，并用明确 marker 打印到 stdout。
6. 本地解析 stdout，落成 rows、summary 或 DataFrame。

## 适合场景

| 场景 | 推荐做法 |
| --- | --- |
| 少量 A 股 1 分钟分时 | 用 [[mindgo-intraday-realtime-bars]] 的脚本模式 |
| 股票/基金/指数/可转债行情 | 在远程代码中调用 [[mindgo-market-data-api]] |
| 证券基本信息、交易日、成分股 | 在远程代码中调用 [[mindgo-security-reference-api]] |
| 财务与估值表 | 在远程代码中调用 [[mindgo-fundamental-table-api]] |
| 自然语言选股 | 在远程代码中调用 [[mindgo-iwencai-api]] |
| indexmap 指标 | 在远程代码中调用 [[mindgo-indexmap-arsenal-api]] |

## 安全边界

远程 Python 执行拥有 Jupyter 账号权限。只读取数代码风险较低；文件写入、删除、网络请求、长时间任务和交易函数需要额外确认。更完整的约束见 [[mindgo-security-model]]。
