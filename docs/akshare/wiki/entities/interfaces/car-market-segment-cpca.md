---
title: "car_market_segment_cpca - 乘联会-统计数据-级别细分市场"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_segment_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-级别细分市场
- 描述: 乘联会-统计数据-级别细分市场
- 目标地址: http://data.cpcadata.com/SegmentMarket
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-级别细分市场

接口: car_market_segment_cpca

目标地址: http://data.cpcadata.com/SegmentMarket

描述: 乘联会-统计数据-级别细分市场

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                          |
|--------|-----|---------------------------------------------|
| symbol | str | symbol="轿车"; choice of {"轿车", "MPV", "SUV"} |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 月份  | object  | -        |
| A00 | float64 | 注意单位: 万辆 |
| A0  | float64 | 注意单位: 万辆 |
| A   | float64 | 注意单位: 万辆 |
| B   | float64 | 注意单位: 万辆 |
| C   | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_segment_cpca_df = ak.car_market_segment_cpca(symbol="轿车")
print(car_market_segment_cpca_df)
```

数据示例

```
          月份        A00         A0          A          B          C
0    2023-3月   5.456084   8.219518  42.917168  34.389297   9.017934
1    2023-4月   5.164784  10.342795  44.179653  30.211243  10.101533
2    2023-5月   4.764809   9.978744  46.005154  28.248846  11.002440
3    2023-6月   4.684416   9.713371  44.913500  30.345741  10.342969
4    2023-7月   4.699168  10.649708  45.020990  28.368778  11.261360
5    2023-8月   4.059616  11.460070  45.084000  29.152237  10.244087
6    2023-9月   7.940861   7.592339  43.092026  30.093441  11.281339
7   2023-10月   9.530694   8.313237  42.630062  28.593506  10.932507
8   2023-11月  11.200026   8.195070  40.859290  29.682444  10.063169
9   2023-12月  12.457766   8.930598  37.996150  30.184662  10.430823
10   2024-1月   9.581266   5.019070  41.158417  35.134407   9.106843
11   2024-2月   7.976292   7.585693  36.759968  36.646090  11.031953
```
