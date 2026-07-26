---
title: "car_market_cate_cpca - 乘联会-统计数据-车型大类"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_cate_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-车型大类
- 描述: 乘联会-统计数据-车型大类
- 目标地址: http://data.cpcadata.com/CategoryMarket
- 限量: 单次返回指定 symbol 和 indicator 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-车型大类

接口: car_market_cate_cpca

目标地址: http://data.cpcadata.com/CategoryMarket

描述: 乘联会-统计数据-车型大类

限量: 单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                |
|-----------|-----|---------------------------------------------------|
| symbol    | str | symbol="轿车"; choice of {"轿车", "MPV", "SUV", "占比"} |
| indicator | str | indicator="批发"; choice of {"批发", "零售"}            |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | object  | -        |
| {前一个年份}年 | float64 | 注意单位: 万辆 |
| {当前年份}年  | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_cate_cpca_df = ak.car_market_cate_cpca(symbol="轿车", indicator="批发")
print(car_market_cate_cpca_df)
```

数据示例

```
     月份   2023年    2024年
0    1月   63.2478  87.1795
1    2月   72.2022  54.5316
2    3月   90.4165      NaN
3    4月   79.3741      NaN
4    5月   89.9973      NaN
5    6月   98.1894      NaN
6    7月   91.2119      NaN
7    8月   97.8467      NaN
8    9月  106.0477      NaN
9   10月  105.2851      NaN
10  11月  110.8935      NaN
11  12月  122.1150      NaN
```
