---
title: "bond_zh_hs_cov_pre_min - 历史行情数据-盘前分时"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_hs_cov_pre_min

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 历史行情数据-盘前分时
- 描述: 东方财富网-可转债-分时行情-盘前分时
- 目标地址: https://quote.eastmoney.com/concept/sz128039.html
- 限量: 单次返回指定可转债在最近一个交易日的盘前分时数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情数据-盘前分时

接口: bond_zh_hs_cov_pre_min

目标地址: https://quote.eastmoney.com/concept/sz128039.html

描述: 东方财富网-可转债-分时行情-盘前分时

限量: 单次返回指定可转债在最近一个交易日的盘前分时数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 时间  | object  | -       |
| 开盘  | float64 | -       |
| 收盘  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 成交量 | float64 | 注意单位: 手 |
| 成交额 | float64 | -       |
| 最新价 | float64 | -       |

接口示例

```python
import akshare as ak

bond_zh_hs_cov_pre_min_df = ak.bond_zh_hs_cov_pre_min(symbol="sh113570")
print(bond_zh_hs_cov_pre_min_df)
```

数据示例

```
                 时间      开盘     收盘  ...  成交量     成交额    最新价
0    2022-07-27 09:15:00  128.14  128.14  ...    0       0.0  128.1400
1    2022-07-27 09:16:00  128.14  128.14  ...    0       0.0  127.9800
2    2022-07-27 09:17:00  128.03  128.03  ...    0       0.0  127.9800
3    2022-07-27 09:18:00  128.30  128.30  ...    0       0.0  127.9800
4    2022-07-27 09:19:00  128.30  128.30  ...    0       0.0  127.9800
..                   ...     ...     ...  ...  ...       ...       ...
131  2022-07-27 11:26:00  128.89  128.89  ...   37   47688.0  128.4185
132  2022-07-27 11:27:00  128.83  128.71  ...   27   34765.0  128.4193
133  2022-07-27 11:28:00  128.71  128.80  ...   21   27043.0  128.4201
134  2022-07-27 11:29:00  128.80  128.81  ...   85  109487.0  128.4232
135  2022-07-27 11:30:00  128.81  128.78  ...    7    9016.0  128.4235
```
