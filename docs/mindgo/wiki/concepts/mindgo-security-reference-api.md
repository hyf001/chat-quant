---
title: MindGo 证券信息 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "securities"]
sources: ["raw/articles/mindgo-api-docs-help-4.md", "raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 证券信息 API

证券信息接口回答“有哪些标的、属于什么分类、在哪些交易日、属于什么行业/概念”。它和 [[mindgo-data-dictionary]] 中的基本信息、行业、概念、指数成分股、因子数据表对应。

## 常用函数

| 函数 | 作用 | 典型用途 |
| --- | --- | --- |
| `get_all_securities(ty=None, date=None)` | 获取某类证券列表 | A 股、ETF、LOF、期货、期权、可转债、指数、外汇等 |
| `get_security_info` | 单只证券基本信息 | 查询交易所、上市日期、名称等 |
| `get_trade_days` / `get_all_trade_days` | 交易日历 | 回测窗口、调仓日期 |
| `get_index_stocks` / `get_index_weight` | 指数成分股与权重 | 指数增强、成分筛选 |
| `get_industry_stocks` / `get_industry_relate` / `get_symbol_industry` | 行业分类 | 行业中性、行业过滤 |
| `get_concept_stocks` / `get_concept_relate` | 同花顺概念 | 概念主题池 |
| `get_sfactor_data` | 因子数据 | 技术因子、基本面因子 |

用户提供的 `获取indexmap指标数据方法.py` 是另一条内部接口思路，使用 `get_arsenal_api(...).post('/babel/api/query_index')`，应单独看 [[mindgo-indexmap-arsenal-api]]。
