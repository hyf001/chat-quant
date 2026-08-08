---
title: "stock_hk_main_board_spot_em - 港股主板实时行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_main_board_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 港股主板实时行情数据-东财
- 描述: 港股主板的实时行情数据; 该数据有 15 分钟延时
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#hk_mainboard
- 限量: 单次返回港股主板的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 港股主板实时行情数据-东财

接口: stock_hk_main_board_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#hk_mainboard

描述: 港股主板的实时行情数据; 该数据有 15 分钟延时

限量: 单次返回港股主板的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 序号  | int64   | -        |
| 代码  | object  | -        |
| 名称  | object  | -        |
| 最新价 | float64 | 注意单位: 港元 |
| 涨跌额 | float64 | 注意单位: 港元 |
| 涨跌幅 | float64 | 注意单位: %  |
| 今开  | float64 | -        |
| 最高  | float64 | -        |
| 最低  | float64 | -        |
| 昨收  | float64 | -        |
| 成交量 | float64 | 注意单位: 股  |
| 成交额 | float64 | 注意单位: 港元 |

接口示例

```python
import akshare as ak

stock_hk_main_board_spot_em_df = ak.stock_hk_main_board_spot_em()
print(stock_hk_main_board_spot_em_df)
```

数据示例

```
        序号     代码            名称  ...      昨收          成交量          成交额
0        1  02048        易居企业控股  ...   0.385   25513200.0   15353803.0
1        2  02121          创新奇智  ...  14.920   16877100.0  317864528.0
2        3  03896           金山云  ...   4.300  109607960.0  558129600.0
3        4  01552  BHCC HOLDING  ...   0.098     555000.0      63190.0
4        5  00799           IGG  ...   3.080   42094549.0  155345439.0
    ...    ...           ...  ...     ...          ...          ...
2278  2279  02181        迈博药业-B  ...   0.740      16000.0       9060.0
2279  2280  00974         中国顺客隆  ...   0.670       3000.0       1580.0
2280  2281  01146        中国服饰控股  ...   0.194       6000.0        806.0
2281  2282  06928          万马控股  ...   2.410    1816000.0    3545800.0
2282  2283  01160        金石资本集团  ...   0.750    1600000.0     747500.0
```
