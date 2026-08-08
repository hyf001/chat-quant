---
title: "macro_usa_nfib_small_business - 美国NFIB小型企业信心指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_nfib_small_business

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 领先指标 > 美国NFIB小型企业信心指数报告
- 描述: 美国NFIB小型企业信心指数报告, 数据区间从 19750201-至今
- 目标地址: https://cdn.jin10.com/dc/reports/dc_usa_nfib_small_business_all.js?v=1578576631
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国NFIB小型企业信心指数报告

接口: macro_usa_nfib_small_business

目标地址: https://cdn.jin10.com/dc/reports/dc_usa_nfib_small_business_all.js?v=1578576631

描述: 美国NFIB小型企业信心指数报告, 数据区间从 19750201-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 商品  | object  | -  |
| 日期  | object  | -  |
| 今值  | float64 | -  |
| 预测值 | float64 | -  |
| 前值  | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_nfib_small_business_df = ak.macro_usa_nfib_small_business()
print(macro_usa_nfib_small_business_df)
```

数据示例

```
                   商品          日期      今值   预测值      前值
0    美国NFIB小型企业信心指数报告  1975-02-01   86.67   NaN     NaN
1    美国NFIB小型企业信心指数报告  1975-05-01   95.16   NaN   86.67
2    美国NFIB小型企业信心指数报告  1975-08-01   99.36   NaN   95.16
3    美国NFIB小型企业信心指数报告  1975-11-01  100.37   NaN   99.36
4    美国NFIB小型企业信心指数报告  1976-02-01  102.01   NaN  100.37
..                ...         ...     ...   ...     ...
501  美国NFIB小型企业信心指数报告  2023-12-12   90.60  90.7   90.70
502  美国NFIB小型企业信心指数报告  2024-01-09   91.90  90.7   90.60
503  美国NFIB小型企业信心指数报告  2024-02-13   89.90  92.3   91.90
504  美国NFIB小型企业信心指数报告  2024-03-12   89.40  90.5   89.90
505  美国NFIB小型企业信心指数报告  2024-04-09     NaN   NaN   89.40
[506 rows x 5 columns]
```
