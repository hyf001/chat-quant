---
title: "stock_intraday_em - 日内分时数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_intraday_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 日内分时数据-东财
- 描述: 东方财富-分时数据
- 目标地址: https://quote.eastmoney.com/f1.html?newcode=0.000001
- 限量: 单次返回指定股票最近一个交易日的分时数据, 包含盘前数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 日内分时数据-东财

接口: stock_intraday_em

目标地址: https://quote.eastmoney.com/f1.html?newcode=0.000001

描述: 东方财富-分时数据

限量: 单次返回指定股票最近一个交易日的分时数据, 包含盘前数据

输入参数

| 名称         | 类型  | 描述                                  |
|------------|-----|-------------------------------------|
| symbol     | str | symbol="000001"; 股票代码               |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 时间    | object  | -  |
| 成交价   | float64 | -  |
| 手数    | int64   | -  |
| 买卖盘性质 | object  | -  |

接口示例

```python
import akshare as ak

stock_intraday_em_df = ak.stock_intraday_em(symbol="000001")
print(stock_intraday_em_df)
```

数据示例

```
         时间    成交价    手数 买卖盘性质
0     09:15:00  10.60    11   中性盘
1     09:15:09  10.57  1547   中性盘
2     09:15:18  10.57  1549   中性盘
3     09:15:27  10.57  1549   中性盘
4     09:15:36  10.57  1552   中性盘
        ...    ...   ...   ...
4396  14:56:51  10.50    30    买盘
4397  14:56:54  10.49   109    卖盘
4398  14:56:57  10.49    27    卖盘
4399  14:57:00  10.50    68    买盘
4400  15:00:00  10.50  8338    买盘
[4401 rows x 4 columns]
```
