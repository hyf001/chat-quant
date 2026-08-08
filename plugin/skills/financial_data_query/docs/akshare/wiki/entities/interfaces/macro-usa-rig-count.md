---
title: "macro_usa_rig_count - 贝克休斯钻井报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_rig_count

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 制造业 > 贝克休斯钻井报告
- 描述: 贝克休斯钻井报告, 数据区间从 19870717-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_rig_count_summary
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 贝克休斯钻井报告

接口: macro_usa_rig_count

目标地址: https://datacenter.jin10.com/reportType/dc_rig_count_summary

描述: 贝克休斯钻井报告, 数据区间从 19870717-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称          | 类型      | 描述 |
|-------------|---------|----|
| 日期          | object  | -  |
| 钻井总数_钻井数    | float64 | -  |
| 钻井总数_变化     | float64 | -  |
| 美国石油钻井_钻井数  | float64 | -  |
| 美国石油钻井_变化   | float64 | -  |
| 混合钻井_钻井数    | float64 | -  |
| 混合钻井_变化     | float64 | -  |
| 美国天然气钻井_钻井数 | float64 | -  |
| 美国天然气钻井_变化  | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_rig_count_df = ak.macro_usa_rig_count()
print(macro_usa_rig_count_df)
```

数据示例

```
              日期  钻井总数_钻井数  钻井总数_变化  ...  混合钻井_变化  美国天然气钻井_钻井数  美国天然气钻井_变化
0     1987-07-17     922.0      NaN  ...      NaN        337.0         NaN
1     1987-07-24     917.0     -5.0  ...     -5.0        331.0        -6.0
2     1987-07-31     973.0     56.0  ...      1.0        346.0        15.0
3     1987-08-07     983.0     10.0  ...     -1.0        349.0         3.0
4     1987-08-14     998.0     15.0  ...      5.0        352.0         3.0
          ...       ...      ...  ...      ...          ...         ...
1891  2024-01-26     621.0      1.0  ...      0.0        119.0        -1.0
1892  2024-02-02     619.0     -2.0  ...      0.0        117.0        -2.0
1893  2024-02-09     623.0      4.0  ...      0.0        121.0         4.0
1894  2024-02-16     621.0     -2.0  ...      0.0        121.0         0.0
1895  2024-02-23     626.0      5.0  ...      0.0        120.0        -1.0
[1896 rows x 9 columns]
```
