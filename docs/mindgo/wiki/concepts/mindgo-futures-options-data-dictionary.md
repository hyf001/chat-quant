---
title: MindGo 期货期权数据字典
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-dictionary", "futures", "options", "td", "catalog"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 期货期权数据字典

本页汇总期货、期权与 T+D 合约的数据平台条目。行情函数优先看 [[mindgo-market-data-api]]，证券/合约信息看 [[mindgo-security-reference-api]]。

| ID | 名称 | 分类 | 字段数 | 代码块 | 主要调用 |
| --- | --- | --- | ---: | ---: | --- |
| 159 | 期货基本信息(商品) | 期货 / 内地期货 / 期货基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有商品期货的基本信息 |
| 160 | 期货基本信息(金融) | 期货 / 内地期货 / 期货基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有股指期货的基本信息 |
| 161 | 期货基本信息(国债) | 期货 / 内地期货 / 期货基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有国债期货的基本信息 |
| 171 | 期货交易日历 | 期货 / 内地期货 / 期货交易日历 | 0 | 1 | get_all_trade_days() |
| 426 | 期货日交易排名 | 期货 / 内地期货 / 期货市场信息 | 7 | 2 | run_query(query_object)<br>#获取全市场2023年6月6日成交量龙虎榜 |
| 427 | 期货库存情况 | 期货 / 内地期货 / 期货市场信息 | 10 | 2 | run_query(query_object)<br>#获取全市场2023年6月6日各品种库存量情况 |
| 174 | 期货日频行情数据 | 期货 / 内地期货 / 期货行情数据 | 14 | 3 | get_price_future(<br>[IN]: |
| 422 | 期货分钟行情数据 | 期货 / 内地期货 / 期货行情数据 | 7 | 3 | get_price_future(<br># 获取IC2304、IF2304两个标的在2023年4月6日10点30分前3分钟的数据 |
| 178 | TD合约基本信息 | 期货 / 延期交收合约(T+D合约) / TD合约基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有T+D合约的基本信息 |
| 182 | TD合约交易日历 | 期货 / 延期交收合约(T+D合约) / TD合约交易日历 | 0 | 1 | get_all_trade_days_td() |
| 185 | TD合约日频行情数据 | 期货 / 延期交收合约(T+D合约) / TD合约行情数据 | 7 | 3 | get_price_td(<br>[IN]: |
| 189 | 期权基本信息 | 期权 / 金融期权 / 期权基本信息 | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有期权的基本信息 |
| 193 | 期权交易日历 | 期权 / 金融期权 / 期权交易日历 | 0 | 1 | get_all_trade_days() |
| 196 | 期权日频行情数据 | 期权 / 金融期权 / 期权行情数据 | 5 | 3 | get_price(<br>[IN]: |
| 197 | 期权分钟行情数据 | 期权 / 金融期权 / 期权行情数据 | 5 | 3 | get_price(<br>[IN]: |
