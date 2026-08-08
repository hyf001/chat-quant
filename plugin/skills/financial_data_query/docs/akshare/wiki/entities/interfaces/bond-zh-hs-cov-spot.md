---
title: "bond_zh_hs_cov_spot - 实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_hs_cov_spot

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 实时行情数据
- 描述: 新浪财经-沪深可转债数据
- 目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
- 限量: 单次返回所有沪深可转债的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据

接口: bond_zh_hs_cov_spot

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hskzz_z

描述: 新浪财经-沪深可转债数据

限量: 单次返回所有沪深可转债的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型  | 描述    |
|-----|-----|-------|
| -   | -   | 不逐一列出 |

接口示例

```python
import akshare as ak

bond_zh_hs_cov_spot_df = ak.bond_zh_hs_cov_spot()
print(bond_zh_hs_cov_spot_df)
```

数据示例

```
       symbol  name    trade pricechange  ...   volume     amount     code    ticktime
0    sh110044  广电转债  164.404      -7.464  ...   463810   78867792  110044  15:00:01
1    sh110045  海澜转债  135.440      -0.737  ...   814670  110615438  110045  15:00:01
2    sh110047  山鹰转债  109.574      -0.846  ...   610430   67002925  110047  15:00:01
3    sh110048  福能转债  161.464       0.083  ...  1146040  187753075  110048  15:00:01
4    sh110052  贵广转债  121.081      -4.359  ...   466970   58073701  110052  15:00:01
..        ...   ...      ...         ...  ...      ...        ...     ...       ...
555  sz128138  侨银转债  117.980      -0.220  ...    84537    9982766  128138  15:00:00
556  sz128141  旺能转债  114.511      -3.023  ...   328740   38135547  128141  15:00:00
557  sz128142  新乳转债  108.094      -0.223  ...   106070   11479168  128142  15:00:00
558  sz128143  锋龙转债  132.097      -7.166  ...  1053140  142958765  128143  15:00:00
559  sz128144  利民转债  104.313      -1.542  ...   161388   16911258  128144  15:00:00
[560 rows x 15 columns]
```
