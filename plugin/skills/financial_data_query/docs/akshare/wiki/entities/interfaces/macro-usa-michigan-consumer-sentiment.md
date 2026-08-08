---
title: "macro_usa_michigan_consumer_sentiment - 美国密歇根大学消费者信心指数初值报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_michigan_consumer_sentiment

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 领先指标 > 美国密歇根大学消费者信心指数初值报告
- 描述: 美国密歇根大学消费者信心指数初值报告, 数据区间从 19700301-至今
- 目标地址: https://cdn.jin10.com/dc/reports/dc_usa_michigan_consumer_sentiment_all.js?v=1578576228
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国密歇根大学消费者信心指数初值报告

接口: macro_usa_michigan_consumer_sentiment

目标地址: https://cdn.jin10.com/dc/reports/dc_usa_michigan_consumer_sentiment_all.js?v=1578576228

描述: 美国密歇根大学消费者信心指数初值报告, 数据区间从 19700301-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 商品  | object  | -  |
| 日期  | object  | -  |
| 今值  | float64 | -  |
| 预测值 | float64 | -  |
| 前值  | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_michigan_consumer_sentiment_df = ak.macro_usa_michigan_consumer_sentiment()
print(macro_usa_michigan_consumer_sentiment_df)
```

数据示例

```
                     商品          日期    今值   预测值    前值
0    美国密歇根大学消费者信心指数初值报告  1970-03-01  78.1   NaN   NaN
1    美国密歇根大学消费者信心指数初值报告  1970-06-01  75.4   NaN  78.1
2    美国密歇根大学消费者信心指数初值报告  1970-09-01  77.6   NaN  75.4
3    美国密歇根大学消费者信心指数初值报告  1970-12-01  72.4   NaN  77.6
4    美国密歇根大学消费者信心指数初值报告  1971-03-01  78.1   NaN  72.4
..                  ...         ...   ...   ...   ...
772  美国密歇根大学消费者信心指数初值报告  2024-02-16  79.6  80.0  79.0
773  美国密歇根大学消费者信心指数初值报告  2024-03-01  76.9  79.6  79.0
774  美国密歇根大学消费者信心指数初值报告  2024-03-15  76.5  77.1  76.9
775  美国密歇根大学消费者信心指数初值报告  2024-03-28  79.4  76.5  76.9
776  美国密歇根大学消费者信心指数初值报告  2024-04-12   NaN   NaN  79.4
[777 rows x 5 columns]
```
