---
title: "macro_euro_sentix_investor_confidence - 欧元区Sentix投资者信心指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_sentix_investor_confidence

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 领先指标 > 欧元区Sentix投资者信心指数报告
- 描述: 欧元区 Sentix 投资者信心指数报告, 数据区间从 20020801-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_sentix_investor_confidence
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区Sentix投资者信心指数报告

接口: macro_euro_sentix_investor_confidence

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_sentix_investor_confidence

描述: 欧元区 Sentix 投资者信心指数报告, 数据区间从 20020801-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_euro_sentix_investor_confidence_df = ak.macro_euro_sentix_investor_confidence()
print(macro_euro_sentix_investor_confidence_df)
```

数据示例

```
                   商品          日期    今值   预测值    前值
0    欧元区Sentix投资者信心指数  2002-08-01  13.0   NaN   NaN
1    欧元区Sentix投资者信心指数  2002-10-01  -8.5   NaN  13.0
2    欧元区Sentix投资者信心指数  2003-02-01 -21.8   NaN  -8.5
3    欧元区Sentix投资者信心指数  2003-03-01 -22.8   NaN -21.8
4    欧元区Sentix投资者信心指数  2003-04-01 -19.4   NaN -22.8
..                ...         ...   ...   ...   ...
239  欧元区Sentix投资者信心指数  2022-07-04 -26.4 -19.9 -15.8
240  欧元区Sentix投资者信心指数  2022-08-08 -25.2 -24.7 -26.4
241  欧元区Sentix投资者信心指数  2022-09-05 -31.8 -27.5 -25.2
242  欧元区Sentix投资者信心指数  2022-10-10 -38.3 -34.7 -31.8
243  欧元区Sentix投资者信心指数  2022-11-07   NaN -34.7 -38.3
```
