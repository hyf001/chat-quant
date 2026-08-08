---
title: "macro_china_daily_energy - 中国日度沿海六大电库存"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_daily_energy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 其他指标 > 中国日度沿海六大电库存
- 描述: 中国日度沿海六大电库存数据, 数据区间从20160101-至今, 不再更新, 只能获得历史数据
- 目标地址: https://datacenter.jin10.com/reportType/dc_qihuo_energy_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中国日度沿海六大电库存

接口: macro_china_daily_energy

目标地址: https://datacenter.jin10.com/reportType/dc_qihuo_energy_report

描述: 中国日度沿海六大电库存数据, 数据区间从20160101-至今, 不再更新, 只能获得历史数据

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 日期      | object  | -  |
| 沿海六大电库存 | float64 | -  |
| 日耗      | float64 | -  |
| 存煤可用天数  | float64 | -  |

接口示例

```python
import akshare as ak

macro_china_daily_energy_df = ak.macro_china_daily_energy()
print(macro_china_daily_energy_df)
```

数据示例

```
              日期  沿海六大电库存     日耗  存煤可用天数
0     2016-01-01  1167.60  64.20   18.19
1     2016-01-02  1162.90  63.40   18.34
2     2016-01-03  1160.80  62.60   18.54
3     2016-01-04  1185.30  57.60   20.58
4     2016-01-05  1150.20  57.20   20.11
          ...      ...    ...     ...
1202  2019-05-17  1639.47  61.71   26.56
1203  2019-05-21  1591.92  62.67   25.40
1204  2019-05-22  1578.63  59.54   26.51
1205  2019-05-24  1671.83  60.65   27.56
1206  2019-06-21  1786.64  66.57   26.84
[1207 rows x 4 columns]
```
