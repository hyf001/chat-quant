---
title: "car_market_fuel_cpca - 乘联会-统计数据-新能源细分市场"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_fuel_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-新能源细分市场
- 描述: 乘联会-统计数据-车型大类
- 目标地址: http://data.cpcadata.com/FuelMarket
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-新能源细分市场

接口: car_market_fuel_cpca

目标地址: http://data.cpcadata.com/FuelMarket

描述: 乘联会-统计数据-车型大类

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                 |
|--------|-----|--------------------------------------------------------------------|
| symbol | str | symbol="整体市场"; choice of {"整体市场", "销量占比-PHEV-BEV", "销量占比-ICE-NEV"} |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | object  | -        |
| {前一个年份}年 | float64 | 注意单位: 万辆 |
| {当前年份}年  | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_fuel_cpca_df = ak.car_market_fuel_cpca()
print(car_market_fuel_cpca_df)
```

数据示例

```
     月份    2023年    2024年
0    1月  33.1542  66.7653
1    2月  43.9068  38.8294
2    3月  54.6472      NaN
3    4月  52.4730      NaN
4    5月  57.9938      NaN
5    6月  66.5066      NaN
6    7月  64.1005      NaN
7    8月  71.6335      NaN
8    9月  74.6305      NaN
9   10月  77.1797      NaN
10  11月  84.0500      NaN
11  12月  94.7347      NaN
```
