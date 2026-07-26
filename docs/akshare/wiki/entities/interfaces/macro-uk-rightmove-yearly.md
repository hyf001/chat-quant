---
title: "macro_uk_rightmove_yearly - Rightmove 房价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_rightmove_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > Rightmove 房价指数年率
- 描述: 东方财富-经济数据-英国-Rightmove 房价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_10.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### Rightmove 房价指数年率

接口: macro_uk_rightmove_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_10.html

描述: 东方财富-经济数据-英国-Rightmove 房价指数年率

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

macro_uk_rightmove_yearly_df = ak.macro_uk_rightmove_yearly()
print(macro_uk_rightmove_yearly_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2008年01月   NaN   3.4  2008-01-20
1    2008年02月   3.4   5.8  2008-02-20
2    2008年03月   5.8   5.0  2008-03-20
3    2008年04月   5.0   1.3  2008-04-20
4    2008年05月   1.3   2.2  2008-05-20
..        ...   ...   ...         ...
148  2022年05月   9.9  10.2  2022-05-24
149  2022年06月  10.2   9.7  2022-06-20
150  2022年07月   9.7   9.3  2022-07-18
151  2022年08月   9.3   8.2  2022-08-16
152  2022年09月   8.2   8.7  2022-09-26
```
