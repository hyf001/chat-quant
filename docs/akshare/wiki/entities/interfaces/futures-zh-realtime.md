---
title: "futures_zh_realtime - 内盘-实时行情数据(品种)"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_zh_realtime

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-实时行情数据(品种)
- 描述: 新浪财经-期货实时行情数据
- 目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-实时行情数据(品种)

接口: futures_zh_realtime

目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1

描述: 新浪财经-期货实时行情数据

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                        |
|--------|-----|-----------------------------------------------------------|
| symbol | str | symbol="白糖", 品种名称；可以通过 ak.futures_symbol_mark() 获取所有品种命名表 |

输出参数

| 名称             | 类型      | 描述     |
|----------------|---------|--------|
| symbol         | object  | 合约代码   |
| exchange       | object  | 交易所    |
| name           | object  | 合约中文名称 |
| trade          | float64 | 最新价    |
| settlement     | float64 | 动态结算   |
| presettlement  | float64 | 昨日结算   |
| open           | float64 | 今开     |
| high           | float64 | 最高     |
| low            | float64 | 最低     |
| close          | float64 | 收盘     |
| bidprice1      | float64 | 买入     |
| askprice1      | float64 | 卖出     |
| bidvol1        | int64   | 买量     |
| askvol1        | int64   | 卖量     |
| volume         | int64   | 成交量    |
| position       | int64   | 持仓量    |
| ticktime       | object  | 时间     |
| tradedate      | object  | 日期     |
| preclose       | float64 | 前收盘价   |
| changepercent  | float64 | 涨跌幅    |
| bid            | float64 | -      |
| ask            | float64 | -      |
| prevsettlement | float64 | 前结算价   |

接口示例

```python
import akshare as ak

futures_zh_realtime_df = ak.futures_zh_realtime(symbol="白糖")
print(futures_zh_realtime_df)
```

数据示例

```
   symbol exchange    name   trade  ...  changepercent  bid  ask  prevsettlement
0     SR0     czce    白糖连续  6090.0  ...       0.004122  0.0  0.0          6065.0
1  SR2209     czce  白糖2209  6090.0  ...       0.004122  0.0  0.0          6065.0
2  SR2211     czce  白糖2211  6121.0  ...       0.004595  0.0  0.0          6093.0
3  SR2301     czce  白糖2301  6229.0  ...       0.003544  0.0  0.0          6207.0
4  SR2207     czce  白糖2207  6041.0  ...       0.003155  0.0  0.0          6022.0
5  SR2303     czce  白糖2303  6200.0  ...       0.000484  0.0  0.0          6197.0
6  SR2305     czce  白糖2305  6208.0  ...       0.000806  0.0  0.0          6203.0
```

接口示例-所有期货品种的所有合约（请注意数据获取频率）

```python
import akshare as ak
import pandas as pd

futures_symbol_mark_df = ak.futures_symbol_mark()

big_df = pd.DataFrame()
for item in futures_symbol_mark_df['symbol']:
    print(item)
    futures_zh_realtime_df = ak.futures_zh_realtime(symbol=item)
    big_df = pd.concat([big_df, futures_zh_realtime_df], ignore_index=True)

print(big_df)
```

数据示例-所有期货品种的所有合约

```
     symbol exchange           name  ...  bid  ask  prevsettlement
0       TA0     czce          PTA连续  ...  0.0  0.0         6744.00
1    TA2209     czce        PTA2209  ...  0.0  0.0         6744.00
2    TA2208     czce        PTA2208  ...  0.0  0.0         6816.00
3    TA2301     czce        PTA2301  ...  0.0  0.0         6424.00
4    TA2210     czce          PTA连续  ...  0.0  0.0         6654.00
..      ...      ...            ...  ...  ...  ...             ...
565  IC2207    cffex  中证500指数期货2207  ...  0.0  0.0         5904.20
566     TS0    cffex      2年期国债期货连续  ...  0.0  0.0          101.04
567  TS2209    cffex    2年期国债期货2209  ...  0.0  0.0          101.04
568  TS2206    cffex    2年期国债期货2206  ...  0.0  0.0          101.28
569  TS2212    cffex    2年期国债期货2212  ...  0.0  0.0          100.92
```
