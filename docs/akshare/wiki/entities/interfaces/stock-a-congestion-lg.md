---
title: "stock_a_congestion_lg - 大盘拥挤度"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_a_congestion_lg

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 大盘拥挤度
- 描述: 乐咕乐股-大盘拥挤度
- 目标地址: https://legulegu.com/stockdata/ashares-congestion
- 限量: 单次获取近 4 年的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 大盘拥挤度

接口: stock_a_congestion_lg

目标地址: https://legulegu.com/stockdata/ashares-congestion

描述: 乐咕乐股-大盘拥挤度

限量: 单次获取近 4 年的历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述  |
|------------|---------|-----|
| date       | object  | 日期  |
| close      | float64 | 收盘价 |
| congestion | float64 | 拥挤度 |

接口示例

```python
import akshare as ak

stock_a_congestion_lg_df = ak.stock_a_congestion_lg()
print(stock_a_congestion_lg_df)
```

数据示例

```
           date    close  congestion
0    2020-04-27  2815.49      0.3783
1    2020-04-28  2810.02      0.3797
2    2020-04-29  2822.44      0.3876
3    2020-04-30  2860.08      0.4009
4    2020-05-06  2878.14      0.4080
..          ...      ...         ...
962  2024-04-18  3074.22      0.3848
963  2024-04-19  3065.26      0.3896
964  2024-04-22  3044.60      0.3834
965  2024-04-23  3021.98      0.3808
966  2024-04-24  3044.82      0.3786
[967 rows x 3 columns]
```
