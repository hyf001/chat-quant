---
title: "energy_carbon_bj - 碳排放权-北京"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_bj

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-北京
- 描述: 北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
- 目标地址: https://www.bjets.com.cn/article/jyxx/
- 限量: 全部历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-北京

接口: energy_carbon_bj

目标地址: https://www.bjets.com.cn/article/jyxx/

描述: 北京市碳排放权电子交易平台-北京市碳排放权公开交易行情

注意: 注意在 2017-08-08 日的数据有误 70.074.00（BEA）

限量: 全部历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 日期   | object  |           |
| 成交量  | int64   | 注意单位: 吨   |
| 成交均价 | float64 | 注意单位: 元/吨 |
| 成交额  | float64 | 注意单位: 元   |
| 成交单位 | object  | -         |

接口示例

```python
import akshare as ak

energy_carbon_bj_df = ak.energy_carbon_bj()
print(energy_carbon_bj_df)
```

数据示例

```
          日期     成交量   成交均价     成交额  成交单位
0     2013-11-28     800  51.25        NaN   NaN
1     2013-12-02     300  55.10        NaN   NaN
2     2013-12-05     100  50.20        NaN   NaN
3     2013-12-06     100  50.00        NaN   NaN
4     2013-12-11     100  50.50        NaN   NaN
          ...     ...    ...        ...   ...
1456  2022-01-04    8370  83.00   694710.0  None
1457  2022-01-12  100000  74.60  7460000.0   BEA
1458  2022-02-10       1  59.70       59.7   BEA
1459  2022-02-14     110  60.00     6600.0   BEA
1460  2022-03-02     100  62.00     6200.0   BEA
```
