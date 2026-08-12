---
title: MindGo 数据源取数快速入口
created: 2026-08-11
updated: 2026-08-11
type: query
tags: ["mindgo", "query", "workflow", "data-source"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md", "raw/articles/mindgo-api-docs-help-4.md", "raw/articles/jupyter-python-execution-pattern.md", "raw/code/indexmap-arsenal-query.py.md"]
confidence: high
---

# MindGo 数据源取数快速入口

当用户问“MindGo 怎么取某类数据”时，按下面顺序决策：

1. 先判断数据类型：行情、证券信息、财务表、因子、问财、远程 Jupyter 自动化、内部 indexmap。
2. 查字段：进入 [[mindgo-data-dictionary]] 及对应分类页。
3. 查函数：进入 [[mindgo-api-docs]] 及对应 API 页。
4. 要远程执行：进入 [[mindgo-jupyter-python-execution]]，把 Python 取数代码发到授权 Jupyter kernel 执行。
5. 要全市场/异动/indexmap：进入 [[mindgo-indexmap-arsenal-api]]，注意当前脚本还缺行数据解析。

## 常见问题到页面

| 用户需求 | 应读页面 |
| --- | --- |
| A 股分钟行情 / 日行情 | [[mindgo-market-data-api]], [[mindgo-stock-data-dictionary]] |
| Jupyter 获取实时 1m 分时 | [[mindgo-intraday-realtime-bars]], [[mindgo-jupyter-python-execution]] |
| 全市场证券列表 | [[mindgo-security-reference-api]], [[mindgo-stock-data-dictionary]] |
| 财务/估值/三大报表 | [[mindgo-fundamental-table-api]], [[mindgo-stock-data-dictionary]] |
| 期货/期权行情 | [[mindgo-market-data-api]], [[mindgo-futures-options-data-dictionary]] |
| 问财自然语言选股 | [[mindgo-iwencai-api]] |
| indexmap 指标 | [[mindgo-indexmap-arsenal-api]] |
| 不确定取数路线 | [[mindgo-access-methods-comparison]] |
