---
title: "macro_australia_cpi_quarterly - 消费者物价指数季率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_cpi_quarterly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 消费者物价指数季率
- 描述: 东方财富-经济数据-澳大利亚-消费者物价指数季率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数季率

接口: macro_australia_cpi_quarterly

目标地址: http://data.eastmoney.com/cjsj/foreign_5_4.html

描述: 东方财富-经济数据-澳大利亚-消费者物价指数季率

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

macro_australia_cpi_quarterly_df = ak.macro_australia_cpi_quarterly()
print(macro_australia_cpi_quarterly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0   2008第1季度  0.9  1.3  2008-06-07
1   2008第2季度  1.3  1.4  2008-09-07
2   2008第3季度  1.4  1.2  2008-12-08
3   2008第4季度  1.2 -0.3  2009-03-09
4   2009第1季度 -0.3  0.1  2009-06-07
..       ...  ...  ...         ...
63  2023第4季度  1.2  0.6  2024-01-31
64  2024第1季度  0.6  1.0  2024-04-24
65  2024第2季度  1.0  1.0  2024-07-31
66  2024第3季度  1.0  0.2  2024-10-30
67  2024第4季度  0.2  NaN  2025-01-29
[68 rows x 4 columns]
```
