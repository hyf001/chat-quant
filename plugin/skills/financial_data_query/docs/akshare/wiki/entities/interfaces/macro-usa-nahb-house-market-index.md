---
title: "macro_usa_nahb_house_market_index - 美国NAHB房产市场指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_nahb_house_market_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国NAHB房产市场指数报告
- 描述: 美国 NAHB 房产市场指数报告, 数据区间从 19850201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_nahb_house_market_index
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国NAHB房产市场指数报告

接口: macro_usa_nahb_house_market_index

目标地址: https://datacenter.jin10.com/reportType/dc_usa_nahb_house_market_index

描述: 美国 NAHB 房产市场指数报告, 数据区间从 19850201-至今

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

macro_usa_nahb_house_market_index_df = ak.macro_usa_nahb_house_market_index()
print(macro_usa_nahb_house_market_index_df)
```

数据示例

```
                 商品          日期    今值   预测值    前值
0    美国NAHB房产市场指数报告  1985-02-01  50.0   NaN   NaN
1    美国NAHB房产市场指数报告  1985-03-01  58.0   NaN  50.0
2    美国NAHB房产市场指数报告  1985-04-01  54.0   NaN  58.0
3    美国NAHB房产市场指数报告  1985-05-01  49.0   NaN  54.0
4    美国NAHB房产市场指数报告  1985-06-01  51.0   NaN  49.0
..              ...         ...   ...   ...   ...
467  美国NAHB房产市场指数报告  2023-12-18  37.0  36.0  34.0
468  美国NAHB房产市场指数报告  2024-01-17  44.0  39.0  37.0
469  美国NAHB房产市场指数报告  2024-02-15  48.0  46.0  44.0
470  美国NAHB房产市场指数报告  2024-03-18  51.0  48.0  48.0
471  美国NAHB房产市场指数报告  2024-04-15   NaN   NaN  51.0
[472 rows x 5 columns]
```
