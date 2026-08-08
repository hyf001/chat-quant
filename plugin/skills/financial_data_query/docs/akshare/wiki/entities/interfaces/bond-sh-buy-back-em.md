---
title: "bond_sh_buy_back_em - 上证质押式回购"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_sh_buy_back_em

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 质押式回购 > 上证质押式回购
- 描述: 东方财富网-行情中心-债券市场-上证质押式回购
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sh_buyback
- 限量: 单次返回所有行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上证质押式回购

接口: bond_sh_buy_back_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sh_buyback

描述: 东方财富网-行情中心-债券市场-上证质押式回购

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

bond_sh_buy_back_em_df = ak.bond_sh_buy_back_em()
print(bond_sh_buy_back_em_df)
```

数据示例

```
   序号 代码    名称    最新价  ...  最低    昨收    成交量          成交额
0   1  204001  GC001  1.600  ...  1.200  1.440  1820652598  1.820653e+12
1   2  204007  GC007  1.735  ...  1.600  1.715   189609010  1.896090e+11
2   3  204014  GC014  1.745  ...  1.600  1.750    26214422  2.621442e+10
3   4  204004  GC004  1.560  ...  1.200  1.475    18866666  1.886667e+10
4   5  204003  GC003  1.565  ...  1.250  1.485    11683291  1.168329e+10
5   6  204028  GC028  1.795  ...  1.630  1.810    10913644  1.091364e+10
6   7  204002  GC002  1.580  ...  1.200  1.470    10655418  1.065542e+10
7   8  204091  GC091  1.795  ...  1.655  1.795      751463  7.514630e+08
8   9  204182  GC182  1.755  ...  1.600  1.800       84107  8.410700e+07
[9 rows x 12 columns]
```
