---
title: "macro_usa_building_permits - 美国营建许可总数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_building_permits

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国营建许可总数报告
- 描述: 美国营建许可总数报告, 数据区间从 20080220-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_building_permits
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国营建许可总数报告

接口: macro_usa_building_permits

目标地址: https://datacenter.jin10.com/reportType/dc_usa_building_permits

描述: 美国营建许可总数报告, 数据区间从 20080220-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 商品  | object  | -        |
| 日期  | object  | -        |
| 今值  | float64 | 注意单位: 万户 |
| 预测值 | float64 | 注意单位: 万户 |
| 前值  | float64 | 注意单位: 万户 |

接口示例

```python
import akshare as ak

macro_usa_building_permits_df = ak.macro_usa_building_permits()
print(macro_usa_building_permits_df)
```

数据示例

```
             商品          日期     今值    预测值     前值
0    美国营建许可总数报告  2008-02-20  105.0  105.0  107.0
1    美国营建许可总数报告  2008-03-18   98.0  105.0  106.0
2    美国营建许可总数报告  2008-04-16   93.0   97.0   98.0
3    美国营建许可总数报告  2008-05-16   98.0   92.0   93.0
4    美国营建许可总数报告  2008-06-17   97.0   96.0   98.0
..          ...         ...    ...    ...    ...
206  美国营建许可总数报告  2024-02-16  147.0  150.9  149.3
207  美国营建许可总数报告  2024-02-26  148.9  147.0  149.3
208  美国营建许可总数报告  2024-03-19  151.8  150.0  148.9
209  美国营建许可总数报告  2024-03-25  152.4  151.8  148.9
210  美国营建许可总数报告  2024-04-16    NaN    NaN  152.4
[211 rows x 5 columns]
```
