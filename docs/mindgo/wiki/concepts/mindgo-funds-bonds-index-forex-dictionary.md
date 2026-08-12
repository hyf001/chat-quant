---
title: MindGo 基金债券指数外汇数据字典
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-dictionary", "funds", "bonds", "index", "forex", "catalog"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 基金债券指数外汇数据字典

本页汇总基金、可转债、指数、外汇的数据平台条目。行情字段通常对应 [[mindgo-market-data-api]]；基本信息与成分股相关函数见 [[mindgo-security-reference-api]]。

| ID | 名称 | 分类 | 字段数 | 代码块 | 主要调用 |
| --- | --- | --- | ---: | ---: | --- |
| 249 | 场内基金基本信息 | 基金 / 场内基金 / 基金基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有ETF基金的基本信息 |
| 253 | 基金净值数据 | 基金 / 场内基金 / 基金净值数据 | 3 | 3 | get_extras(<br>[IN]: |
| 257 | 基金日频行情数据 | 基金 / 场内基金 / 基金行情数据 | 15 | 3 | get_price(<br>[IN]: |
| 258 | 基金分钟行情数据 | 基金 / 场内基金 / 基金行情数据 | 8 | 3 | get_price(<br>[IN]: |
| 259 | 基金实时行情数据 | 基金 / 场内基金 / 基金行情数据 | 52 | 1 | get_current(securities, fields) |
| 277 | 基金十大持仓 | 基金 / 场外基金 / 基金持仓情况 | 11 | 2 | run_query(query_object)<br>#获取全部基金十大持仓数据 |
| 278 | 基金持仓明细 | 基金 / 场外基金 / 基金持仓情况 | 11 | 2 | run_query(query_object)<br>#获取全部基金持仓明细 |
| 269 | 场外基金基本信息 | 基金 / 场外基金 / 基金基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有场外基金的基本信息 |
| 273 | 基金净值数据 | 基金 / 场外基金 / 基金净值数据 | 3 | 3 | get_extras(<br>[IN]: |
| 332 | 外汇基本信息 | 外汇 / 外汇基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有外汇基本信息 |
| 336 | 外汇交易日历 | 外汇 / 外汇交易日历 | 0 | 1 | get_all_trade_days_fx() |
| 324 | 外汇日行情数据 | 外汇 / 外汇行情数据 | 4 | 3 | get_price_fx(<br>[IN]: |
| 325 | 外汇分钟行情数据 | 外汇 / 外汇行情数据 | 4 | 3 | get_price_fx(<br>[IN]: |
| 204 | 可转债基本信息 | 债券 / 可转债 / 可转债基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有可转债的基本信息 |
| 224 | 可转债条款信息 | 债券 / 可转债 / 可转债条款信息 | 34 | 2 | run_query(query_object)<br>#获取全市场可转债信息表 |
| 228 | 可转债转股价变更表 | 债券 / 可转债 / 可转债条款信息 | 5 | 2 | run_query(query_object)<br>#获取全市场可转债转股价变更表 |
| 229 | 可转债余额变动表 | 债券 / 可转债 / 可转债条款信息 | 4 | 2 | run_query(query_object)<br>#获取全市场可转债余额变动表 |
| 230 | 可转债转股数量表 | 债券 / 可转债 / 可转债条款信息 | 10 | 2 | run_query(query_object)<br>#获取全市场可转债转股数量表 |
| 231 | 可转债特殊条款预计价格表 | 债券 / 可转债 / 可转债条款信息 | 4 | 2 | run_query(query_object)<br>#获取全市场可转债特殊条款预计价格表 |
| 208 | 可转债日行情数据 | 债券 / 可转债 / 可转债行情 | 12 | 3 | get_price(<br>[IN]: |
| 209 | 可转债分钟行情数据 | 债券 / 可转债 / 可转债行情 | 8 | 3 | get_price(<br>[IN]: |
| 210 | 可转债实时行情快照 | 债券 / 可转债 / 可转债行情 | 52 | 1 | get_current(securities, fields) |
| 211 | 可转债历史行情快照 | 债券 / 可转债 / 可转债行情 | 53 | 1 | get_tick(securities, start_date, end_date, fields) |
| 300 | 指数成分股及权重 | 指数 / 指数成分股数据 | 2 | 0 |  |
| 293 | 指数基本信息 | 指数 / 指数基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于可用状态的所有指数的基本信息 |
| 295 | 常用股票型指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 488 | 常用基金型指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 498 | 常用债券型指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 504 | 常用期货型指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 510 | 常用港股指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 512 | 常用全球指数 | 指数 / 指数基本信息 | 0 | 0 |  |
| 296 | 指数日行情数据 | 指数 / 指数行情数据 | 16 | 3 | get_price(<br>[IN]: |
| 297 | 指数分钟行情数据 | 指数 / 指数行情数据 | 9 | 3 | get_price(<br>[IN]: |
| 298 | 指数实时行情快照 | 指数 / 指数行情数据 | 52 | 1 | get_current(securities, fields) |
