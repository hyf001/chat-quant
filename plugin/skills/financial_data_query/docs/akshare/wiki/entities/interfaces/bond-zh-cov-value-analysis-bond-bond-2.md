---
title: "bond_zh_cov_value_analysis - 可转债溢价率分析"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_cov_value_analysis

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债溢价率分析
- 描述: 东方财富网-行情中心-新股数据-可转债数据-可转债溢价率分析
- 目标地址: https://data.eastmoney.com/kzz/detail/113527.html
- 限量: 单次返回所有可转债溢价率分析数据；此接口同 bond_zh_cov_value_analysis
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债溢价率分析

接口: bond_zh_cov_value_analysis

目标地址: https://data.eastmoney.com/kzz/detail/113527.html

描述: 东方财富网-行情中心-新股数据-可转债数据-可转债溢价率分析

限量: 单次返回所有可转债溢价率分析数据；此接口同 bond_zh_cov_value_analysis

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
      日期     收盘价      纯债价值      转股价值    纯债溢价率    转股溢价率
0    2019-01-24     NaN   90.186522   98.195187  10.881313   1.837985
1    2019-01-25     NaN   90.045626   98.729947  11.054811   1.286391
2    2019-01-28     NaN   90.100390   97.593583  10.987310   2.465753
3    2019-01-29     NaN   90.105909   94.585561  10.980512   5.724382
4    2019-01-30     NaN   90.006260   94.184492  11.103384   6.174592
..          ...     ...         ...         ...        ...        ...
766  2022-03-24  123.46  107.178436  102.871795  15.191082  20.013460
767  2022-03-25  122.83  107.241827  103.076923  14.535535  19.163433
768  2022-03-28  123.37  107.300045  102.564103  14.976652  20.285750
769  2022-03-29  122.37  107.319545  101.025641  14.023964  21.127665
770  2022-03-30  122.75  107.335419  102.358974  14.361132  19.921092
```
