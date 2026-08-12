---
title: MindGo 取数方式对比
created: 2026-08-11
updated: 2026-08-11
type: comparison
tags: ["mindgo", "comparison", "data-source", "workflow"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md", "raw/articles/mindgo-api-docs-help-4.md", "raw/articles/jupyter-python-execution-pattern.md", "raw/code/indexmap-arsenal-query.py.md"]
confidence: high
---

# MindGo 取数方式对比

| 方式 | 主要用途 | 优点 | 局限 | 首选页面 |
| --- | --- | --- | --- | --- |
| 数据平台详情页 | 查表、字段、样例 | 字段说明和样例最完整 | 不是执行环境 | [[mindgo-data-dictionary]] |
| API 文档 | 写研究/策略代码 | 函数签名、参数、返回值清楚 | 字段细节需要查字典 | [[mindgo-api-docs]] |
| 远程 Jupyter Python 执行 | 本地脚本/Agent 调远程 MindGo runtime | 可真实执行取数代码 | 需要授权 Jupyter token，任意代码执行风险高 | [[mindgo-jupyter-python-execution]] |
| 专用分时脚本模式 | 小批量 A 股分钟行情 | 输入/输出规范，少写代码 | 只覆盖 A 股 1m bars | [[mindgo-intraday-realtime-bars]] |
| indexmap/arsenal | 内部指标或全市场股票行情/异动 | 可访问 query_index 类接口 | 当前只有入口脚本，需补 rows 解析 | [[mindgo-indexmap-arsenal-api]] |

实践中先从 [[mindgo-data-source-overview]] 分流：查字段走字典，写函数走 API，自动执行走远程 Jupyter Python，内部指标再尝试 indexmap。
