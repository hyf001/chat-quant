---
title: MindGo 策略框架 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "trading"]
sources: ["raw/articles/mindgo-api-docs-help-4.md"]
confidence: high
---
# MindGo 策略框架 API

策略框架 API 定义回测/模拟交易代码的生命周期、回调函数、交易函数、context 对象和重要枚举。它是 [[mindgo-api-docs]] 的基础层，行情和财务 API 通常在这些回调中被调用。

## 关键回调

- `init(context)`：初始化函数，通常只运行一次。
- `handle_bar(context, bar_dict)`：按交易频率处理 bar 行情。
- `handle_tick(context, tick)`：tick 行情变化时调用，支持范围受策略类型限制。
- `before_trading` / `open_auction` / `after_trading`：盘前、集合竞价后、盘后阶段。
- `on_order` / `on_trade`：委托和成交回调。

## 交易相关

下单函数如 `order_target`、`order_target_value`、`order_target_percent` 属于策略交易语义，不应和只读数据查询混淆。若通过 [[mindgo-jupyter-python-execution]] 运行策略相关代码，要先确认不会触发真实交易或远程文件修改；参见 [[mindgo-security-model]]。
