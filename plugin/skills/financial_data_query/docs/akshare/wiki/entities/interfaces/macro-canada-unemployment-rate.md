---
title: "macro_canada_unemployment_rate - 失业率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_unemployment_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 失业率
- 描述: 东方财富-经济数据-加拿大-失业率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_1.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 失业率

接口: macro_canada_unemployment_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_7_1.html

描述: 东方财富-经济数据-加拿大-失业率

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

macro_canada_unemployment_rate_df = ak.macro_canada_unemployment_rate()
print(macro_canada_unemployment_rate_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2022年11月  5.2  NaN  2022-12-02
1    2022年10月  5.2  5.2  2022-11-04
2    2022年09月  5.4  5.2  2022-10-07
3    2022年08月  4.9  5.4  2022-09-09
4    2022年07月  4.9  4.9  2022-08-05
..        ...  ...  ...         ...
174  2008年05月  6.1  6.1  2008-06-08
175  2008年04月  6.0  6.1  2008-05-09
176  2008年03月  5.8  6.0  2008-04-08
177  2008年02月  5.8  5.8  2008-03-10
178  2008年01月  5.9  5.8  2008-02-08
```
