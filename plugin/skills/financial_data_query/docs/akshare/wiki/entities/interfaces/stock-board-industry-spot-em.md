---
title: "stock_board_industry_spot_em - 东方财富-行业板块-实时行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_board_industry_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 行业板块 > 东方财富-行业板块-实时行情
- 描述: 东方财富网-沪深板块-行业板块-实时行情
- 目标地址: https://quote.eastmoney.com/bk/90.BK1027.html
- 限量: 单次返回指定板块的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 东方财富-行业板块-实时行情

接口: stock_board_industry_spot_em

目标地址: https://quote.eastmoney.com/bk/90.BK1027.html

描述: 东方财富网-沪深板块-行业板块-实时行情

限量: 单次返回指定板块的实时行情数据

输入参数

| 名称     | 类型  | 描述           |
|--------|-----|--------------|
| symbol | str | symbol="小金属" |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| item  | object  | -  |
| value | float64 | -  |

接口示例

```python
import akshare as ak

stock_board_industry_spot_em_df = ak.stock_board_industry_spot_em(symbol="小金属")
print(stock_board_industry_spot_em_df)
```

数据示例

```
  item         value
0   最新  1.957370e+03
1   最高  1.990130e+03
2   最低  1.953700e+03
3   开盘  1.964160e+03
4  成交量  1.386981e+07
5  成交额  2.165428e+10
6  换手率  2.970000e+00
7  涨跌额 -1.791000e+01
8  涨跌幅 -9.100000e-01
9   振幅  1.840000e+00
```
