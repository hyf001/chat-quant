---
title: "macro_euro_trade_balance - 欧元区未季调贸易帐报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_trade_balance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 贸易状况 > 欧元区未季调贸易帐报告
- 描述: 欧元区未季调贸易帐报告, 数据区间从 19990201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_trade_balance_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区未季调贸易帐报告

接口: macro_euro_trade_balance

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_trade_balance_mom

描述: 欧元区未季调贸易帐报告, 数据区间从 19990201-至今

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

macro_euro_trade_balance_df = ak.macro_euro_trade_balance()
print(macro_euro_trade_balance_df)
```

数据示例

```
            商品          日期     今值    预测值     前值
0    欧元区未季调贸易帐  1999-02-01  -27.0    NaN    NaN
1    欧元区未季调贸易帐  1999-03-01   19.0    NaN  -27.0
2    欧元区未季调贸易帐  1999-04-01   27.0    NaN   19.0
3    欧元区未季调贸易帐  1999-05-01   21.0    NaN   27.0
4    欧元区未季调贸易帐  1999-06-01   -9.0    NaN   21.0
..         ...         ...    ...    ...    ...
281  欧元区未季调贸易帐  2022-07-15 -263.0    NaN -328.0
282  欧元区未季调贸易帐  2022-08-16 -246.0 -200.0 -284.0
283  欧元区未季调贸易帐  2022-09-15 -340.0 -200.0 -254.0
284  欧元区未季调贸易帐  2022-10-14 -509.0    NaN -339.0
285  欧元区未季调贸易帐  2022-11-15    NaN    NaN -509.0
```
