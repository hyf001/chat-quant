---
title: "macro_japan_unemployment_rate - 失业率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_japan_unemployment_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 日本宏观 > 失业率
- 描述: 东方财富-经济数据-日本-失业率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_2_3.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 失业率

接口: macro_japan_unemployment_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_2_3.html

描述: 东方财富-经济数据-日本-失业率

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

macro_japan_unemployment_rate_df = ak.macro_japan_unemployment_rate()
print(macro_japan_unemployment_rate_df)
```

数据示例

```
      时间   前值   现值        发布日期
0    2008年01月  3.7  3.9  2008-02-29
1    2008年02月  3.9  4.0  2008-03-31
2    2008年03月  4.0  3.8  2008-04-29
3    2008年04月  3.8  3.9  2008-05-30
4    2008年05月  3.9  4.0  2008-06-29
..        ...  ...  ...         ...
173  2022年06月  2.6  2.6  2022-07-29
174  2022年07月  2.6  2.6  2022-08-30
175  2022年08月  2.6  2.5  2022-09-30
176  2022年09月  2.5  2.7  2022-10-28
177  2022年10月  2.7  NaN  2022-11-29
```
