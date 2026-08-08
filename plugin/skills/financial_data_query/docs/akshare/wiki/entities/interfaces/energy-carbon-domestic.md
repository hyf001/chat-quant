---
title: "energy_carbon_domestic - 碳排放权-国内"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, energy, parameters, returns, example]
sources: [raw/data-dictionary/energy/energy.md]
confidence: high
---
# energy_carbon_domestic

- 分类: [[energy-energy|AKShare 能源数据]]
- 主题路径: AKShare 能源数据 > 碳排放 > 碳排放权-国内
- 描述: 碳交易网-行情信息
- 目标地址: http://www.tanjiaoyi.com/
- 限量: 返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/energy/energy.html

## 相关

- [[energy-energy|AKShare 能源数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 碳排放权-国内

接口: energy_carbon_domestic

目标地址: http://www.tanjiaoyi.com/

描述: 碳交易网-行情信息

限量: 返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                      |
|--------|-----|-------------------------------------------------------------------------|
| symbol | str | symbol="湖北"; choice of {'湖北', '上海', '北京', '重庆', '广东', '天津', '深圳', '福建'} |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  |         |
| 成交价 | float64 | 注意单位: 元 |
| 成交量 | float64 | 注意单位: 吨 |
| 成交额 | float64 | -       |
| 地点  | object  | -       |

接口示例

```python
import akshare as ak

energy_carbon_domestic_df = ak.energy_carbon_domestic(symbol="湖北")
print(energy_carbon_domestic_df)
```

数据示例

```
      日期        成交价       成交量           成交额  地点
0     2014-04-02  21.000000  510020.0  1.071040e+07  湖北
1     2014-04-03  24.200001   51468.0  1.245530e+06  湖北
2     2014-04-04  26.620001  304125.0  8.092670e+06  湖北
3     2014-04-05  26.620001       0.0  0.000000e+00  湖北
4     2014-04-06  26.620001       0.0  0.000000e+00  湖北
          ...        ...       ...           ...  ..
1847  2021-03-17  31.799999     535.0  1.701280e+04  湖北
1848  2021-03-18  28.129999     551.0  1.550140e+04  湖北
1849  2021-03-19  30.350000    2074.0  6.293808e+04  湖北
1850  2021-03-22  30.350000    3073.0  9.326129e+04  湖北
1851  2021-03-23  30.350000     100.0  3.508000e+03  湖北
```
