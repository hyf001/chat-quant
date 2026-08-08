---
title: "macro_uk_gdp_yearly - GDP 年率初值"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_gdp_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > GDP 年率初值
- 描述: 东方财富-经济数据-英国-GDP 年率初值
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_13.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### GDP 年率初值

接口: macro_uk_gdp_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_13.html

描述: 东方财富-经济数据-英国-GDP 年率初值

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

macro_uk_gdp_yearly_df = ak.macro_uk_gdp_yearly()
print(macro_uk_gdp_yearly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0   2009第4季度  NaN  1.1  2010-03-31
1   2010第4季度  1.1  3.0  2011-03-31
2   2011第4季度  3.0  1.5  2012-03-30
3   2012第4季度  1.5  0.4  2013-03-31
4   2013第4季度  0.4  2.4  2014-03-31
5   2014第4季度  2.4  3.5  2015-03-31
6   2015第4季度  3.5  1.7  2016-03-31
7   2016第4季度  1.7  2.0  2017-03-31
8   2017第4季度  2.0  1.3  2018-03-29
9   2018第4季度  1.3  1.4  2019-03-29
10  2019第4季度  1.4  1.1  2020-03-31
11  2020第4季度  1.1 -6.3  2021-03-31
12  2021第4季度 -6.3  6.6  2022-03-31
```
