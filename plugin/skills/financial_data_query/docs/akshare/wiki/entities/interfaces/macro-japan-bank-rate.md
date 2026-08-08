---
title: "macro_japan_bank_rate - 央行公布利率决议"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_japan_bank_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 日本宏观 > 央行公布利率决议
- 描述: 东方财富-经济数据-日本-央行公布利率决议
- 目标地址: http://data.eastmoney.com/cjsj/foreign_3_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 央行公布利率决议

接口: macro_japan_bank_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_3_0.html

描述: 东方财富-经济数据-日本-央行公布利率决议

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

macro_japan_bank_rate_df = ak.macro_japan_bank_rate()
print(macro_japan_bank_rate_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2008年01月  NaN  0.5  2008-01-21
1    2008年02月  0.5  0.5  2008-02-21
2    2008年03月  0.5  0.5  2008-03-21
3    2008年04月  0.5  0.5  2008-04-21
4    2008年05月  0.5  0.5  2008-05-21
..        ...  ...  ...         ...
148  2022年05月 -0.1 -0.1  2022-06-17
149  2022年06月 -0.1 -0.1  2022-06-17
150  2022年07月 -0.1  NaN  2022-07-21
151  2022年09月  NaN -0.1  2022-09-22
152  2022年10月 -0.1 -0.1  2022-10-28
```
