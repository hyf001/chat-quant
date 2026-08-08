---
title: "macro_usa_trade_balance - 美国贸易帐报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_trade_balance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 贸易状况 > 美国贸易帐报告
- 描述: 美国贸易帐报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_trade_balance
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国贸易帐报告

接口: macro_usa_trade_balance

目标地址: https://datacenter.jin10.com/reportType/dc_usa_trade_balance

描述: 美国贸易帐报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

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

macro_usa_trade_balance_df = ak.macro_usa_trade_balance()
print(macro_usa_trade_balance_df)
```

数据示例

```
          商品          日期     今值    预测值     前值
0    美国贸易帐报告  1970-01-01    2.0    NaN    NaN
1    美国贸易帐报告  1970-02-01    1.0    NaN    2.0
2    美国贸易帐报告  1970-03-01    2.0    NaN    1.0
3    美国贸易帐报告  1970-04-01    1.0    NaN    2.0
4    美国贸易帐报告  1970-05-01    1.0    NaN    1.0
..       ...         ...    ...    ...    ...
648  美国贸易帐报告  2023-12-06 -643.0 -642.0 -612.0
649  美国贸易帐报告  2024-01-09 -632.0 -650.0 -645.0
650  美国贸易帐报告  2024-02-07 -622.0 -620.0 -619.0
651  美国贸易帐报告  2024-03-07 -674.0 -634.0 -642.0
652  美国贸易帐报告  2024-04-04 -689.0 -669.0 -676.0
[653 rows x 5 columns]
```
