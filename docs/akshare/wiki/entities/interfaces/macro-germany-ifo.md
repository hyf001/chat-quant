---
title: "macro_germany_ifo - IFO商业景气指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_ifo

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > IFO商业景气指数
- 描述: 东方财富-数据中心-经济数据一览-IFO商业景气指数
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### IFO商业景气指数

接口: macro_germany_ifo

目标地址: https://data.eastmoney.com/cjsj/foreign_1_0.html

描述: 东方财富-数据中心-经济数据一览-IFO商业景气指数

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

macro_germany_ifo_df = ak.macro_germany_ifo()
print(macro_germany_ifo_df)
```

数据示例

```
       时间      前值    现值    发布日期
0    2008年01月  98.3  97.9  2008-01-25
1    2008年02月  97.9  97.8  2008-02-25
2    2008年03月  97.8  97.9  2008-03-25
3    2008年04月  97.9  97.1  2008-04-25
4    2008年05月  97.1  96.6  2008-05-25
..        ...   ...   ...         ...
173  2022年06月  93.3  92.3  2022-06-24
174  2022年07月  92.3  88.6  2022-07-25
175  2022年08月  88.6  88.6  2022-08-25
176  2022年09月  88.6  84.4  2022-09-26
177  2022年10月  84.4  84.3  2022-10-25
```
