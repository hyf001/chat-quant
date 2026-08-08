---
title: "AKShare 外汇数据"
created: 2026-07-26
updated: 2026-07-26
type: concept
tags: [akshare, data-dictionary, category, fx]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# AKShare 外汇数据

来源页面: https://akshare.akfamily.xyz/data/fx/fx.html
原始快照: [fx/fx.md](../../raw/data-dictionary/fx/fx.md)

该分类从 AKShare 数据字典中抽取出 11 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。

## 接口

- [[currency-boc-safe|currency_boc_safe]] - 外汇管理局-人民币汇率中间价
- [[currency-boc-sina|currency_boc_sina]] - 新浪财经-中行人民币牌价历史数据
- [[currency-pair-map|currency_pair_map]] - 指定币种的所有能够获取到的货币对信息，历史数据可以调用 **ak.currency_history()** 获取
- [[forex-hist-em|forex_hist_em]] - 东方财富网-行情中心-外汇市场-所有汇率-历史行情数据
- [[forex-spot-em|forex_spot_em]] - 东方财富网-行情中心-外汇市场-所有汇率-实时行情数据
- [[fx-c-swap-cm|fx_c_swap_cm]] - 中国外汇交易中心暨全国银行间同业拆借中心-基准-外汇市场-外汇掉期曲线-外汇掉期 C-Swap 定盘曲线
- [[fx-pair-quote|fx_pair_quote]] - 外币对即期报价
- [[fx-quote-baidu|fx_quote_baidu]] - 百度股市通-外汇-行情榜单
- [[fx-spot-quote|fx_spot_quote]] - 人民币外汇即期报价
- [[fx-swap-quote|fx_swap_quote]] - 人民币外汇远掉报价
- [[macro-fx-sentiment|macro_fx_sentiment]] - 货币对-投机情绪报告

## 相关

- [[index]]
- [[_meta/topic-map]]
