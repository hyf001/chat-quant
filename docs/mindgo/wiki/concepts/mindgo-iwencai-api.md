---
title: MindGo 问财 API
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "api", "iwencai"]
sources: ["raw/articles/mindgo-api-docs-help-4.md", "raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 问财 API

问财接口把自然语言选股接入 MindGo，但 `query_iwencai` 和 `get_iwencai` 的服务侧重点不同。

| 函数 | 适合环境 | 返回/副作用 | 典型用途 |
| --- | --- | --- | --- |
| `query_iwencai(query, domain='股票', timeout=6, df=True)` | 研究环境 | DataFrame 或 list | 实时自然语言选股、快速验证想法 |
| `get_iwencai(question, set_attr='iwencai_securities', version=None)` | 回测环境 init | 无直接返回，写入 context 属性 | 历史回测中的每日选股池 |

API 文档提醒：问财诞生场景偏实时选股，不是为回测天然设计；回测使用时应注意未来函数和语句可用性。数据平台也有 `query_iwencai` 与 `get_iwencai` 两个文档条目，见 [[mindgo-factor-risk-alt-dictionary]]。

若想快速回答“某个自然语言选股能不能用”，先看 [[mindgo-api-docs]]，再用 [[mindgo-jupyter-python-execution]] 在研究环境中小样本验证。
