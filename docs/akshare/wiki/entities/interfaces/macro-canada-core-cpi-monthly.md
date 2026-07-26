---
title: "macro_canada_core_cpi_monthly - 核心消费者物价指数月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_core_cpi_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 核心消费者物价指数月率
- 描述: 东方财富-经济数据-加拿大-核心消费者物价指数月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_6.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 核心消费者物价指数月率

接口: macro_canada_core_cpi_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_7_6.html

描述: 东方财富-经济数据-加拿大-核心消费者物价指数月率

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 前值   | float64 | 注意单位: % |
| 现值   | float64 | 注意单位: % |
| 发布日期 | object  | -       |

接口示例

```python
import akshare as ak

macro_canada_core_cpi_monthly_df = ak.macro_canada_core_cpi_monthly()
print(macro_canada_core_cpi_monthly_df)
```

数据示例

```
     时间        前值        现值        发布日期
0    2022年11月  0.400000       NaN  2022-12-21
1    2022年10月  0.400000  0.400000  2022-11-16
2    2022年09月  0.000000  0.400000  2022-10-19
3    2022年08月  0.500000  0.000000  2022-09-20
4    2022年07月  0.300000  0.500000  2022-08-16
..        ...       ...       ...         ...
173  2008年05月  0.270514  0.269784  2008-06-21
174  2008年04月  0.180668  0.270514  2008-05-22
175  2008年03月  0.544959  0.180668  2008-04-21
176  2008年02月  0.090909  0.544959  2008-03-23
177  2008年01月 -0.271985  0.090909  2008-02-21
```
