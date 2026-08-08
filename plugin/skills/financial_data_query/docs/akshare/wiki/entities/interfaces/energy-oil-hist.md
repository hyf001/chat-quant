---
title: "energy_oil_hist - 汽柴油历史调价信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_oil_hist

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 中国油价 > 汽柴油历史调价信息
- 描述: 东方财富-数据中心-中国油价-汽柴油历史调价信息
- 目标地址: https://data.eastmoney.com/cjsj/oil_default.html
- 限量: 单次返回中国油价的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 汽柴油历史调价信息

接口: energy_oil_hist

目标地址: https://data.eastmoney.com/cjsj/oil_default.html

描述: 东方财富-数据中心-中国油价-汽柴油历史调价信息

限量: 单次返回中国油价的所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 调整日期 | object  | 价格调整的日期   |
| 汽油价格 | int64   | 注意单位: 元/吨 |
| 柴油价格 | int64   | 注意单位: 元/吨 |
| 汽油涨幅 | float64 | 注意单位: 元/吨 |
| 柴油涨幅 | float64 | 注意单位: 元/吨 |

接口示例

```python
import akshare as ak

energy_oil_hist_df = ak.energy_oil_hist()
print(energy_oil_hist_df)
```

数据示例

```
     调整日期  汽油价格  柴油价格   汽油涨跌   柴油涨跌
0    2000-06-06  2935  2430    NaN    NaN
1    2000-07-15  3135  2610  200.0  180.0
2    2000-08-18  3405  2770  270.0  160.0
3    2000-09-20  3615  3070  210.0  300.0
4    2000-10-20  3435  3440 -180.0  370.0
..          ...   ...   ...    ...    ...
272  2023-11-22  9100  8055 -340.0 -330.0
273  2023-12-06  9045  8005  -55.0  -50.0
274  2023-12-20  8630  7605 -415.0 -400.0
275  2024-01-04  8830  7795  200.0  190.0
276  2024-01-18  8780  7745  -50.0  -50.0
[277 rows x 5 columns]
```
