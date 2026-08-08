---
title: "macro_china_m2_yearly - M2货币供应年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_m2_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > M2货币供应年率
- 描述: 中国年度 M2 数据, 数据区间从 19980201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### M2货币供应年率

接口: macro_china_m2_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy

描述: 中国年度 M2 数据, 数据区间从 19980201-至今

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

macro_china_m2_yearly_df = ak.macro_china_m2_yearly()
print(macro_china_m2_yearly_df)
```

数据示例

```
               商品          日期    今值  预测值    前值
0    中国M2货币供应年率报告  1998-02-01  17.4  NaN   NaN
1    中国M2货币供应年率报告  1998-03-01  16.7  NaN  17.4
2    中国M2货币供应年率报告  1998-04-01  15.4  NaN  16.7
3    中国M2货币供应年率报告  1998-05-01  14.6  NaN  15.4
4    中国M2货币供应年率报告  1998-06-01  15.5  NaN  14.6
..            ...         ...   ...  ...   ...
349  中国M2货币供应年率报告  2024-03-12   NaN  8.8   8.7
350  中国M2货币供应年率报告  2024-03-13   NaN  8.8   8.7
351  中国M2货币供应年率报告  2024-03-14   NaN  8.8   8.7
352  中国M2货币供应年率报告  2024-03-15   8.7  8.8   8.7
353  中国M2货币供应年率报告  2024-04-11   NaN  NaN   8.7
[354 rows x 5 columns]
```
