---
title: "macro_uk_core_cpi_yearly - 核心消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_core_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 核心消费者物价指数年率
- 描述: 东方财富-经济数据-英国-核心消费者物价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 核心消费者物价指数年率

接口: macro_uk_core_cpi_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_4.html

描述: 东方财富-经济数据-英国-核心消费者物价指数年率

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

macro_uk_core_cpi_yearly_df = ak.macro_uk_core_cpi_yearly()
print(macro_uk_core_cpi_yearly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2008年01月  1.4  1.3  2008-02-16
1    2008年02月  1.3  1.2  2008-03-18
2    2008年03月  1.2  1.2  2008-04-16
3    2008年04月  1.2  1.4  2008-05-17
4    2008年05月  1.4  1.5  2008-06-16
..        ...  ...  ...         ...
172  2022年05月  6.2  5.9  2022-06-22
173  2022年06月  5.9  5.8  2022-07-20
174  2022年07月  5.8  6.2  2022-08-17
175  2022年08月  6.2  6.3  2022-09-14
176  2022年09月  6.3  6.5  2022-10-19
```
