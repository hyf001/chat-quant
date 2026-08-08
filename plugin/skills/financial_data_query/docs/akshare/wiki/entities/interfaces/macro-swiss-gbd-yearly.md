---
title: "macro_swiss_gbd_yearly - GDP 年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_swiss_gbd_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 瑞士宏观 > GDP 年率
- 描述: 东方财富-经济数据-瑞士-GDP 年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_2_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### GDP 年率

接口: macro_swiss_gbd_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_2_4.html

描述: 东方财富-经济数据-瑞士-GDP 年率

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

macro_swiss_gbd_yearly_df = ak.macro_swiss_gbd_yearly()
print(macro_swiss_gbd_yearly_df)
```

数据示例

```
    时间   前值   现值        发布日期
0   2007年12月  NaN  3.6  2008-03-02
1   2008年12月  3.6 -0.6  2009-03-03
2   2009年12月 -0.6  0.6  2010-03-03
3   2010年12月  0.6  3.1  2011-03-03
4   2011年12月  3.1  1.3  2012-03-02
5   2012年12月  1.3  1.4  2013-03-03
6   2013年12月  1.4  1.7  2014-03-03
7   2014年12月  1.7  1.9  2015-03-03
8   2015年12月  1.9  0.4  2016-03-02
9   2016年12月  0.4  0.6  2017-03-02
10  2017年12月  0.6  1.9  2018-03-01
11  2018年12月  1.9  1.4  2019-02-28
12  2019年12月  1.4  1.5  2020-03-03
13  2020年12月  1.5 -1.6  2021-03-03
14  2021年12月 -1.6  3.7  2022-02-28
```
