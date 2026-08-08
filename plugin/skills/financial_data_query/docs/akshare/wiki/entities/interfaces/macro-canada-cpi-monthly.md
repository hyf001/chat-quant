---
title: "macro_canada_cpi_monthly - 消费者物价指数月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_cpi_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 消费者物价指数月率
- 描述: 东方财富-经济数据-加拿大-消费者物价指数月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_8.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数月率

接口: macro_canada_cpi_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_7_8.html

描述: 东方财富-经济数据-加拿大-消费者物价指数月率

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

macro_canada_cpi_monthly_df = ak.macro_canada_cpi_monthly()
print(macro_canada_cpi_monthly_df)
```

数据示例

```
           时间        前值        现值        发布日期
0    2022年10月  0.065531  0.720367  2022-11-16
1    2022年09月 -0.326584  0.065531  2022-10-19
2    2022年08月  0.130804 -0.326584  2022-09-20
3    2022年07月  0.658328  0.130804  2022-08-16
4    2022年06月  1.401869  0.658328  2022-07-20
..        ...       ...       ...         ...
172  2008年05月  0.799290  0.969163  2008-06-20
173  2008年04月  0.356506  0.799290  2008-05-21
174  2008年03月  0.357782  0.356506  2008-04-20
175  2008年02月 -0.178571  0.357782  2008-03-22
176  2008年01月  0.089366 -0.178571  2008-02-20
```
