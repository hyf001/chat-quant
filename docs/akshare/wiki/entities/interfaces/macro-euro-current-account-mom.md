---
title: "macro_euro_current_account_mom - 欧元区经常帐报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_current_account_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 贸易状况 > 欧元区经常帐报告
- 描述: 欧元区经常帐报告, 数据区间从 20080221-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_current_account_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区经常帐报告

接口: macro_euro_current_account_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_current_account_mom

描述: 欧元区经常帐报告, 数据区间从 20080221-至今

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

macro_euro_current_account_mom_df = ak.macro_euro_current_account_mom()
print(macro_euro_current_account_mom_df)
```

数据示例

```
         商品          日期     今值    预测值     前值
0    欧元区经常帐  1999-02-01 -150.0    NaN    NaN
1    欧元区经常帐  2003-07-01   10.0    NaN    0.0
2    欧元区经常帐  2008-02-21 -103.0    2.0    7.0
3    欧元区经常帐  2008-03-26 -106.0    0.0 -103.0
4    欧元区经常帐  2008-04-24   43.0    0.0 -106.0
..      ...         ...    ...    ...    ...
175  欧元区经常帐  2022-07-20  -45.0    NaN  -58.0
176  欧元区经常帐  2022-08-19   42.0    NaN  -45.0
177  欧元区经常帐  2022-09-20 -199.0   53.0   42.0
178  欧元区经常帐  2022-10-20 -263.0 -203.0 -199.0
179  欧元区经常帐  2022-11-22    NaN    NaN -263.0
```
