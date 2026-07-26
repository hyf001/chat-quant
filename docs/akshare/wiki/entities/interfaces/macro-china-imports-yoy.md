---
title: "macro_china_imports_yoy - 以美元计算进口年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_imports_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 贸易状况 > 以美元计算进口年率
- 描述: 中国以美元计算进口年率报告, 数据区间从 19960201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_imports_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 以美元计算进口年率

接口: macro_china_imports_yoy

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_imports_yoy

描述: 中国以美元计算进口年率报告, 数据区间从 19960201-至今

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

macro_china_imports_yoy_df = ak.macro_china_imports_yoy()
print(macro_china_imports_yoy_df)
```

数据示例

```
                商品          日期    今值  预测值    前值
0    中国以美元计算进口年率报告  1996-02-01  55.8  NaN   NaN
1    中国以美元计算进口年率报告  1996-03-01  14.2  NaN  55.8
2    中国以美元计算进口年率报告  1996-04-01   8.7  NaN  14.2
3    中国以美元计算进口年率报告  1996-05-01   6.4  NaN   8.7
4    中国以美元计算进口年率报告  1996-06-01   4.5  NaN   6.4
..             ...         ...   ...  ...   ...
343  中国以美元计算进口年率报告  2023-12-07  -0.6  3.3   3.0
344  中国以美元计算进口年率报告  2024-01-12   0.2  0.3  -0.6
345  中国以美元计算进口年率报告  2024-01-13   NaN  NaN  -0.6
346  中国以美元计算进口年率报告  2024-03-07   3.5  1.5   0.2
347  中国以美元计算进口年率报告  2024-04-12   NaN  NaN   3.5
[348 rows x 5 columns]
```
