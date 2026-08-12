---
title: MindGo A股1分钟分时实时行情
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "intraday", "market-data", "jupyter", "stock"]
sources: ["raw/code/jupyter-intraday-realtime-pattern.py.md", "raw/articles/mindgo-api-docs-help-4.md"]
confidence: high
---

# MindGo A股1分钟分时实时行情

A 股 1 分钟分时取数可以抽象为一段远程 Jupyter Python 脚本：在 MindGo kernel 中执行 `get_price(STOCK_LIST, START_TIME, END_TIME, "1m", FIELDS, True, None, 0, is_panel=1)`，再把返回的 Panel/dict/DataFrame 结构转成 JSON rows。

## 输入规范

- 股票代码支持 `000001.SZ` 或纯 6 位代码；纯代码可按规则补交易所后缀。
- `trade_date` 为 `YYYYMMDD`。
- `end_time` 为 `HH:MM`；历史日通常取 `15:00`，当天应按上海交易时段裁剪到当前交易分钟或午休/收盘边界。

## 输出字段

每行包含 `stockcode`、`trade_date`、`bar_time`、`open`、`high`、`low`、`close`、`volume`、`amount`。远程 MindGo 返回的 `turnover` 可归一化为 `amount`。

## 关键脚本模式

完整模式见 `raw/code/jupyter-intraday-realtime-pattern.py.md`。核心点是：远程执行 [[mindgo-market-data-api]] 的 `get_price`，本地只解析标记 JSON，不在本地复刻 MindGo runtime。

字段背景可对照 [[mindgo-market-data-api]] 与 [[mindgo-stock-data-dictionary]]；远程执行流程见 [[mindgo-jupyter-python-execution]]。
