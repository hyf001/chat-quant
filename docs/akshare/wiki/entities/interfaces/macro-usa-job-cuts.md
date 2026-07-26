---
title: "macro_usa_job_cuts - 美国挑战者企业裁员人数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_job_cuts

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 失业率 > 美国挑战者企业裁员人数报告
- 描述: 美国挑战者企业裁员人数报告, 数据区间从 19940201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_job_cuts
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国挑战者企业裁员人数报告

接口: macro_usa_job_cuts

目标地址: https://datacenter.jin10.com/reportType/dc_usa_job_cuts

描述: 美国挑战者企业裁员人数报告, 数据区间从 19940201-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 商品  | object  | -        |
| 日期  | object  | -        |
| 今值  | float64 | 注意单位: 万人 |
| 预测值 | float64 | 注意单位: 万人 |
| 前值  | float64 | 注意单位: 万人 |

接口示例

```python
import akshare as ak

macro_usa_job_cuts_df = ak.macro_usa_job_cuts()
print(macro_usa_job_cuts_df)
```

数据示例

```
              商品          日期       今值  预测值       前值
0    美国挑战者企业裁员人数  1994-02-01  10.8900  NaN      NaN
1    美国挑战者企业裁员人数  1994-03-01   3.4600  NaN  10.8900
2    美国挑战者企业裁员人数  1994-04-01   4.9000  NaN   3.4600
3    美国挑战者企业裁员人数  1994-05-01   3.6100  NaN   4.9000
4    美国挑战者企业裁员人数  1994-06-01   3.6300  NaN   3.6100
..           ...         ...      ...  ...      ...
360  美国挑战者企业裁员人数  2023-12-07   4.5510  NaN   3.6836
361  美国挑战者企业裁员人数  2024-01-04   3.4817  NaN   4.5510
362  美国挑战者企业裁员人数  2024-02-01   8.2307  NaN   3.4817
363  美国挑战者企业裁员人数  2024-03-07   8.4638  NaN   8.2307
364  美国挑战者企业裁员人数  2024-04-04   9.0309  NaN   8.4638
[365 rows x 5 columns]
```
