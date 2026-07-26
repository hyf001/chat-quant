---
title: "macro_uk_trade - 贸易帐"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_trade

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 贸易帐
- 描述: 东方财富-经济数据-英国-贸易帐
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 贸易帐

接口: macro_uk_trade

目标地址: http://data.eastmoney.com/cjsj/foreign_4_2.html

描述: 东方财富-经济数据-英国-贸易帐

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

macro_uk_trade_df = ak.macro_uk_trade()
print(macro_uk_trade_df)
```

数据示例

```
           时间     前值     现值        发布日期
0    2008年01月  -3157  -3750  2008-03-11
1    2008年02月  -3750  -3749  2008-04-11
2    2008年03月  -3749  -3194  2008-05-10
3    2008年04月  -3194  -3182  2008-06-10
4    2008年05月  -3182  -2696  2008-07-10
..        ...    ...    ...         ...
171  2022年04月 -11881  -9266  2022-06-13
172  2022年05月  -9266  -9119  2022-07-13
173  2022年06月  -9119 -11387  2022-08-12
174  2022年07月 -11387  -7793  2022-09-12
175  2022年08月  -7793  -7080  2022-10-12
```
