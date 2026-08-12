---
title: MindGo 数据平台数据字典
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-dictionary", "catalog"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 数据平台数据字典

数据平台字典来自 `https://quant.10jqka.com.cn/view/dataplatform` 及 101 个 `detail/{id}` 详情页。每个详情页通常包含：字段说明、使用代码、参数说明、使用样例、数据样例。原始解析结果见 `raw/articles/mindgo-dataplatform-detail-docs.json.md`。

## 分类规模

- 风险模型: 1 个数据文档
- 股票: 46 个数据文档
- 基金: 9 个数据文档
- 期货: 11 个数据文档
- 期权: 4 个数据文档
- 外汇: 4 个数据文档
- 因子数据: 2 个数据文档
- 债券: 10 个数据文档
- 指数: 11 个数据文档
- i问财接口: 2 个数据文档
- iFinD数据接口: 1 个数据文档

## 目录页

- 股票类表：[[mindgo-stock-data-dictionary]]
- 期货/期权/T+D：[[mindgo-futures-options-data-dictionary]]
- 基金/债券/指数/外汇：[[mindgo-funds-bonds-index-forex-dictionary]]
- 因子/风险模型/问财/iFinD：[[mindgo-factor-risk-alt-dictionary]]

数据字典负责“有什么字段”和“样例长什么样”；具体函数行为、运行环境限制和策略框架对象应回到 [[mindgo-api-docs]]。如果目标是自动远程取数，则结合 [[mindgo-jupyter-python-execution]]。
