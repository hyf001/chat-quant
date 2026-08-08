---
title: "macro_australia_cpi_yearly - 消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 消费者物价指数年率
- 描述: 东方财富-经济数据-澳大利亚-消费者物价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_5.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数年率

接口: macro_australia_cpi_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_5_5.html

描述: 东方财富-经济数据-澳大利亚-消费者物价指数年率

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

macro_australia_cpi_yearly_df = ak.macro_australia_cpi_yearly()
print(macro_australia_cpi_yearly_df)
```

数据示例

```
    时间   前值   现值        发布日期
0   2008年03月  2.9  4.3  2008-04-26
1   2008年06月  4.3  4.4  2008-07-27
2   2008年09月  4.4  5.0  2008-10-27
3   2008年12月  5.0  3.7  2009-01-26
4   2009年03月  3.7  2.4  2009-04-26
..       ...  ...  ...         ...
63  2023年12月  5.4  4.1  2024-01-31
64  2024年03月  4.1  3.6  2024-04-24
65  2024年06月  3.6  3.8  2024-07-31
66  2024年09月  3.8  2.8  2024-10-30
67  2024年12月  2.8  NaN  2025-01-29
[68 rows x 4 columns]
```
