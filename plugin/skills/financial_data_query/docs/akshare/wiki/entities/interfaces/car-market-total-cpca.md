---
title: "car_market_total_cpca - 乘联会-统计数据-总体市场"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_total_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-总体市场
- 描述: 乘联会-统计数据-总体市场
- 目标地址: http://data.cpcadata.com/TotalMarket
- 限量: 单次返回指定 symbol 和 indicator 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-总体市场

接口: car_market_total_cpca

目标地址: http://data.cpcadata.com/TotalMarket

描述: 乘联会-统计数据-总体市场

限量: 单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                 |
|-----------|-----|----------------------------------------------------|
| symbol    | str | symbol="狭义乘用车"; choice of {"狭义乘用车", "广义乘用车"}       |
| indicator | str | indicator="产量"; choice of {"产量", "批发", "零售", "出口"} |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | object  | -        |
| {前一个年份}年 | float64 | 注意单位: 万辆 |
| {当前年份}年  | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_total_cpca_df = ak.car_market_total_cpca(symbol="狭义乘用车", indicator="产量")
print(car_market_total_cpca_df)
```

数据示例

```
     月份   2023年     2024年
0    1月  134.6266  202.0941
1    2月  166.4180  123.4852
2    3月  208.7694       NaN
3    4月  172.8825       NaN
4    5月  198.9448       NaN
5    6月  219.4569       NaN
6    7月  208.9492       NaN
7    8月  223.7048       NaN
8    9月  243.6938       NaN
9   10月  244.8691       NaN
10  11月  264.3703       NaN
11  12月  267.8423       NaN
```
