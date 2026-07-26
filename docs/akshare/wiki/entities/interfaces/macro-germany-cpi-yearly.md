---
title: "macro_germany_cpi_yearly - 消费者物价指数年率终值"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > 消费者物价指数年率终值
- 描述: 东方财富-数据中心-经济数据一览-德国-消费者物价指数年率终值
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数年率终值

接口: macro_germany_cpi_yearly

目标地址: https://data.eastmoney.com/cjsj/foreign_1_2.html

描述: 东方财富-数据中心-经济数据一览-德国-消费者物价指数年率终值

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

macro_germany_cpi_yearly_df = ak.macro_germany_cpi_yearly()
print(macro_germany_cpi_yearly_df)
```

数据示例

```
     时间   前值    现值        发布日期
0    2008年01月  3.1   2.9  2008-02-16
1    2008年02月  2.9   3.0  2008-03-18
2    2008年03月  3.0   3.3  2008-04-16
3    2008年04月  3.3   2.6  2008-05-17
4    2008年05月  2.6   3.1  2008-06-16
..        ...  ...   ...         ...
172  2022年05月  7.8   8.7  2022-06-17
173  2022年06月  8.7   8.2  2022-07-19
174  2022年07月  8.2   8.5  2022-08-18
175  2022年08月  8.5   8.8  2022-09-16
176  2022年09月  8.8  10.9  2022-10-19
```
