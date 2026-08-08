---
title: "macro_germany_retail_sale_yearly - 实际零售销售年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_retail_sale_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > 实际零售销售年率
- 描述: 东方财富-数据中心-经济数据一览-德国-实际零售销售年率
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_6.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实际零售销售年率

接口: macro_germany_retail_sale_yearly

目标地址: https://data.eastmoney.com/cjsj/foreign_1_6.html

描述: 东方财富-数据中心-经济数据一览-德国-实际零售销售年率

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

macro_germany_retail_sale_yearly_df = ak.macro_germany_retail_sale_yearly()
print(macro_germany_retail_sale_yearly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0   2008年12月  3.2  3.9  2009-04-13
1   2009年12月  3.9 -0.1  2010-04-13
2   2010年12月 -0.1  0.4  2011-04-13
3   2011年12月  0.4  2.0  2012-04-12
4   2012年12月  2.0  2.5  2013-04-13
5   2013年12月  2.5  2.5  2014-11-18
6   2014年12月  2.5  1.0  2015-01-16
7   2015年12月  1.0  0.1  2016-01-16
8   2016年12月  0.1  0.6  2017-01-16
9   2017年12月  0.6  2.0  2018-01-16
10  2018年12月  2.0  1.9  2019-01-16
11  2019年12月  1.9  0.7  2020-01-16
12  2020年12月  0.7 -0.1  2021-01-19
13  2021年12月 -0.1  5.3  2022-01-19
14  2022年12月  5.3  NaN  2023-01-17
```
