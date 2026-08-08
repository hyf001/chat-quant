---
title: "macro_australia_bank_rate - 央行公布利率决议"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_bank_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 央行公布利率决议
- 描述: 东方财富-经济数据-澳大利亚-央行公布利率决议
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_6.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 央行公布利率决议

接口: macro_australia_bank_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_5_6.html

描述: 东方财富-经济数据-澳大利亚-央行公布利率决议

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

macro_australia_bank_rate_df = ak.macro_australia_bank_rate()
print(macro_australia_bank_rate_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2008年01月   NaN  7.00  2008-01-05
1    2008年02月  7.00  7.00  2008-02-05
2    2008年03月  7.00  7.25  2008-03-05
3    2008年04月  7.25  7.25  2008-04-05
4    2008年05月  7.25  7.25  2008-05-05
..        ...   ...   ...         ...
186  2024年08月  4.35  4.35  2024-08-06
187  2024年09月  4.35  4.35  2024-09-24
188  2024年11月  4.35  4.35  2024-11-05
189  2024年12月  4.35  4.35  2024-12-10
190  2025年02月  4.35   NaN  2025-02-04
[191 rows x 4 columns]
```
