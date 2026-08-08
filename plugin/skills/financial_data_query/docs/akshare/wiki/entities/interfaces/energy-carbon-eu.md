---
title: "energy_carbon_eu - 碳排放权-国际"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_eu

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-国际
- 描述: 深圳碳排放交易所-国际碳情
- 目标地址: http://www.cerx.cn/dailynewsOuter/index.htm
- 限量: 返回从 2018-03-13 至 2020-04-29 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-国际

接口: energy_carbon_eu

目标地址: http://www.cerx.cn/dailynewsOuter/index.htm

描述: 深圳碳排放交易所-国际碳情

限量: 返回从 2018-03-13 至 2020-04-29 的所有历史数据

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

energy_carbon_eu_df = ak.energy_carbon_eu()
print(energy_carbon_eu_df)
```

数据示例

```
      交易日期 市场交易指数  开盘价  最高价  最低价  成交均价    收盘价  成交量  成交额
0     2018-03-13  欧盟EUA  NaN  NaN  NaN   NaN  11.40  15880000.0  NaN
1     2018-03-13  欧盟CER  NaN  NaN  NaN   NaN   0.19         NaN  NaN
2     2018-03-14  欧盟EUA  NaN  NaN  NaN   NaN  11.18  17926000.0  NaN
3     2018-03-14  欧盟CER  NaN  NaN  NaN   NaN   0.19      3000.0  NaN
4     2018-03-15  欧盟EUA  NaN  NaN  NaN   NaN  11.19  17290000.0  NaN
          ...    ...  ...  ...  ...   ...    ...         ...  ...
997   2020-04-27  欧盟CER  NaN  NaN  NaN   NaN   0.24      1000.0  NaN
998   2020-04-28  欧盟EUA  NaN  NaN  NaN   NaN  20.21  21249000.0  NaN
999   2020-04-28  欧盟CER  NaN  NaN  NaN   NaN   0.25      1000.0  NaN
1000  2020-04-29  欧盟EUA  NaN  NaN  NaN   NaN  20.19  18621000.0  NaN
1001  2020-04-29  欧盟CER  NaN  NaN  NaN   NaN   0.25     96000.0  NaN
```
