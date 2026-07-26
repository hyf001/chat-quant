---
title: "macro_australia_unemployment_rate - 失业率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_unemployment_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 失业率
- 描述: 东方财富-经济数据-澳大利亚-失业率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 失业率

接口: macro_australia_unemployment_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_5_2.html

描述: 东方财富-经济数据-澳大利亚-失业率

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

macro_australia_unemployment_rate_df = ak.macro_australia_unemployment_rate()
print(macro_australia_unemployment_rate_df)
```

数据示例

```
      时间        前值        现值        发布日期
0    2008年01月  4.309566  4.221168  2008-02-15
1    2008年02月  4.221168  3.981161  2008-03-17
2    2008年03月  3.981161  4.058254  2008-04-15
3    2008年04月  4.058254  4.266881  2008-05-16
4    2008年05月  4.266881  4.266643  2008-06-15
..        ...       ...       ...         ...
200  2024年09月  4.131262  4.067827  2024-10-17
201  2024年10月  4.067827  4.105942  2024-11-14
202  2024年11月  4.105942  3.926610  2024-12-12
203  2024年12月  3.926610  3.977499  2025-01-16
204  2025年01月  3.977499       NaN  2025-02-20
[205 rows x 4 columns]
```
