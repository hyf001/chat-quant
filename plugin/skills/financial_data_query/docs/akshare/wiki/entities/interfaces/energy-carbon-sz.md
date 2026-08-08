---
title: "energy_carbon_sz - 碳排放权-深圳"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_sz

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-深圳
- 描述: 深圳碳排放交易所-国内碳情
- 目标地址: http://www.cerx.cn/dailynewsCN/index.htm
- 限量: 全部历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-深圳

接口: energy_carbon_sz

目标地址: http://www.cerx.cn/dailynewsCN/index.htm

描述: 深圳碳排放交易所-国内碳情

限量: 全部历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 交易日期   | object  | -   |
| 市场交易指数 | object  | -   |
| 开盘价    | float64 | -   |
| 最高价    | float64 | -   |
| 最低价    | float64 | -   |
| 成交均价   | float64 | -   |
| 收盘价    | float64 | -   |
| 成交量    | int64   | -   |
| 成交额    | float64 | -   |

接口示例

```python
import akshare as ak

energy_carbon_sz_df = ak.energy_carbon_sz()
print(energy_carbon_sz_df)
```

数据示例

```
     交易日期    市场交易指数   开盘价    最高价    最低价   成交均价    收盘价  成交量    成交额
0    2022-01-21  SZA-2014  10.54  10.54  10.54  10.54  10.54    1  10.54
1    2022-01-21  SZA-2020  13.80    NaN    NaN    NaN  13.80    0   0.00
2    2022-01-21  SZA-2019  16.28  16.28  16.28  16.28  16.28    1  16.28
3    2022-01-21  SZA-2015  16.02  19.58  16.02  16.62  16.02    6  99.74
4    2022-01-21  SZA-2017   6.41    NaN    NaN    NaN   6.41    0   0.00
..          ...       ...    ...    ...    ...    ...    ...  ...    ...
195  2022-03-03  SZA-2016   4.82    NaN    NaN    NaN   4.82    0   0.00
196  2022-03-03  SZA-2017   4.20    NaN    NaN    NaN   4.20    0   0.00
197  2022-03-03  SZA-2018   6.00   6.00   6.00   6.00   6.00    1   6.00
198  2022-03-03  SZA-2019   6.88    NaN    NaN    NaN   6.88    0   0.00
199  2022-03-03  SZA-2020   4.78    NaN    NaN    NaN   4.78    0   0.00
```
