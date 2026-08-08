---
title: "macro_china_new_financial_credit - 新增信贷数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_new_financial_credit

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 新增信贷数据
- 描述: 中国新增信贷数据数据, 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/xzxd.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 新增信贷数据

接口: macro_china_new_financial_credit

目标地址: http://data.eastmoney.com/cjsj/xzxd.html

描述: 中国新增信贷数据数据, 数据区间从 200801 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 月份      | object  | -        |
| 当月      | float64 | 注意单位: 亿元 |
| 当月-同比增长 | float64 | 注意单位: %  |
| 当月-环比增长 | float64 | 注意单位: %  |
| 累计      | float64 | 注意单位: 亿元 |
| 累计-同比增长 | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_new_financial_credit_df = ak.macro_china_new_financial_credit()
print(macro_china_new_financial_credit_df)
```

数据示例

```
     月份       当月    当月-同比增长      当月-环比增长        累计    累计-同比增长
0    2022年10月份   4431.0 -42.840557   -82.749358  183298.0   4.127067
1    2022年09月份  25686.0  44.669107    92.491007  178867.0   6.290669
2    2022年08月份  13344.0   4.963423   226.418787  153181.0   1.763815
3    2022年07月份   4088.0 -51.281135   -86.614276  139837.0   1.468657
4    2022年06月份  30540.0  31.740143    67.526056  135749.0   4.888659
..         ...      ...        ...          ...       ...        ...
173  2008年05月份   3185.0  28.790942   -32.089552   21201.0   1.386830
174  2008年04月份   4690.0  11.137441    65.490473   18016.0  -2.288751
175  2008年03月份   2834.0 -35.838805    16.433854   13326.0  -6.273738
176  2008年02月份   2434.0 -41.179314   -69.793994   10492.0   7.050301
177  2008年01月份   8058.0  42.292071  1561.443299    8058.0  42.292071
```
