---
title: "macro_china_czsr - 财政收入"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_czsr

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 财政收入
- 描述: 中国财政收入, 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/czsr.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 财政收入

接口: macro_china_czsr

目标地址: http://data.eastmoney.com/cjsj/czsr.html

描述: 中国财政收入, 数据区间从 200801 至今, 月度数据

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

macro_china_czsr_df = ak.macro_china_czsr()
print(macro_china_czsr_df)
```

数据示例

```
       月份         当月    当月-同比增长  当月-环比增长  累计  累计-同比增长
0    2008年01月份   7396.64  42.352305  135.212710    7396.64     42.4
1    2008年02月份   4158.75  36.552139  -43.775147   11555.39     40.2
2    2008年03月份   4415.95  24.671449    6.184551   15971.34     35.5
3    2008年04月份   6824.88  17.016465   54.550663   22796.22     29.4
4    2008年05月份   6268.15  52.602556   -8.157360   29064.37     33.8
..         ...       ...        ...         ...        ...      ...
201  2025年05月份  16007.00   0.131365  -21.638028   96623.00     -0.3
202  2025年06月份  18943.00  -0.305247   18.341975  115566.00     -0.3
203  2025年07月份  20273.00   2.648101    7.021063  135839.00      0.1
204  2025年08月份  12359.00   2.030876  -39.037143  148198.00      0.3
205  2025年09月份  15678.00   2.584571   26.854924  163876.00      0.5
[206 rows x 6 columns]
```
