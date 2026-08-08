---
title: "bond_sz_buy_back_em - 深证质押式回购"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_sz_buy_back_em

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 质押式回购 > 深证质押式回购
- 描述: 东方财富网-行情中心-债券市场-深证质押式回购
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sz_buyback
- 限量: 单次返回所有行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 深证质押式回购

接口: bond_sz_buy_back_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sz_buyback

描述: 东方财富网-行情中心-债券市场-深证质押式回购

限量: 单次返回所有行情数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 序号  | int64   | -  |
| 代码  | object  | -  |
| 名称  | object  | -  |
| 最新价 | float64 | -  |
| 涨跌额 | float64 | -  |
| 涨跌幅 | float64 | -  |
| 今开  | float64 | -  |
| 最高  | float64 | -  |
| 最低  | float64 | -  |
| 昨收  | float64 | -  |
| 成交量 | float64 | -  |
| 成交额 | float64 | -  |

接口示例

```python
import akshare as ak

bond_sz_buy_back_em_df = ak.bond_sz_buy_back_em()
print(bond_sz_buy_back_em_df)
```

数据示例

```
   序号  代码    名称   最新价  ...    最低   昨收     成交量          成交额
0   1  131810  Ｒ-001  1.555  ...  1.305  1.410  213447602  2.134476e+11
1   2  131801  Ｒ-007  1.735  ...  1.405  1.715   19034425  1.903442e+10
2   3  131800  Ｒ-003  1.490  ...  1.015  1.430    3258575  3.258575e+09
3   4  131809  Ｒ-004  1.500  ...  0.110  1.465    2571117  2.571117e+09
4   5  131811  Ｒ-002  1.525  ...  1.200  1.455    1620576  1.620576e+09
5   6  131802  Ｒ-014  1.750  ...  0.010  1.785    1312069  1.312069e+09
6   7  131803  Ｒ-028  1.740  ...  1.600  1.790     986564  9.865640e+08
7   8  131805  Ｒ-091  1.680  ...  1.000  1.815      20476  2.047600e+07
8   9  131806  Ｒ-182  1.660  ...  1.600  1.730      14124  1.412400e+07
[9 rows x 12 columns]
```
