---
title: "macro_japan_core_cpi_yearly - 全国核心消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_japan_core_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 日本宏观 > 全国核心消费者物价指数年率
- 描述: 东方财富-经济数据-日本-全国核心消费者物价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_2_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国核心消费者物价指数年率

接口: macro_japan_core_cpi_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_2_2.html

描述: 东方财富-经济数据-日本-全国核心消费者物价指数年率

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

macro_japan_core_cpi_yearly_df = ak.macro_japan_core_cpi_yearly()
print(macro_japan_core_cpi_yearly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2008年01月 -0.1 -0.1  2008-02-25
1    2008年02月 -0.1 -0.1  2008-03-27
2    2008年03月 -0.1  0.1  2008-04-25
3    2008年04月  0.1 -0.1  2008-05-26
4    2008年05月 -0.1 -0.1  2008-06-25
..        ...  ...  ...         ...
173  2022年06月  0.2  0.2  2022-07-22
174  2022年07月  0.2  0.4  2022-08-19
175  2022年08月  0.4  0.7  2022-09-20
176  2022年09月  0.7  0.9  2022-10-21
177  2022年10月  0.9  NaN  2022-11-18
```
