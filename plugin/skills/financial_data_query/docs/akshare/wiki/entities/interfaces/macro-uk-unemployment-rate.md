---
title: "macro_uk_unemployment_rate - 失业率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_unemployment_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 失业率
- 描述: 东方财富-经济数据-英国-失业率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_14.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 失业率

接口: macro_uk_unemployment_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_4_14.html

描述: 东方财富-经济数据-英国-失业率

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

macro_uk_unemployment_rate_df = ak.macro_uk_unemployment_rate()
print(macro_uk_unemployment_rate_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2008年01月  5.19  5.21  2008-02-16
1    2008年02月  5.21  5.21  2008-03-18
2    2008年03月  5.21  5.20  2008-04-16
3    2008年04月  5.20  5.30  2008-05-17
4    2008年05月  5.30  5.20  2008-06-16
..        ...   ...   ...         ...
172  2022年05月  3.80  3.80  2022-07-19
173  2022年06月  3.80  3.80  2022-08-16
174  2022年07月  3.80  3.60  2022-09-13
175  2022年08月  3.60  3.50  2022-10-11
176  2022年09月  3.50   NaN  2022-11-15
```
