---
title: "macro_china_passenger_load_factor - 民航客座率及载运率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_passenger_load_factor

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 民航客座率及载运率
- 描述: 国家统计局-民航客座率及载运率
- 目标地址: http://finance.sina.com.cn/mac/#industry-20-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 民航客座率及载运率

接口: macro_china_passenger_load_factor

目标地址: http://finance.sina.com.cn/mac/#industry-20-0-31-1

描述: 国家统计局-民航客座率及载运率

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 统计年度 | object  | 年月      |
| 客座率  | float64 | 注意单位: % |
| 载运率  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_passenger_load_factor_df = ak.macro_china_passenger_load_factor()
print(macro_china_passenger_load_factor_df)
```

数据示例

```
     统计时间    客座率    载运率
0    2023.7  81.20  68.50
1    2023.6  78.60  69.30
2    2023.5  74.30  65.90
3    2023.4  75.90  66.10
4    2023.3  74.70  66.20
..      ...    ...    ...
202  2006.6  72.00  64.60
203  2006.5  71.30  64.40
204  2006.4  76.30  69.00
205  2006.3  72.40  67.50
206  2006.2  72.70  64.60
[207 rows x 3 columns]
```
