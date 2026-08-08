---
title: "futures_foreign_hist - 外盘-历史行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_foreign_hist

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 外盘-历史行情数据-新浪
- 描述: 新浪财经-期货外盘历史行情数据
- 目标地址: https://finance.sina.com.cn/futuremarket/
- 限量: 单次返回指定品种的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 外盘-历史行情数据-新浪

接口: futures_foreign_hist

目标地址: https://finance.sina.com.cn/futuremarket/

描述: 新浪财经-期货外盘历史行情数据

限量: 单次返回指定品种的历史数据

输入参数

| 名称     | 类型  | 描述                                                                           |
|--------|-----|------------------------------------------------------------------------------|
| symbol | str | symbol="ZSD"; 外盘期货的 **symbol** 可以通过 **ak.futures_hq_subscribe_exchange_symbol()** 获取 |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| date   | object  | 交易日 |
| open   | float64 | 开盘价 |
| high   | float64 | 最高价 |
| low    | float64 | 最低价 |
| close  | float64 | 收盘价 |
| volume | int64   | 成交量 |

接口示例

```python
import akshare as ak

futures_foreign_hist_df = ak.futures_foreign_hist(symbol="ZSD")
print(futures_foreign_hist_df)
```

数据示例

```
           date     open    high      low   close  volume  position  s
0    2014-01-20  2082.00  2086.0  2068.75  2076.5    1159         0  0
1    2014-01-21  2077.75  2092.5  2061.25  2089.0    1318         0  0
2    2014-01-22  2088.75  2102.0  2077.50  2084.0    1754         0  0
3    2014-01-23  2083.75  2084.0  2041.25  2045.5    2639         0  0
4    2014-01-24  2043.75  2051.0  2019.25  2025.0    2264         0  0
         ...      ...     ...      ...     ...     ...       ... ..
2541 2024-01-15  2510.00  2615.0  2506.50  2555.0    9364         0  0
2542 2024-01-16  2555.00  2567.0  2531.00  2548.5    6719         0  0
2543 2024-01-17  2548.00  2550.0  2460.00  2466.0   11555         0  0
2544 2024-01-18  2474.00  2478.5  2443.00  2466.0   10442         0  0
2545 2024-01-19  2469.50  2485.0  2454.00  2456.5    7236         0  0
[2546 rows x 8 columns]
```
