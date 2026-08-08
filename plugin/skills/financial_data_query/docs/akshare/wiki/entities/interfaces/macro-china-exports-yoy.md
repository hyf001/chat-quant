---
title: "macro_china_exports_yoy - 以美元计算出口年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_exports_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 贸易状况 > 以美元计算出口年率
- 描述: 中国以美元计算出口年率报告, 数据区间从 19820201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_exports_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 以美元计算出口年率

接口: macro_china_exports_yoy

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_exports_yoy

描述: 中国以美元计算出口年率报告, 数据区间从 19820201-至今

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

macro_china_exports_yoy_df = ak.macro_china_exports_yoy()
print(macro_china_exports_yoy_df)
```

数据示例

```
                商品          日期    今值  预测值    前值
0    中国以美元计算出口年率报告  1982-02-01   8.7  NaN   NaN
1    中国以美元计算出口年率报告  1982-03-01  23.2  NaN   8.7
2    中国以美元计算出口年率报告  1982-04-01  12.2  NaN  23.2
3    中国以美元计算出口年率报告  1982-05-01  -2.5  NaN  12.2
4    中国以美元计算出口年率报告  1982-06-01  41.5  NaN  -2.5
..             ...         ...   ...  ...   ...
505  中国以美元计算出口年率报告  2023-12-07   0.5 -1.1  -6.4
506  中国以美元计算出口年率报告  2024-01-12   2.3  1.7   0.5
507  中国以美元计算出口年率报告  2024-01-13   NaN  NaN   0.5
508  中国以美元计算出口年率报告  2024-03-07   7.1  1.9   2.3
509  中国以美元计算出口年率报告  2024-04-12   NaN  NaN   7.1
[510 rows x 5 columns]
```
