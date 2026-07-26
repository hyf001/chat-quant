---
title: "macro_china_trade_balance - 以美元计算贸易帐(亿美元)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_trade_balance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 贸易状况 > 以美元计算贸易帐(亿美元)
- 描述: 中国以美元计算贸易帐报告, 数据区间从19810201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_trade_balance
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 以美元计算贸易帐(亿美元)

接口: macro_china_trade_balance

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_trade_balance

描述: 中国以美元计算贸易帐报告, 数据区间从19810201-至今

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

macro_china_trade_balance_df = ak.macro_china_trade_balance()
print(macro_china_trade_balance_df)
```

数据示例

```
               商品          日期      今值     预测值      前值
0    中国以美元计算贸易帐报告  1981-02-01    -2.2     NaN     NaN
1    中国以美元计算贸易帐报告  1981-03-01    -4.9     NaN    -2.2
2    中国以美元计算贸易帐报告  1981-04-01    -7.4     NaN    -4.9
3    中国以美元计算贸易帐报告  1981-05-01    -4.8     NaN    -7.4
4    中国以美元计算贸易帐报告  1981-06-01    -5.4     NaN    -4.8
..            ...         ...     ...     ...     ...
528  中国以美元计算贸易帐报告  2023-12-07   683.9   580.0   565.3
529  中国以美元计算贸易帐报告  2024-01-12   753.4   747.5   683.9
530  中国以美元计算贸易帐报告  2024-01-13     NaN     NaN   683.9
531  中国以美元计算贸易帐报告  2024-03-07  1251.6  1103.0   753.4
532  中国以美元计算贸易帐报告  2024-04-12     NaN     NaN  1251.6
[533 rows x 5 columns]
```
