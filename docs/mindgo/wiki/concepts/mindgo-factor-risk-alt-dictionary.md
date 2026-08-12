---
title: MindGo 因子风险问财数据字典
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-dictionary", "factors", "risk-model", "iwencai", "ifind", "catalog"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 因子风险问财数据字典

本页汇总风险模型、因子数据、i问财接口和 iFinD 数据接口。因子函数可结合 [[mindgo-security-reference-api]] 的 `get_sfactor_data`；问财使用方式见 [[mindgo-iwencai-api]]。

| ID | 名称 | 分类 | 字段数 | 代码块 | 主要调用 |
| --- | --- | --- | ---: | ---: | --- |
| 244 | CNE5风险模型 | 风险模型 / CNE5风险模型 | 0 | 3 | #获取因子暴露度数据<br>#获取因子收益数据 |
| 285 | 技术因子 | 因子数据 | 61 | 2 | run_query(query_object)<br>#获取2023年2月1日全市场股票的因子数据 |
| 289 | 基本面因子 | 因子数据 | 66 | 2 | run_query(query_object)<br>#获取2023年2月1日全市场股票的因子数据 |
| 398 | query_iwencai | i问财接口 | 0 | 0 |  |
| 399 | get_iwencai | i问财接口 | 0 | 0 |  |
| 419 | iFinD数据接口 | iFinD数据接口 | 0 | 0 |  |
