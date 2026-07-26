---
title: "macro_germany_zew - ZEW 经济景气指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_zew

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > ZEW 经济景气指数
- 描述: 东方财富-数据中心-经济数据一览-德国-ZEW 经济景气指数
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_7.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### ZEW 经济景气指数

接口: macro_germany_zew

目标地址: https://data.eastmoney.com/cjsj/foreign_1_7.html

描述: 东方财富-数据中心-经济数据一览-德国-ZEW 经济景气指数

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

macro_germany_zew_df = ak.macro_germany_zew()
print(macro_germany_zew_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2008年01月 -37.2 -41.6  2008-01-16
1    2008年02月 -41.6 -39.5  2008-02-16
2    2008年03月 -39.5 -32.0  2008-03-16
3    2008年04月 -32.0 -40.7  2008-04-16
4    2008年05月 -40.7 -41.4  2008-05-16
..        ...   ...   ...         ...
174  2022年07月 -28.0 -53.8  2022-07-12
175  2022年08月 -53.8 -55.3  2022-08-16
176  2022年09月 -55.3 -61.9  2022-09-13
177  2022年10月 -61.9 -59.2  2022-10-18
178  2022年11月 -59.2   NaN  2022-11-15
```
