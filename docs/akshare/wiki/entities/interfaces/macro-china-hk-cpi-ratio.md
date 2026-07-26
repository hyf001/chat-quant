---
title: "macro_china_hk_cpi_ratio - 消费者物价指数年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_cpi_ratio

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国香港宏观 > 消费者物价指数年率
- 描述: 东方财富-经济数据一览-中国香港-消费者物价指数年率
- 目标地址: https://data.eastmoney.com/cjsj/foreign_8_1.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 消费者物价指数年率

接口: macro_china_hk_cpi_ratio

目标地址: https://data.eastmoney.com/cjsj/foreign_8_1.html

描述: 东方财富-经济数据一览-中国香港-消费者物价指数年率

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 前值   | float64 | 注意单位: % |
| 现值   | float64 | 注意单位: % |
| 发布日期 | object  | -       |

接口示例

```python
import akshare as ak

macro_china_hk_cpi_ratio_df = ak.macro_china_hk_cpi_ratio()
print(macro_china_hk_cpi_ratio_df)
```

数据示例

```
           时间   前值   现值        发布日期
0    2008年01月  3.8  3.2  2008-02-21
1    2008年02月  3.2  6.3  2008-03-23
2    2008年03月  6.3  4.2  2008-04-21
3    2008年04月  4.2  5.4  2008-05-22
4    2008年05月  5.4  5.7  2008-06-21
..        ...  ...  ...         ...
167  2021年12月  1.8  2.4  2022-01-20
168  2022年01月  2.4  1.2  2022-02-22
169  2022年02月  1.2  1.6  2022-03-21
170  2022年03月  1.6  1.7  2022-04-22
171  2022年04月  1.7  1.3  2022-05-23
[172 rows x 4 columns]
```
