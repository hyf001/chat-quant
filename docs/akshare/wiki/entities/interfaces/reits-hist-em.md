---
title: "reits_hist_em - REITs-历史行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# reits_hist_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > REITs > REITs-历史行情
- 描述: 东方财富网-行情中心-REITs-沪深 REITs-历史行情
- 目标地址: https://quote.eastmoney.com/sh508097.html
- 限量: 单次返回指定 symbol 的历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### REITs-历史行情

接口: reits_hist_em

目标地址: https://quote.eastmoney.com/sh508097.html

描述: 东方财富网-行情中心-REITs-沪深 REITs-历史行情

限量: 单次返回指定 symbol 的历史行情数据

输入参数

| 名称     | 类型  | 描述                        |
|--------|-----|---------------------------|
| symbol | str | symbol="508097"; REITs 代码 |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | -       |
| 今开  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 最新价 | float64 | -       |
| 成交量 | int64   | -       |
| 成交额 | float64 | -       |
| 振幅  | float64 | 注意单位: % |
| 换手  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

reits_hist_em_df = ak.reits_hist_em(symbol="508097")
print(reits_hist_em_df)
```

数据示例

```
      日期       今开    最高   最低   最新价    成交量 成交额    振幅    换手
0   2024-12-03  2.599  2.599  2.567  2.595  26355  6792450.0  1.25  0.66
1   2024-12-04  2.595  2.600  2.557  2.600   5391  1397092.0  1.66  0.13
2   2024-12-05  2.600  2.600  2.572  2.592   1481   383988.0  1.08  0.04
3   2024-12-06  2.592  2.703  2.592  2.694   3165   829019.0  4.28  0.08
4   2024-12-09  2.717  2.800  2.717  2.769   7622  2099354.0  3.08  0.19
..         ...    ...    ...    ...    ...    ...        ...   ...   ...
71  2025-03-21  3.311  3.348  3.293  3.347   2408   801004.0  1.66  0.06
72  2025-03-24  3.346  3.420  3.346  3.408   6742  2289801.0  2.21  0.17
73  2025-03-25  3.408  3.479  3.408  3.448   4742  1631309.0  2.08  0.12
74  2025-03-26  3.432  3.520  3.419  3.515   3782  1314263.0  2.93  0.09
75  2025-03-27  3.498  3.600  3.498  3.570   3915  1389384.0  2.90  0.10
[76 rows x 9 columns]
```
