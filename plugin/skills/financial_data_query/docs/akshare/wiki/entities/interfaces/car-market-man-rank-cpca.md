---
title: "car_market_man_rank_cpca - 乘联会-统计数据-厂商排名"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# car_market_man_rank_cpca

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 汽车销量排行 > 乘联会-统计数据-厂商排名
- 描述: 乘联会-统计数据-厂商排名
- 目标地址: http://data.cpcadata.com/ManRank
- 限量: 单次返回指定 symbol 和 indicator 的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 乘联会-统计数据-厂商排名

接口: car_market_man_rank_cpca

目标地址: http://data.cpcadata.com/ManRank

描述: 乘联会-统计数据-厂商排名

限量: 单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                                            |
|-----------|-----|-------------------------------------------------------------------------------|
| symbol    | str | symbol="狭义乘用车-单月"; choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"} |
| indicator | str | indicator="批发"; choice of {"批发", "零售"}                                        |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | object  | -        |
| {前一个年份}年 | float64 | 注意单位: 万辆 |
| {当前年份}年  | float64 | 注意单位: 万辆 |

接口示例

```python
import akshare as ak

car_market_man_rank_cpca_df = ak.car_market_man_rank_cpca(symbol="狭义乘用车-单月", indicator="批发")
print(car_market_man_rank_cpca_df)
```

数据示例

```
       厂商  2023年2月  2024年2月
0    奇瑞汽车   9.6553  13.7819
1   比亚迪汽车  19.1664  12.1748
2    吉利汽车  10.8701  11.1398
3    一汽大众  10.5007   8.4073
4    长安汽车  11.6407   8.3550
5    上汽大众   7.3303   6.3003
6    长城汽车   5.1053   6.0550
7   特斯拉中国   7.4402   6.0365
8  上汽通用五菱   3.7029   4.9366
9    华晨宝马   5.2871   4.1604
```
