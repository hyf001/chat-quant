---
title: "fund_value_estimation_em - 净值估算"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_value_estimation_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 净值估算
- 描述: 东方财富网-数据中心-净值估算
- 目标地址: http://fund.eastmoney.com/fundguzhi.html
- 限量: 单次返回当前交易日指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 净值估算

接口: fund_value_estimation_em

目标地址: http://fund.eastmoney.com/fundguzhi.html

描述: 东方财富网-数据中心-净值估算

限量: 单次返回当前交易日指定 symbol 的所有数据

说明: 非交易时段若上游返回“暂无数据”，则返回空的 `pandas.DataFrame`，不再抛出异常

输入参数

| 名称     | 类型  | 描述                                                                                                    |
|--------|-----|-------------------------------------------------------------------------------------------------------|
| symbol | str | symbol='全部'; 默认返回所有数据; choice of {'全部', '股票型', '混合型', '债券型', '指数型', 'QDII', 'ETF联接', 'LOF', '场内交易基金'} |

输出参数

| 名称             | 类型    | 描述  |
|----------------|-------|-----|
| 序号             | str   | -   |
| 基金代码           | str   | -   |
| 基金名称           | str   | -   |
| 交易日-估算数据-估算值   | float | -   |
| 交易日-估算数据-估算增长率 | str   | -   |
| 交易日-公布数据-单位净值  | float | -   |
| 交易日-公布数据-日增长率  | str   | -   |
| 估算偏差           | str   | -   |
| 交易日-单位净值       | str   | -   |

接口示例

```python
import akshare as ak

fund_value_estimation_em_df = ak.fund_value_estimation_em(symbol="混合型")
print(fund_value_estimation_em_df)
```

数据示例

```
        序号    基金代码  ...    估算偏差 2021-02-18-单位净值
0        1  164403  ...   0.06%          1.6720
1        2  180020  ...  -0.34%          1.9700
2        3  161810  ...  -0.47%          3.3300
3        4  009394  ...  -1.04%          1.0705
4        5  001763  ...   1.37%          1.5990
    ...     ...  ...     ...             ...
4846  4847  010895  ...     ---             ---
4847  4848  010875  ...     ---             ---
4848  4849  010718  ...     ---             ---
4849  4850  010717  ...     ---             ---
4850  4851  011059  ...     ---             ---
```
