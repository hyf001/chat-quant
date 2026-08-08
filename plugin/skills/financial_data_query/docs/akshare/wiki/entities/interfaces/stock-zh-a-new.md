---
title: "stock_zh_a_new - 次新股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_new

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 次新股
- 描述: 新浪财经-行情中心-沪深股市-次新股
- 目标地址: http://vip.stock.finance.sina.com.cn/mkt/#new_stock
- 限量: 单次返回所有次新股行情数据, 由于次新股名单随着交易日变化而变化，只能获取最近交易日的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 次新股

接口: stock_zh_a_new

目标地址: http://vip.stock.finance.sina.com.cn/mkt/#new_stock

描述: 新浪财经-行情中心-沪深股市-次新股

限量: 单次返回所有次新股行情数据, 由于次新股名单随着交易日变化而变化，只能获取最近交易日的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型      | 描述   |
|---------------|---------|------|
| symbol        | object  | 新浪代码 |
| code          | object  | 股票代码 |
| name          | object  | 股票简称 |
| open          | float64 | 开盘价  |
| high          | float64 | 最高价  |
| low           | float64 | 最低价  |
| volume        | int64   | 成交量  |
| amount        | int64   | 成交额  |
| mktcap        | float64 | 市值   |
| turnoverratio | float64 | 换手率  |

接口示例

```python
import akshare as ak

stock_zh_a_new_df = ak.stock_zh_a_new()
print(stock_zh_a_new_df)
```

数据示例

```
     symbol    code  name  ...      amount        mktcap  turnoverratio
0   sh601728  601728  中国电信  ...  2078538311  4.146314e+07        7.91425
1   sh601825  601825  沪农商行  ...   511698399  7.657689e+06        6.67390
2   sh601921  601921  浙版传媒  ...   218150606  2.284444e+06        9.66828
3   sh605028  605028  世茂能源  ...   248080378  3.996800e+05       24.98649
4   sh605056  605056  咸亨国际  ...    60691275  7.736193e+05        7.80149
..       ...     ...   ...  ...         ...           ...            ...
79  sz301052  301052  果麦文化  ...   231553223  2.541569e+05       38.94978
80  sz301053  301053  远信工业  ...   214016261  3.033018e+05       33.99790
81  sz301055  301055  C张小泉  ...   679460624  5.285280e+05       64.66610
82  sz301056  301056   C森赫  ...   423894365  3.694995e+05       48.84555
83  sz301058  301058  中粮工科  ...           0  0.000000e+00        0.00000
```
