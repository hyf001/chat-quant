---
title: "stock_zh_b_minute - 分时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_b_minute

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > B股 > 历史行情数据 > 分时数据
- 描述: 新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
- 目标地址: http://finance.sina.com.cn/realstock/company/sh900901/nc.shtml
- 限量: 单次返回指定股票或指数的指定频率的最近交易日的历史分时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 分时数据

接口: stock_zh_b_minute

目标地址: http://finance.sina.com.cn/realstock/company/sh900901/nc.shtml

描述: 新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权

限量: 单次返回指定股票或指数的指定频率的最近交易日的历史分时行情数据

输入参数

| 名称     | 类型  | 描述                                                         |
|--------|-----|------------------------------------------------------------|
| symbol | str | symbol='sh900901'; 同日频率数据接口                                |
| period | str | period='1'; 获取 1, 5, 15, 30, 60 分钟的数据频率                    |
| adjust | str | adjust=""; 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| day    | object  | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | float64 | -   |

接口示例

```python
import akshare as ak

stock_zh_b_minute_df = ak.stock_zh_b_minute(symbol='sh900901', period='1', adjust="qfq")
print(stock_zh_b_minute_df)
```

数据示例

```
                      day      open      high       low     close volume
0     2024-06-28 14:41:00  0.472987  0.472987  0.472987  0.472987    100
1     2024-06-28 14:42:00  0.470996  0.470996  0.470000  0.470000  12000
2     2024-06-28 14:44:00  0.470996  0.470996  0.470996  0.470996   5000
3     2024-06-28 14:45:00  0.470996  0.470996  0.470996  0.470996  43600
4     2024-06-28 14:48:00  0.470000  0.470000  0.469004  0.469004  16000
...                   ...       ...       ...       ...       ...    ...
1965  2024-07-22 14:43:00  0.498994  0.498994  0.498994  0.498994   5000
1966  2024-07-22 14:48:00  0.497988  0.497988  0.497988  0.497988   1300
1967  2024-07-22 14:56:00  0.496982  0.496982  0.496982  0.496982    200
1968  2024-07-22 14:57:00  0.497988  0.497988  0.497988  0.497988   5100
1969  2024-07-22 15:00:00  0.500000  0.500000  0.500000  0.500000    400
[1970 rows x 6 columns]
```
