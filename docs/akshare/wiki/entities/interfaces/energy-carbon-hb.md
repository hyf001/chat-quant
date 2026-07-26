---
title: "energy_carbon_hb - 碳排放权-湖北"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_hb

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-湖北
- 描述: 湖北碳排放权交易中心-碳排放权交易数据
- 目标地址: http://www.cerx.cn/dailynewsOuter/index.htm
- 限量: 返回从 2014-04-02 至今的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-湖北

接口: energy_carbon_hb

目标地址: http://www.cerx.cn/dailynewsOuter/index.htm

描述: 湖北碳排放权交易中心-碳排放权交易数据

限量: 返回从 2014-04-02 至今的所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 日期  | object  | -  |
| 成交价 | float64 | -  |
| 成交量 | float64 | -  |
| 最新  | float64 | -  |
| 涨跌  | float64 | -  |

接口示例

```python
import akshare as ak

energy_carbon_hb_df = ak.energy_carbon_hb()
print(energy_carbon_hb_df)
```

数据示例

```
          日期    成交价    成交量   最新   涨跌
0     2014-04-02  21.00  510020.0  0.0  0.0
1     2014-04-03  24.20   51468.0  0.0  0.0
2     2014-04-04  26.61  304125.0  0.0  0.0
3     2014-04-08  26.57  112057.0  0.0  0.0
4     2014-04-09  25.07   77473.0  0.0  0.0
...          ...    ...       ...  ...  ...
2433  2024-06-03  41.72    1314.0  0.0  0.0
2434  2024-06-04  42.01    3260.0  0.0  0.0
2435  2024-06-05  42.09    7031.0  0.0  0.0
2436  2024-06-06  41.97    3691.0  0.0  0.0
2437  2024-06-07  42.41   17613.0  0.0  0.0
[2438 rows x 5 columns]
```
