---
title: MindGo 财务与表数据 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "fundamentals"]
sources: ["raw/articles/mindgo-api-docs-help-4.md", "raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 财务与表数据 API

财务和表数据主要通过 `get_fundamentals(query_object, date=None, statDate=None, latest=False)` 查询。API 文档说明函数签名、参数和返回值；字段、表名和样例应对照 [[mindgo-stock-data-dictionary]] 中的上市公司财务数据。

## 常见表族

| 表族 | 数据平台文档 |
| --- | --- |
| 估值 | 估值指标表 |
| 三大报表 | 资产负债表、利润表、现金流量表 |
| 单季度报表 | 利润表(单季度)、现金流量表(单季度) |
| 财务指标 | 盈利能力、成长能力、偿还能力、运营能力 |
| 业绩 | 业绩快报、业绩预告 |

## 使用提示

- `date` 与 `statDate` 通常二选一；二者都为 `None` 时文档描述默认取当前时间前一日。
- 返回列常以 `表名_字段名` 命名。
- 查询前先在 [[mindgo-data-dictionary]] 找字段含义，避免误用同比、累计、单季度或特殊平衡科目字段。

相关取数路线对比见 [[mindgo-access-methods-comparison]]。
