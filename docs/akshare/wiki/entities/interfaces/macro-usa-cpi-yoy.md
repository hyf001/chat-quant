---
title: "macro_usa_cpi_yoy - 美国CPI年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cpi_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 物价水平 > 美国CPI年率报告
- 描述: 东方财富-经济数据一览-美国-CPI年率, 数据区间从2008-至今
- 目标地址: https://data.eastmoney.com/cjsj/foreign_0_12.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国CPI年率报告

接口: macro_usa_cpi_yoy

目标地址: https://data.eastmoney.com/cjsj/foreign_0_12.html

描述: 东方财富-经济数据一览-美国-CPI年率, 数据区间从2008-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 发布日期 | object  | -       |
| 现值   | float64 | 注意单位: % |
| 前值   | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_usa_cpi_yoy_df = ak.macro_usa_cpi_yoy()
print(macro_usa_cpi_yoy_df)
```

数据示例

```
       时间        发布日期   现值   前值
0    2008-01-01  2008-02-14  4.3  4.1
1    2008-02-01  2008-03-16  4.0  4.3
2    2008-03-01  2008-04-14  4.0  4.0
3    2008-04-01  2008-05-15  3.9  4.0
4    2008-05-01  2008-06-14  4.2  3.9
..          ...         ...  ...  ...
181  2023-03-01  2023-04-12  5.0  6.0
182  2023-04-01  2023-05-10  4.9  5.0
183  2023-05-01  2023-06-13  4.0  4.9
184  2023-06-01  2023-07-12  3.0  4.0
185  2023-07-01  2023-08-10  NaN  3.0
[186 rows x 4 columns]
```
