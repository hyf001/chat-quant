---
title: "macro_usa_spcs20 - 美国S&P/CS20座大城市房价指数年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_spcs20

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国S&P/CS20座大城市房价指数年率报告
- 描述: 美国S&P/CS20座大城市房价指数年率报告, 数据区间从 20010201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_spcs20
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国S&P/CS20座大城市房价指数年率报告

接口: macro_usa_spcs20

目标地址: https://datacenter.jin10.com/reportType/dc_usa_spcs20

描述: 美国S&P/CS20座大城市房价指数年率报告, 数据区间从 20010201-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_usa_spcs20_df = ak.macro_usa_spcs20()
print(macro_usa_spcs20_df)
```

数据示例

```
                       商品          日期    今值  预测值    前值
0    美国S&P/CS20座大城市房价指数年率  2001-02-01  12.4  NaN   NaN
1    美国S&P/CS20座大城市房价指数年率  2001-03-01  12.2  NaN  12.4
2    美国S&P/CS20座大城市房价指数年率  2001-04-01  12.0  NaN  12.2
3    美国S&P/CS20座大城市房价指数年率  2001-05-01  11.4  NaN  12.0
4    美国S&P/CS20座大城市房价指数年率  2001-06-01  10.5  NaN  11.4
..                    ...         ...   ...  ...   ...
275  美国S&P/CS20座大城市房价指数年率  2023-11-28   3.9  4.0   2.1
276  美国S&P/CS20座大城市房价指数年率  2023-12-26   4.9  5.0   3.9
277  美国S&P/CS20座大城市房价指数年率  2024-01-30   5.4  5.8   4.9
278  美国S&P/CS20座大城市房价指数年率  2024-02-27   6.1  6.0   5.4
279  美国S&P/CS20座大城市房价指数年率  2024-03-26   6.6  6.6   6.2
[280 rows x 5 columns]
```
