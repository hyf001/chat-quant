---
title: "macro_canada_trade - 贸易帐"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_trade

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 贸易帐
- 描述: 东方财富-经济数据-加拿大-贸易帐
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 贸易帐

接口: macro_canada_trade

目标地址: http://data.eastmoney.com/cjsj/foreign_7_2.html

描述: 东方财富-经济数据-加拿大-贸易帐

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 时间   | object  | -         |
| 前值   | float64 | 注意单位: 亿加元 |
| 现值   | float64 | 注意单位: 亿加元 |
| 发布日期 | object  | -         |

接口示例

```python
import akshare as ak

macro_canada_trade_df = ak.macro_canada_trade()
print(macro_canada_trade_df)
```

数据示例

```
       时间    前值      现值        发布日期
0    2022年10月  1138     NaN  2022-12-06
1    2022年09月   550  1138.0  2022-11-03
2    2022年08月  2373   550.0  2022-10-05
3    2022年07月  4881  2373.0  2022-09-07
4    2022年06月  4769  4881.0  2022-08-04
..        ...   ...     ...         ...
173  2008年05月  5110  5540.0  2008-07-06
174  2008年04月  5530  5110.0  2008-06-06
175  2008年03月  4940  5530.0  2008-05-06
176  2008年02月  3260  4940.0  2008-04-07
177  2008年01月  2350  3260.0  2008-03-07
```
