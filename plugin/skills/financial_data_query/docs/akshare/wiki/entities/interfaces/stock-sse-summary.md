---
title: "stock_sse_summary - 上海证券交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sse_summary

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 股票市场总貌 > 上海证券交易所
- 描述: 上海证券交易所-股票数据总貌
- 目标地址: http://www.sse.com.cn/market/stockdata/statistic/
- 限量: 单次返回最近交易日的股票数据总貌(当前交易日的数据需要交易所收盘后统计)
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海证券交易所

接口: stock_sse_summary

目标地址: http://www.sse.com.cn/market/stockdata/statistic/

描述: 上海证券交易所-股票数据总貌

限量: 单次返回最近交易日的股票数据总貌(当前交易日的数据需要交易所收盘后统计)

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数-实时行情数据

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 项目  | object | -   |
| 股票  | object | -   |
| 科创板 | object | -   |
| 主板  | object | -   |

接口示例

```python
import akshare as ak

stock_sse_summary_df = ak.stock_sse_summary()
print(stock_sse_summary_df)
```

数据示例

```
      项目     股票       科创板         主板
0   流通股本   40403.47    413.63   39989.84
1    总市值  516714.68   55719.6  460995.09
2  平均市盈率      17.92      71.0      16.51
3   上市公司       2036       377       1659
4   上市股票       2078       377       1701
5   流通市值  432772.13   22274.3  410497.83
6   报告时间   20211230  20211230   20211230
8    总股本   46234.03    1211.5   45022.54
```
