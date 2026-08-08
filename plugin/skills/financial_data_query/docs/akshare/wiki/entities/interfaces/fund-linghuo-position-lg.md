---
title: "fund_linghuo_position_lg - 灵活配置型基金仓位"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_linghuo_position_lg

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金仓位 > 灵活配置型基金仓位
- 描述: 乐咕乐股-基金仓位-灵活配置型基金仓位
- 目标地址: https://legulegu.com/stockdata/fund-position/pos-linghuo
- 限量: 返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 灵活配置型基金仓位

接口: fund_linghuo_position_lg

目标地址: https://legulegu.com/stockdata/fund-position/pos-linghuo

描述: 乐咕乐股-基金仓位-灵活配置型基金仓位

限量: 返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述               |
|----------|---------|------------------|
| date     | object  | -                |
| close    | float64 | 注意单位: 沪深 300 收盘价 |
| position | float64 | 注意单位: 持仓比例       |

接口示例

```python
import akshare as ak

fund_linghuo_position_lg_df = ak.fund_linghuo_position_lg()
print(fund_linghuo_position_lg_df)
```

数据示例

```
           date    close  position
0    2017-12-04  4018.86     51.44
1    2017-12-08  4003.38     52.48
2    2017-12-15  3980.86     52.59
3    2017-12-22  4054.60     52.70
4    2017-12-29  4030.85     53.18
..          ...      ...       ...
256  2022-11-25  3775.78     69.86
257  2022-12-02  3870.95     71.01
258  2022-12-09  3998.24     71.95
259  2022-12-16  3954.23     72.73
260  2022-12-23  3828.22     72.55
```
