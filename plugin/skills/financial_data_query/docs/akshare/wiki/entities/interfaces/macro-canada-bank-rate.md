---
title: "macro_canada_bank_rate - 央行公布利率决议"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_bank_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 央行公布利率决议
- 描述: 东方财富-经济数据-加拿大-央行公布利率决议
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 央行公布利率决议

接口: macro_canada_bank_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_7_4.html

描述: 东方财富-经济数据-加拿大-央行公布利率决议

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

macro_canada_bank_rate_df = ak.macro_canada_bank_rate()
print(macro_canada_bank_rate_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2022年12月  3.75   NaN  2022-12-07
1    2022年10月  3.25  3.75  2022-10-26
2    2022年09月  2.50  3.25  2022-09-07
3    2022年07月  1.50  2.50  2022-07-13
4    2022年06月  1.00  1.50  2022-06-01
..        ...   ...   ...         ...
145  2008年05月  3.00  3.00  2008-05-15
146  2008年04月  3.50  3.00  2008-04-15
147  2008年03月  4.00  3.50  2008-03-15
148  2008年02月  4.00  4.00  2008-02-15
149  2008年01月   NaN  4.00  2008-01-15
```
