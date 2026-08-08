---
title: "macro_usa_cb_consumer_confidence - 美国谘商会消费者信心指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cb_consumer_confidence

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 领先指标 > 美国谘商会消费者信心指数报告
- 描述: 美国谘商会消费者信心指数报告, 数据区间从 19700101-至今
- 目标地址: https://cdn.jin10.com/dc/reports/dc_usa_cb_consumer_confidence_all.js?v=1578576859
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国谘商会消费者信心指数报告

接口: macro_usa_cb_consumer_confidence

目标地址: https://cdn.jin10.com/dc/reports/dc_usa_cb_consumer_confidence_all.js?v=1578576859

描述: 美国谘商会消费者信心指数报告, 数据区间从 19700101-至今

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

macro_usa_cb_consumer_confidence_df = ak.macro_usa_cb_consumer_confidence()
print(macro_usa_cb_consumer_confidence_df)
```

数据示例

```
               商品          日期     今值    预测值     前值
0    美国谘商会消费者信心指数  1970-01-01  126.0    NaN    NaN
1    美国谘商会消费者信心指数  1970-02-01  126.0    NaN  126.0
2    美国谘商会消费者信心指数  1970-03-01  101.7    NaN  126.0
3    美国谘商会消费者信心指数  1970-04-01  101.7    NaN  101.7
4    美国谘商会消费者信心指数  1970-05-01   98.0    NaN  101.7
..            ...         ...    ...    ...    ...
650  美国谘商会消费者信心指数  2023-11-28  102.0  101.0   99.1
651  美国谘商会消费者信心指数  2023-12-20  110.7  103.8  101.0
652  美国谘商会消费者信心指数  2024-01-30  114.8  114.2  108.0
653  美国谘商会消费者信心指数  2024-02-27  106.7  114.8  110.9
654  美国谘商会消费者信心指数  2024-03-26  104.7  106.9  104.8
[655 rows x 5 columns]
```
