---
title: "macro_china_industrial_production_yoy - 规模以上工业增加值年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_industrial_production_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 规模以上工业增加值年率
- 描述: 中国规模以上工业增加值年率报告, 数据区间从 19900301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_industrial_production_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 规模以上工业增加值年率

接口: macro_china_industrial_production_yoy

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_industrial_production_yoy

描述: 中国规模以上工业增加值年率报告, 数据区间从 19900301-至今

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

macro_china_industrial_production_yoy_df = ak.macro_china_industrial_production_yoy()
print(macro_china_industrial_production_yoy_df)
```

数据示例

```
                  商品          日期   今值  预测值   前值
0    中国规模以上工业增加值年率报告  1990-03-01  5.0  NaN  NaN
1    中国规模以上工业增加值年率报告  1990-04-01  0.8  NaN  5.0
2    中国规模以上工业增加值年率报告  1990-05-01  1.7  NaN  0.8
3    中国规模以上工业增加值年率报告  1990-06-01  3.3  NaN  1.7
4    中国规模以上工业增加值年率报告  1990-07-01  5.0  NaN  3.3
..               ...         ...  ...  ...  ...
392  中国规模以上工业增加值年率报告  2023-11-15  4.6  4.4  4.5
393  中国规模以上工业增加值年率报告  2023-12-15  6.6  5.6  4.6
394  中国规模以上工业增加值年率报告  2024-01-17  6.8  6.6  6.6
395  中国规模以上工业增加值年率报告  2024-03-18  7.0  5.3  6.8
396  中国规模以上工业增加值年率报告  2024-04-16  NaN  NaN  7.0
[397 rows x 5 columns]
```
