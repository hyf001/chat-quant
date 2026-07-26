---
title: "index_news_sentiment_scope - A 股新闻情绪指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_news_sentiment_scope

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 市场情绪指数 > A 股新闻情绪指数
- 描述: 数库-A股新闻情绪指数
- 目标地址: https://www.chinascope.com/reasearch.html
- 限量: 该接口返回近一年的 A 股新闻情绪指数数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### A 股新闻情绪指数

接口: index_news_sentiment_scope

目标地址: https://www.chinascope.com/reasearch.html

描述: 数库-A股新闻情绪指数

限量: 该接口返回近一年的 A 股新闻情绪指数数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 日期      | object  | -  |
| 市场情绪指数  | float64 | -  |
| 沪深300指数 | float64 | -  |

接口示例

```python
import akshare as ak

index_news_sentiment_scope_df = ak.index_news_sentiment_scope()
print(index_news_sentiment_scope_df)
```

数据示例

```
        日期    市场情绪指数  沪深300指数
0    2023-10-31  0.986883  3607.2454
1    2023-11-01  0.995480  3607.2454
2    2023-11-02  1.005612  3607.2454
3    2023-11-03  1.017992  3607.2454
4    2023-11-06  1.017223  3607.2454
..          ...       ...        ...
236  2024-10-25  0.996452  3956.4210
237  2024-10-28  1.001457  3964.1569
238  2024-10-29  1.008418  3924.6490
239  2024-10-30  1.004648  3889.4487
240  2024-10-31  1.007300  3891.0396
[241 rows x 3 columns]
```
