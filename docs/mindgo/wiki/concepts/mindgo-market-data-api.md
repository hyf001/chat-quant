---
title: MindGo 行情资金 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "market-data", "intraday"]
sources: ["raw/articles/mindgo-api-docs-help-4.md", "raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 行情资金 API

行情资金接口集中在 API 文档“行情资金数据接口”，并和数据平台中的日频/分钟/快照字段表互相对应。

## 常用函数

| 函数 | 用途 | 对应字典 |
| --- | --- | --- |
| `get_price` | 股票、场内基金、指数、可转债等行情 | [[mindgo-stock-data-dictionary]], [[mindgo-funds-bonds-index-forex-dictionary]] |
| `get_price_future` | 期货行情 | [[mindgo-futures-options-data-dictionary]] |
| `history` | 策略内获取历史行情 | [[mindgo-strategy-framework-api]] |
| `get_last_tick` / `get_tick` | 实时/历史快照 | [[mindgo-stock-data-dictionary]] |
| `get_money_flow_step` | 历史资金数据 | [[mindgo-stock-data-dictionary]] |
| `get_call_auction` | 开盘竞价成交信息 | [[mindgo-stock-data-dictionary]] |
| `get_mtss` | 融资融券数据 | [[mindgo-stock-data-dictionary]] |

分时实时脚本模式实际使用远端 `get_price(..., fre_step='1m', is_panel=1)`，并把 MindGo 的 `turnover` 归一化为 `amount`，见 [[mindgo-intraday-realtime-bars]]。

字段选择应先查数据平台：A 股日行情、分钟行情、历史行情快照、实时行情快照、期货日/分钟行情、基金行情、指数行情、外汇行情等都已在 [[mindgo-data-dictionary]] 建档。
