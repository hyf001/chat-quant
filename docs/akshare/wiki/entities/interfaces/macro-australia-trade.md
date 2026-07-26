---
title: "macro_australia_trade - 贸易帐"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_trade

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 贸易帐
- 描述: 东方财富-经济数据-澳大利亚-贸易帐
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_1.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 贸易帐

接口: macro_australia_trade

目标地址: http://data.eastmoney.com/cjsj/foreign_5_1.html

描述: 东方财富-经济数据-澳大利亚-贸易帐

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 时间   | object  | -         |
| 前值   | float64 | 注意单位: 亿澳元 |
| 现值   | float64 | 注意单位: 亿澳元 |
| 发布日期 | object  | -         |

接口示例

```python
import akshare as ak

macro_australia_trade_df = ak.macro_australia_trade()
print(macro_australia_trade_df)
```

数据示例

```
     时间     前值     现值        发布日期
0    2008年01月  -1148  -3854  2008-03-06
1    2008年02月  -3854  -2677  2008-04-06
2    2008年03月  -2677  -1434  2008-05-05
3    2008年04月  -1434  -1939  2008-06-05
4    2008年05月  -1939  -1285  2008-07-05
..        ...    ...    ...         ...
183  2023年04月  16759  11789  2023-06-08
184  2023年05月  11789   9382  2023-07-06
185  2023年06月   9382  10846  2023-08-03
186  2023年07月  10846   6209  2023-09-07
187  2023年08月   6209   7892  2023-10-05
[188 rows x 4 columns]
```
