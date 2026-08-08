---
title: "car_market_country_cpca - 乘联会-统计数据-国别细分市场"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_country_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-国别细分市场
- 描述: 乘联会-统计数据-国别细分市场
- 目标地址: http://data.cpcadata.com/CountryMarket
- 限量: 单次返回指定 symbol 和 indicator 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-国别细分市场

接口: car_market_country_cpca

目标地址: http://data.cpcadata.com/CountryMarket

描述: 乘联会-统计数据-国别细分市场

限量: 单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 月份   | object  | -        |
| 自主   | float64 | 注意单位: 万辆 |
| 德系   | float64 | 注意单位: 万辆 |
| 日系   | float64 | 注意单位: 万辆 |
| 法系   | float64 | 注意单位: 万辆 |
| 美系   | float64 | 注意单位: 万辆 |
| 韩系   | float64 | 注意单位: 万辆 |
| 其他欧系 | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_country_cpca_df = ak.car_market_country_cpca()
print(car_market_country_cpca_df)
```

数据示例

```
     月份         自主      德系  ...        美系       韩系     其他欧系
0    2023-3月  52.937614  18.783411  ...  8.944649  1.841395  0.656085
1    2023-4月  56.117973  17.591091  ...  9.997354  1.454204  0.767231
2    2023-5月  54.849330  17.672825  ...  9.739207  1.441945  0.856578
3    2023-6月  53.630800  18.637491  ...  9.731017  1.782815  0.873428
4    2023-7月  58.120550  17.234150  ...  8.402960  1.375989  0.825758
5    2023-8月  57.429867  17.205738  ...  8.894298  1.640349  0.783967
6    2023-9月  56.517770  17.429178  ...  8.500368  1.590704  0.753809
7   2023-10月  59.985280  15.645699  ...  7.352488  1.470236  0.694709
8   2023-11月  59.638090  16.112440  ...  7.439157  1.567490  0.624859
9   2023-12月  57.890274  17.040712  ...  8.136273  1.738795  0.650838
10   2024-1月  60.437893  17.406410  ...  6.315318  1.404617  0.804964
11   2024-2月  60.124140  17.637665  ...  6.854863  1.837663  0.695454
[12 rows x 8 columns]
```
