---
title: "macro_swiss_cpi_yearly - 消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_swiss_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 瑞士宏观 > 消费者物价指数年率
- 描述: 东方财富-经济数据-瑞士-消费者物价指数年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_2_2.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数年率

接口: macro_swiss_cpi_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_2_2.html

描述: 东方财富-经济数据-瑞士-消费者物价指数年率

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

macro_swiss_cpi_yearly_df = ak.macro_swiss_cpi_yearly()
print(macro_swiss_cpi_yearly_df)
```

数据示例

```
    时间   前值   现值        发布日期
0   2007第4季度  NaN  2.0  2008-01-08
1   2008第4季度  2.0  0.7  2009-01-08
2   2009第4季度  0.7  0.3  2010-01-08
3   2010第4季度  0.3  0.5  2011-01-08
4   2011第4季度  0.5 -0.7  2012-01-08
5   2012第4季度 -0.7 -0.4  2013-01-08
6   2013第4季度 -0.4  0.1  2014-01-08
7   2015第4季度 -0.3 -1.3  2016-01-08
8   2016第4季度 -1.3  0.0  2017-01-05
9   2017第4季度  0.0  0.8  2018-01-08
10  2018第4季度  0.8  0.7  2019-01-09
11  2014第4季度  0.1 -0.3  2019-01-09
12  2019第4季度  0.7  0.2  2020-01-07
13  2020第4季度  0.2 -0.8  2021-01-05
14  2021第4季度 -0.8  1.5  2022-01-04
```
