---
title: "macro_euro_zew_economic_sentiment - 欧元区ZEW经济景气指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_zew_economic_sentiment

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 领先指标 > 欧元区ZEW经济景气指数报告
- 描述: 欧元区 ZEW 经济景气指数报告, 数据区间从 20080212-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_zew_economic_sentiment
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区ZEW经济景气指数报告

接口: macro_euro_zew_economic_sentiment

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_zew_economic_sentiment

描述: 欧元区 ZEW 经济景气指数报告, 数据区间从 20080212-至今

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

macro_euro_zew_economic_sentiment_df = ak.macro_euro_zew_economic_sentiment()
print(macro_euro_zew_economic_sentiment_df)
```

数据示例

```
               商品          日期    今值   预测值    前值
0    欧元区ZEW经济景气指数  2008-02-12 -41.4 -43.0 -41.7
1    欧元区ZEW经济景气指数  2008-03-11 -35.0 -42.0 -41.4
2    欧元区ZEW经济景气指数  2008-04-15 -44.8 -33.0 -35.0
3    欧元区ZEW经济景气指数  2008-05-20 -43.6 -44.2 -44.8
4    欧元区ZEW经济景气指数  2008-06-17 -52.7 -43.9 -43.6
..            ...         ...   ...   ...   ...
174  欧元区ZEW经济景气指数  2022-07-12  51.1   NaN -28.0
175  欧元区ZEW经济景气指数  2022-08-16 -54.9 -57.0 -51.1
176  欧元区ZEW经济景气指数  2022-09-13 -60.7 -58.3 -54.9
177  欧元区ZEW经济景气指数  2022-10-18 -59.7 -61.2 -60.7
178  欧元区ZEW经济景气指数  2022-11-15   NaN   NaN -59.7
```
