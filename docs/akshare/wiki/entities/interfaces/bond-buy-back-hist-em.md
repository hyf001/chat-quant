---
title: "bond_buy_back_hist_em - 质押式回购历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_buy_back_hist_em

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 质押式回购 > 质押式回购历史数据
- 描述: 东方财富网-行情中心-债券市场-质押式回购-历史数据
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sh_buyback
- 限量: 单次返回所有历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 质押式回购历史数据

接口: bond_buy_back_hist_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#bond_sh_buyback

描述: 东方财富网-行情中心-债券市场-质押式回购-历史数据

限量: 单次返回所有历史行情数据

输入参数

| 名称     | 类型  | 描述                       |
|--------|-----|--------------------------|
| symbol | str | symbol="204001"; 质押式回购代码 |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 日期  | int64   | -  |
| 开盘  | float64 | -  |
| 收盘  | float64 | -  |
| 最高  | float64 | -  |
| 最低  | float64 | -  |
| 成交量 | float64 | -  |
| 成交额 | float64 | -  |

接口示例

```python
import akshare as ak

bond_buy_back_hist_em_df = ak.bond_buy_back_hist_em(symbol="204001")
print(bond_buy_back_hist_em_df)
```

数据示例

```
           日期    开盘  收盘    最高    最低        成交量     成交额
0     2006-05-08  1.50  1.500  1.500  1.50         100  1.000000e+05
1     2006-05-16  1.65  1.650  1.650  1.65       10000  1.000000e+07
2     2006-05-22  1.62  1.620  1.620  1.62         500  5.000000e+05
3     2006-06-01  3.06  3.060  3.060  3.06       50000  5.000000e+07
4     2006-06-12  1.62  1.620  1.620  1.62         400  4.000000e+05
...          ...   ...    ...    ...   ...         ...           ...
4565  2025-03-28  2.25  3.595  5.100  2.22  1777635143  1.777635e+12
4566  2025-03-31  2.90  2.780  3.900  1.30  1900163681  1.900164e+12
4567  2025-04-01  2.11  1.745  2.130  1.65  1848921966  1.848922e+12
4568  2025-04-02  1.86  1.440  1.955  1.20  1797375867  1.797376e+12
4569  2025-04-03  1.80  1.600  1.815  1.20  1820652598  1.820653e+12
[4570 rows x 7 columns]
```
