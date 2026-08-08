---
title: "energy_carbon_gz - 碳排放权-广州"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_gz

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-广州
- 描述: 广州碳排放权交易中心-行情信息
- 目标地址: http://www.cnemission.com/article/hqxx/
- 限量: 该接口返回从 2013-12-19 至今的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-广州

接口: energy_carbon_gz

目标地址: http://www.cnemission.com/article/hqxx/

描述: 广州碳排放权交易中心-行情信息

限量: 该接口返回从 2013-12-19 至今的所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 日期   | object  | -       |
| 品种   | object  | -       |
| 开盘价  | float64 | -       |
| 收盘价  | float64 | -       |
| 最高价  | float64 | -       |
| 最低价  | float64 | -       |
| 涨跌   | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |
| 成交数量 | int64   | -       |
| 成交金额 | float64 | -       |

接口示例

```python
import akshare as ak

energy_carbon_gz_df = ak.energy_carbon_gz()
print(energy_carbon_gz_df)
```

数据示例

```
          日期    品种    开盘价    收盘价  ...    涨跌   涨跌幅    成交数量        成交金额
0     2013-12-19  GDEA  60.00  60.17  ...  0.17  0.28  120029  7221740.00
1     2013-12-20  GDEA  60.17  60.00  ... -0.17 -0.28     100     6000.00
2     2014-03-11  GDEA  60.00  60.00  ...  0.00  0.00    5242   314520.00
3     2014-03-14  GDEA  60.00  63.00  ...  3.00  5.00     200    12600.00
4     2014-03-17  GDEA  63.00  65.00  ...  2.00  3.17     100     6500.00
          ...   ...    ...    ...  ...   ...   ...     ...         ...
1718  2022-02-28  GDEA  72.24  71.38  ... -0.86 -1.19    9468   675792.95
1719  2022-03-01  GDEA  71.38  69.44  ... -1.94 -2.72    3239   224927.37
1720  2022-03-02  GDEA  69.44  69.57  ...  0.13  0.19   18551  1290675.12
1721  2022-03-03  GDEA  69.57  66.95  ... -2.62 -3.77  135661  8450773.49
1722  2022-03-04  GDEA  66.95  66.80  ... -0.15 -0.22    8042   537213.18
```
