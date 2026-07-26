---
title: "stock_zh_b_spot_em - 实时行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_b_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > B股 > 实时行情数据 > 实时行情数据-东财
- 描述: 东方财富网-实时行情数据
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#hs_b_board
- 限量: 单次返回所有 B 股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时行情数据-东财

接口: stock_zh_b_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#hs_b_board

描述: 东方财富网-实时行情数据

限量: 单次返回所有 B 股上市公司的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 序号      | int64   | -       |
| 代码      | object  | -       |
| 名称      | object  | -       |
| 最新价     | float64 | -       |
| 涨跌幅     | float64 | 注意单位: % |
| 涨跌额     | float64 | -       |
| 成交量     | float64 | 注意单位: 手 |
| 成交额     | float64 | 注意单位: 元 |
| 振幅      | float64 | 注意单位: % |
| 最高      | float64 | -       |
| 最低      | float64 | -       |
| 今开      | float64 | -       |
| 昨收      | float64 | -       |
| 量比      | float64 | -       |
| 换手率     | float64 | 注意单位: % |
| 市盈率-动态  | float64 | -       |
| 市净率     | float64 | -       |
| 总市值     | float64 | 注意单位: 元 |
| 流通市值    | float64 | 注意单位: 元 |
| 涨速      | float64 | -       |
| 5分钟涨跌   | float64 | 注意单位: % |
| 60日涨跌幅  | float64 | 注意单位: % |
| 年初至今涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_zh_b_spot_em_df = ak.stock_zh_b_spot_em()
print(stock_zh_b_spot_em_df)
```

数据示例

```
      序号      代码     名称    最新价  ...    涨速  5分钟涨跌  60日涨跌幅  年初至今涨跌幅
0      1  900953    凯马Ｂ  0.330  ...  0.00   0.92    0.00    -2.65
1      2  200625  长  安Ｂ  4.420  ...  0.00   0.23   20.11     1.38
2      3  900914   锦在线B  0.702  ...  0.14   0.29   13.96    16.42
3      4  200761   本钢板Ｂ  2.670  ...  0.00   0.38    8.54     1.14
4      5  900957   凌云Ｂ股  0.568  ...  0.00  -0.35   -6.73    -9.98
..   ...     ...    ...    ...  ...   ...    ...     ...      ...
109  110  200017   深中华B  1.210  ... -1.63  -0.82  -14.18   -15.38
110  111  900936   鄂资Ｂ股  2.630  ...  0.00  -0.53   30.46    27.92
111  112  900919   退市庭B  0.026  ...  0.00   0.00  -78.15   -86.32
112  113  900906   中毅达B  0.571  ...  0.71  -0.70   17.73    13.07
113  114  900948   伊泰Ｂ股  1.465  ... -0.61   0.14   47.38    67.81
```
