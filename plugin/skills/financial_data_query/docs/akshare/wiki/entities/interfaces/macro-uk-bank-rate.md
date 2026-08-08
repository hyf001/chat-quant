---
title: "macro_uk_bank_rate - 央行公布利率决议"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_bank_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 央行公布利率决议
- 描述: 东方财富-经济数据-英国-央行公布利率决议
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_3.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 央行公布利率决议

接口: macro_uk_bank_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_4_3.html

描述: 东方财富-经济数据-英国-央行公布利率决议

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

macro_uk_bank_rate_df = ak.macro_uk_bank_rate()
print(macro_uk_bank_rate_df)
```

数据示例

```
      时间    前值    现值        发布日期
0    2008年01月   NaN  5.50  2008-01-15
1    2008年02月  5.50  5.25  2008-02-15
2    2008年03月  5.25  5.25  2008-03-15
3    2008年04月  5.25  5.00  2008-04-15
4    2008年05月  5.00  5.00  2008-05-15
..        ...   ...   ...         ...
150  2022年05月  0.75  1.00  2022-05-05
151  2022年06月  1.00  1.25  2022-06-16
152  2022年08月  1.25  1.75  2022-08-04
153  2022年09月  1.75  2.25  2022-09-22
154  2022年11月  2.25  3.00  2022-11-03
```
