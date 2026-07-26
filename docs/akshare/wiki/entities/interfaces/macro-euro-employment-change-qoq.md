---
title: "macro_euro_employment_change_qoq - 欧元区季调后就业人数季率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_employment_change_qoq

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 劳动力市场 > 欧元区季调后就业人数季率报告
- 描述: 欧元区季调后就业人数季率报告, 数据区间从 20083017-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_employment_change_qoq
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区季调后就业人数季率报告

接口: macro_euro_employment_change_qoq

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_employment_change_qoq

描述: 欧元区季调后就业人数季率报告, 数据区间从 20083017-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

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

macro_euro_employment_change_qoq_df = ak.macro_euro_employment_change_qoq()
print(macro_euro_employment_change_qoq_df)
```

数据示例

```
              商品          日期   今值  预测值   前值
0   欧元区季调后就业人数季率  2008-03-17  0.2  0.0  0.3
1   欧元区季调后就业人数季率  2008-06-13  0.3  0.0  0.2
2   欧元区季调后就业人数季率  2008-09-12  0.2  NaN  0.3
3   欧元区季调后就业人数季率  2008-12-16 -0.1  NaN  0.2
4   欧元区季调后就业人数季率  2009-03-16 -0.3  NaN -0.1
..           ...         ...  ...  ...  ...
70  欧元区季调后就业人数季率  2022-03-08  0.5  0.5  0.9
71  欧元区季调后就业人数季率  2022-05-17  0.5  NaN  0.4
72  欧元区季调后就业人数季率  2022-06-08  0.6  0.5  0.4
73  欧元区季调后就业人数季率  2022-08-17  0.3  NaN  0.6
74  欧元区季调后就业人数季率  2022-09-07  0.4  0.3  0.7
```
