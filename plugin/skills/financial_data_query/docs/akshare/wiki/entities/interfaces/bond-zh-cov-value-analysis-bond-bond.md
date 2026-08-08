---
title: "bond_zh_cov_value_analysis - 可转债价值分析"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_cov_value_analysis

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债价值分析
- 描述: 东方财富网-行情中心-新股数据-可转债数据-可转债价值分析
- 目标地址: https://data.eastmoney.com/kzz/detail/113527.html
- 限量: 单次返回所有可转债价值分析数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债价值分析

接口: bond_zh_cov_value_analysis

目标地址: https://data.eastmoney.com/kzz/detail/113527.html

描述: 东方财富网-行情中心-新股数据-可转债数据-可转债价值分析

限量: 单次返回所有可转债价值分析数据

输入参数

| 名称     | 类型  | 描述                     |
|--------|-----|------------------------|
| symbol | str | symbol="113527"; 可转债代码 |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 日期    | object  | -       |
| 收盘价   | float64 | 注意单位: 元 |
| 纯债价值  | float64 | 注意单位: 元 |
| 转股价值  | float64 | 注意单位: 元 |
| 纯债溢价率 | float64 | 注意单位: % |
| 转股溢价率 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

bond_zh_cov_value_analysis_df = ak.bond_zh_cov_value_analysis(symbol="113527")
print(bond_zh_cov_value_analysis_df)
```

数据示例

```
        日期      收盘价      纯债价值      转股价值    纯债溢价率    转股溢价率
0     2019-01-24      NaN   90.156612   98.195187  10.918098   1.837985
1     2019-01-25      NaN   90.015417   98.729947  11.092081   1.286391
2     2019-01-28      NaN   90.070170   97.593583  11.024549   2.465753
3     2019-01-29      NaN   90.075261   94.585561  11.018274   5.724382
4     2019-01-30      NaN   89.976132   94.184492  11.140586   6.174592
          ...      ...         ...         ...        ...        ...
1229  2024-02-22  122.183  112.436703   98.963731   8.668252  23.462403
1230  2024-02-23  121.745  112.471066   99.274611   8.245618  22.634577
1231  2024-02-26  122.580  112.497496  102.383420   8.962425  19.726417
1232  2024-02-27  122.030  112.525381  103.212435   8.446645  18.231878
1233  2024-02-28  116.601  112.526608   92.953368   3.620825  25.440318
[1234 rows x 6 columns]
```
