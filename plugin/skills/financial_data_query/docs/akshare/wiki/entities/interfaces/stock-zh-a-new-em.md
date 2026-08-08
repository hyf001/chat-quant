---
title: "stock_zh_a_new_em - 新股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_new_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 新股
- 描述: 东方财富网-行情中心-沪深个股-新股
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#newshares
- 限量: 单次返回当前交易日新股板块的所有股票的行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 新股

接口: stock_zh_a_new_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#newshares

描述: 东方财富网-行情中心-沪深个股-新股

限量: 单次返回当前交易日新股板块的所有股票的行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 序号     | int64   | -       |
| 代码     | object  | -       |
| 名称     | object  | -       |
| 最新价    | float64 | -       |
| 涨跌幅    | float64 | 注意单位: % |
| 涨跌额    | float64 | -       |
| 成交量    | float64 | -       |
| 成交额    | float64 | -       |
| 振幅     | float64 | 注意单位: % |
| 最高     | float64 | -       |
| 最低     | float64 | -       |
| 今开     | float64 | -       |
| 昨收     | float64 | -       |
| 量比     | float64 | -       |
| 换手率    | float64 | 注意单位: % |
| 市盈率-动态 | float64 | -       |
| 市净率    | float64 | -       |

接口示例

```python
import akshare as ak

stock_zh_a_new_em_df = ak.stock_zh_a_new_em()
print(stock_zh_a_new_em_df)
```

数据示例

```
      序号      代码    名称     最新价   涨跌幅  ...      昨收    量比    换手率  市盈率-动态   市净率
0      1  301559  N中集环   23.95 -1.11  ...   24.22   NaN  50.66   20.05  2.92
1      2  688657   C浩辰   89.26  0.42  ...   88.89  0.62  29.22   76.48  2.91
2      3  688719   C爱科   60.33  0.05  ...   60.30  0.44  18.92   45.79  2.86
3      4  301558   C三态   14.72  1.73  ...   14.47  0.66  38.74   71.25  8.58
4      5  603276  恒兴新材   24.17 -0.62  ...   24.32  0.40  12.34   43.70  2.24
..   ...     ...   ...     ...   ...  ...     ...   ...    ...     ...   ...
261  262  688152  麒麟信安   81.80  2.06  ...   80.15  1.26   9.45 -225.22  5.02
262  263  688372  伟测科技  103.70  2.65  ...  101.02  0.98   5.67   83.07  4.95
263  264  688291   金橙子   30.13  4.22  ...   28.91  1.09   6.76   60.43  3.37
264  265  001322  箭牌家居   13.56  1.12  ...   13.41  0.82   3.14   38.40  2.75
265  266  688426  康为世纪   32.25  3.80  ...   31.07  1.76   6.44 -183.28  2.10
[266 rows x 17 columns]
```
