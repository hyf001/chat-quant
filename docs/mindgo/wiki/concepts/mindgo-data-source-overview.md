---
title: MindGo 数据源总览
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-source", "workflow"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md", "raw/articles/mindgo-api-docs-help-4.md", "raw/articles/jupyter-python-execution-pattern.md", "raw/code/indexmap-arsenal-query.py.md"]
confidence: high
---
# MindGo 数据源总览

MindGo 数据源由三层材料组成：

1. [[mindgo-data-dictionary]]：从数据平台详情页抓取的 101 个数据文档，包含字段说明、使用代码和数据样例。
2. [[mindgo-api-docs]]：从 `help/4` 抓取的 API 文档，包含策略框架、行情资金、证券信息、表数据、问财和工具函数。
3. [[mindgo-jupyter-python-execution]]：通过远程 Jupyter 执行 MindGo runtime 内函数，适合让本地 LLM/Agent 自动取数或跑 notebook 代码。

选择路径时优先按问题类型分流：

| 问题 | 优先入口 | 备注 |
| --- | --- | --- |
| 查某张表有哪些字段 | [[mindgo-data-dictionary]] | 字段说明和样例数据最完整 |
| 写策略或研究环境代码 | [[mindgo-api-docs]] | 看函数签名、参数、返回值、示例 |
| 让本地 Agent 自动调远端数据 | [[mindgo-jupyter-python-execution]] | 需要 Jupyter URL/token |
| 查股票/基金/期货等标的基础信息 | [[mindgo-security-reference-api]] | 常用 `get_all_securities`、`get_security_info` |
| 查历史行情或分钟行情 | [[mindgo-market-data-api]] | 常用 `get_price` / `get_price_future` |
| 查财务表 | [[mindgo-fundamental-table-api]] | 常用 `get_fundamentals` |
| 问自然语言选股 | [[mindgo-iwencai-api]] | 区分研究环境和回测环境 |
| 用内部 indexmap/query_index | [[mindgo-indexmap-arsenal-api]] | 当前样例脚本未完整解析 rows |
