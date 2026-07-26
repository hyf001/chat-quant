---
title: "macro_germany_retail_sale_monthly - 实际零售销售月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_retail_sale_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > 实际零售销售月率
- 描述: 东方财富-数据中心-经济数据一览-德国-实际零售销售月率
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_5.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实际零售销售月率

接口: macro_germany_retail_sale_monthly

目标地址: https://data.eastmoney.com/cjsj/foreign_1_5.html

描述: 东方财富-数据中心-经济数据一览-德国-实际零售销售月率

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

macro_germany_retail_sale_monthly_df = ak.macro_germany_retail_sale_monthly()
print(macro_germany_retail_sale_monthly_df)
```

数据示例

```
      时间    前值    现值        发布日期
0    2008年01月   4.5   4.4  2008-02-13
1    2008年02月   4.4   4.5  2008-03-15
2    2008年03月   4.5   5.1  2008-04-13
3    2008年04月   5.1   4.4  2008-05-14
4    2008年05月   4.4   4.8  2008-06-13
..        ...   ...   ...         ...
173  2022年06月   9.1  10.2  2022-07-13
174  2022年07月  10.2  11.5  2022-08-10
175  2022年08月  11.5  12.7  2022-09-13
176  2022年09月  12.7  14.1  2022-10-13
177  2022年10月  14.1   NaN  2022-11-11
```
