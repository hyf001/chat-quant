---
title: "macro_china_cx_services_pmi_yearly - 财新服务业PMI"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_cx_services_pmi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 财新服务业PMI
- 描述: 中国财新服务业 PMI 报告, 数据区间从 20120405-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_caixin_services_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 财新服务业PMI

接口: macro_china_cx_services_pmi_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_caixin_services_pmi

描述: 中国财新服务业 PMI 报告, 数据区间从 20120405-至今

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

macro_china_cx_services_pmi_yearly_df = ak.macro_china_cx_services_pmi_yearly()
print(macro_china_cx_services_pmi_yearly_df)
```

数据示例

```
               商品          日期    今值   预测值    前值
0    中国财新服务业PMI报告  2012-04-05  53.3   NaN  53.9
1    中国财新服务业PMI报告  2012-05-04  54.1   NaN  53.3
2    中国财新服务业PMI报告  2012-06-05  54.7   NaN  54.1
3    中国财新服务业PMI报告  2012-07-04  52.3   NaN  54.7
4    中国财新服务业PMI报告  2012-08-03  53.1   NaN  52.3
..            ...         ...   ...   ...   ...
143  中国财新服务业PMI报告  2023-12-05  51.5  50.7  50.4
144  中国财新服务业PMI报告  2024-01-04  52.9  51.6  51.5
145  中国财新服务业PMI报告  2024-02-05  52.7  53.0  52.9
146  中国财新服务业PMI报告  2024-03-05  52.5  52.9  52.7
147  中国财新服务业PMI报告  2024-04-03  52.7  52.7  52.5
[148 rows x 5 columns]
```
