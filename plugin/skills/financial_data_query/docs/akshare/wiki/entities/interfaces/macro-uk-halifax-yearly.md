---
title: "macro_uk_halifax_yearly - Halifax 房价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_halifax_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > Halifax 房价指数年率
- 描述: 东方财富-经济数据-英国-Halifax 房价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_1.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### Halifax 房价指数年率

接口: macro_uk_halifax_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_1.html

描述: 东方财富-经济数据-英国-Halifax 房价指数年率

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

macro_uk_halifax_yearly_df = ak.macro_uk_halifax_yearly()
print(macro_uk_halifax_yearly_df)
```

数据示例

```
      时间    前值    现值        发布日期
0    2008年01月   5.2   4.5  2008-02-07
1    2008年02月   4.5   4.2  2008-03-09
2    2008年03月   4.2   1.1  2008-04-07
3    2008年04月   1.1  -0.9  2008-05-08
4    2008年05月  -0.9  -3.8  2008-06-07
..        ...   ...   ...         ...
174  2022年07月  12.5  11.8  2022-08-05
175  2022年08月  11.8  11.4  2022-09-07
176  2022年09月  11.4   9.8  2022-10-07
177  2022年10月   9.8   8.3  2022-11-07
178  2022年11月   8.3   NaN  2022-12-07
```
