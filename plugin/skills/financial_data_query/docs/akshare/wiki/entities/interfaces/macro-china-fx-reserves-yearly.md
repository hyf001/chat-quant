---
title: "macro_china_fx_reserves_yearly - 外汇储备(亿美元)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_fx_reserves_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 外汇储备(亿美元)
- 描述: 中国年度外汇储备数据, 数据区间从 20140115-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_fx_reserves
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 外汇储备(亿美元)

接口: macro_china_fx_reserves_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_fx_reserves

描述: 中国年度外汇储备数据, 数据区间从 20140115-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述        |
|-----|---------|-----------|
| 商品  | object  | -         |
| 日期  | object  | -         |
| 今值  | float64 | 注意单位: 亿美元 |
| 预测值 | float64 | 注意单位: 亿美元 |
| 前值  | float64 | 注意单位: 亿美元 |

接口示例

```python
import akshare as ak

macro_china_fx_reserves_yearly_df = ak.macro_china_fx_reserves_yearly()
print(macro_china_fx_reserves_yearly_df)
```

数据示例

```
           商品          日期       今值      预测值     前值
0    中国外汇储备报告  2014-01-15  38200.0  38000.0  36600
1    中国外汇储备报告  2014-07-15  39900.0  39800.0  39500
2    中国外汇储备报告  2015-01-15  38400.0  39000.0  39900
3    中国外汇储备报告  2016-03-07  32000.0  31900.0  32300
4    中国外汇储备报告  2016-04-07  32100.0  32100.0  32000
..        ...         ...      ...      ...    ...
106  中国外汇储备报告  2023-12-07  31720.0  31200.0  31010
107  中国外汇储备报告  2024-01-07  32380.0  32000.0  31720
108  中国外汇储备报告  2024-02-07  32190.0  32170.0  32380
109  中国外汇储备报告  2024-03-07  32260.0  32050.0  32190
110  中国外汇储备报告  2024-04-07      NaN      NaN  32260
[111 rows x 5 columns]
```
