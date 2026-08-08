---
title: "macro_usa_initial_jobless - 美国初请失业金人数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_initial_jobless

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 其他 > 美国初请失业金人数报告
- 描述: 美国初请失业金人数报告, 数据区间从 19700101-至今
- 目标地址: https://cdn.jin10.com/dc/reports/dc_usa_michigan_consumer_sentiment_all.js?v=1578576228
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国初请失业金人数报告

接口: macro_usa_initial_jobless

目标地址: https://cdn.jin10.com/dc/reports/dc_usa_michigan_consumer_sentiment_all.js?v=1578576228

描述: 美国初请失业金人数报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 商品  | object  | -        |
| 日期  | object  | -        |
| 今值  | float64 | 注意单位: 万人 |
| 预测值 | float64 | 注意单位: 万人 |
| 前值  | float64 | 注意单位: 万人 |

接口示例

```python
import akshare as ak

macro_usa_initial_jobless_df = ak.macro_usa_initial_jobless()
print(macro_usa_initial_jobless_df)
```

数据示例

```
             商品          日期      今值   预测值      前值
0     美国初请失业金人数  1970-01-01  22.109   NaN     NaN
1     美国初请失业金人数  1970-02-01  24.932   NaN  22.109
2     美国初请失业金人数  1970-03-01  25.850   NaN  24.932
3     美国初请失业金人数  1970-04-01  26.868   NaN  25.850
4     美国初请失业金人数  1970-05-01  33.159   NaN  26.868
         ...         ...     ...   ...     ...
1293  美国初请失业金人数  2024-03-14  20.900  21.8  21.000
1294  美国初请失业金人数  2024-03-21  21.000  21.2  21.200
1295  美国初请失业金人数  2024-03-28  21.000  21.2  21.200
1296  美国初请失业金人数  2024-04-04  22.100  21.3  21.200
1297  美国初请失业金人数  2024-04-11     NaN   NaN  22.100
[1298 rows x 5 columns]
```
