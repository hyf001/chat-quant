---
title: "spot_hist_sge - 历史行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hist_sge

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 上海黄金交易所 > 历史行情数据
- 描述: 上海黄金交易所-数据资讯-行情走势-历史数据
- 目标地址: https://www.sge.com.cn/sjzx/mrhq
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情数据

接口: spot_hist_sge

目标地址: https://www.sge.com.cn/sjzx/mrhq

描述: 上海黄金交易所-数据资讯-行情走势-历史数据

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                      |
|--------|-----|---------------------------------------------------------|
| symbol | str | symbol="Au99.99"; 可以通过 ak.spot_symbol_table_sge() 获取品种表 |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| date  | object  | -   |
| open  | float64 | -   |
| close | float64 | -   |
| low   | float64 | -   |
| high  | float64 | -   |

接口示例

```python
import akshare as ak

spot_hist_sge_df = ak.spot_hist_sge(symbol='Au99.99')
print(spot_hist_sge_df)
```

数据示例

```
            date    open   close     low    high
0     2016-12-19  262.45  262.76  262.02  263.50
1     2016-12-20  262.88  262.06  261.42  263.70
2     2016-12-21  262.40  260.97  258.60  262.65
3     2016-12-22  261.18  260.00  259.05  261.18
4     2016-12-23  258.95  260.07  258.70  260.37
...          ...     ...     ...     ...     ...
1775  2024-04-15  567.01  558.68  556.00  576.99
1776  2024-04-16  559.00  562.50  552.66  569.00
1777  2024-04-17  562.61  564.46  562.02  569.00
1778  2024-04-18  566.30  563.37  558.80  568.00
1779  2024-04-19  562.80  565.55  561.00  573.96
[1780 rows x 5 columns]
```
