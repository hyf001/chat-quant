---
title: "bond_cb_adj_logs_jsl - 可转债转股价格调整记录-集思录"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cb_adj_logs_jsl

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 可转债转股价格调整记录-集思录
- 描述: 集思录-单个可转债的转股价格-调整记录
- 目标地址: https://app.jisilu.cn/data/cbnew/#cb; 点击带红色星号的转股价会弹出转股价调整记录
- 限量: 返回当前时刻该可转债的所有转股价格调整记录
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 可转债转股价格调整记录-集思录

接口: bond_cb_adj_logs_jsl

目标地址: https://app.jisilu.cn/data/cbnew/#cb; 点击带红色星号的转股价会弹出转股价调整记录

描述: 集思录-单个可转债的转股价格-调整记录

限量: 返回当前时刻该可转债的所有转股价格调整记录

输入参数

| 名称     | 类型  | 描述                     |
|--------|-----|------------------------|
| symbol | str | symbol="128013"; 可转债代码 |

输出参数

| 名称       | 类型      | 描述  |
|----------|---------|-----|
| 转债名称     | object  | -   |
| 股东大会日    | object  | -   |
| 下修前转股价   | float64 | -   |
| 下修后转股价   | float64 | -   |
| 新转股价生效日期 | object  | -   |
| 下修底价     | float64 | -   |

接口示例

```python
import akshare as ak

bond_convert_adj_logs_jsl_df = ak.bond_cb_adj_logs_jsl(symbol="128013")
print(bond_convert_adj_logs_jsl_df)
```

数据示例

```
   转债名称  股东大会日  下修前转股价 下修后转股价 新转股价生效日期 下修底价
0  洪涛转债  2021-02-23    3.10    2.32  2021-02-24  2.32
1  洪涛转债  2020-06-29    8.00    3.12  2020-06-30  3.12
2  洪涛转债  2019-11-20    9.97    8.00  2019-11-21  3.10
```
