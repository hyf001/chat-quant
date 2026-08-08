---
title: "macro_uk_cpi_monthly - 消费者物价指数月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_cpi_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 消费者物价指数月率
- 描述: 东方财富-经济数据-英国-消费者物价指数月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_7.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数月率

接口: macro_uk_cpi_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_7.html

描述: 东方财富-经济数据-英国-消费者物价指数月率

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 前值   | float64 | -   |
| 现值   | float64 | -   |
| 发布日期 | object  | -   |

接口示例

```python
import akshare as ak

macro_uk_cpi_monthly_df = ak.macro_uk_cpi_monthly()
print(macro_uk_cpi_monthly_df)
```

数据示例

```
      时间   前值   现值        发布日期
0    2008年01月  0.6 -1.0  2008-02-16
1    2008年02月 -1.0  0.3  2008-03-18
2    2008年03月  0.3  0.4  2008-04-16
3    2008年04月  0.4  0.5  2008-05-17
4    2008年05月  0.5  0.3  2008-06-16
..        ...  ...  ...         ...
170  2022年05月  0.7  0.5  2022-06-22
171  2022年06月  0.5  0.4  2022-07-20
172  2022年07月  0.4  0.3  2022-08-17
173  2022年08月  0.3  0.8  2022-09-14
174  2022年09月  0.8  0.6  2022-10-19
```
