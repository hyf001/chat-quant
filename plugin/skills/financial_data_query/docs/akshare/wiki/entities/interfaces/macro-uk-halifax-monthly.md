---
title: "macro_uk_halifax_monthly - Halifax 房价指数月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_halifax_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > Halifax 房价指数月率
- 描述: 东方财富-经济数据-英国-Halifax 房价指数月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### Halifax 房价指数月率

接口: macro_uk_halifax_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_0.html

描述: 东方财富-经济数据-英国-Halifax 房价指数月率

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

macro_uk_halifax_monthly_df = ak.macro_uk_halifax_monthly()
print(macro_uk_halifax_monthly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2008年01月  NaN -0.4  2008-02-07
1    2008年02月 -0.4  0.1  2008-03-09
2    2008年03月  0.1 -2.5  2008-04-07
3    2008年04月 -2.5 -1.5  2008-05-08
4    2008年05月 -1.5 -2.5  2008-06-07
..        ...  ...  ...         ...
174  2022年07月  1.4 -0.1  2022-08-05
175  2022年08月 -0.1  0.3  2022-09-07
176  2022年09月  0.3 -0.1  2022-10-07
177  2022年10月 -0.1 -0.4  2022-11-07
178  2022年11月 -0.4  NaN  2022-12-07
```
