---
title: "macro_uk_cpi_yearly - 消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 消费者物价指数年率
- 描述: 东方财富-经济数据-英国-消费者物价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_6.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数年率

接口: macro_uk_cpi_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_6.html

描述: 东方财富-经济数据-英国-消费者物价指数年率

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

macro_uk_cpi_yearly_df = ak.macro_uk_cpi_yearly()
print(macro_uk_cpi_yearly_df)
```

数据示例

```
           时间         前值         现值        发布日期
0    2008年01月   2.115385   2.228682  2008-02-16
1    2008年02月   2.228682   2.507232  2008-03-18
2    2008年03月   2.507232   2.399232  2008-04-16
3    2008年04月   2.399232   2.966507  2008-05-17
4    2008年05月   2.966507   3.339695  2008-06-16
..        ...        ...        ...         ...
172  2022年05月   9.000000   9.100000  2022-06-22
173  2022年06月   9.100000   9.400000  2022-07-20
174  2022年07月   9.400000  10.100000  2022-08-17
175  2022年08月  10.100000   9.900000  2022-09-14
176  2022年09月   9.900000  10.100000  2022-10-19
```
