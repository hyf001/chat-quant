---
title: "futures_hold_pos_sina - 成交持仓"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_hold_pos_sina

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 成交持仓
- 描述: 新浪财经-期货-成交持仓
- 目标地址: https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php
- 限量: 单次返回指定合约的成交持仓数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 成交持仓

接口: futures_hold_pos_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php

描述: 新浪财经-期货-成交持仓

限量: 单次返回指定合约的成交持仓数据

输入参数

| 名称       | 类型  | 描述                                              |
|----------|-----|-------------------------------------------------|
| symbol   | str | symbol="成交量"; choice of {"成交量", "多单持仓", "空单持仓"} |
| contract | str | contract="OI2501"; 只限于商品期货                      |
| date     | str | date="20240223"                                 |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 名次     | int64  | -  |
| 会员简称   | object | -  |
| 成交量    | int64  | -  |
| 比上交易增减 | int64  | -  |

接口示例

```python
import akshare as ak

futures_hold_pos_sina_df = ak.futures_hold_pos_sina(symbol="成交量", contract="OI2501", date="20241016")
print(futures_hold_pos_sina_df)
```

数据示例

```
    名次    会员简称    成交量   比上交易增减
0    1    中信期货（代客）  78197 -15458.0
1    2    东证期货（代客）  67129  -6540.0
2    3    国泰君安（代客）  53632 -12474.0
3    4    银河期货（代客）  21916 -10902.0
4    5    华闻期货（代客）  21807  -4777.0
5    6    徽商期货（代客）  21615  -7861.0
6    7    海通期货（代客）  18847  -4165.0
7    8    中信建投（代客）  15285  -2470.0
8    9    华泰期货（代客）  14610  -3036.0
9   10    南华期货（代客）  11990   -554.0
10  11    华西期货（代客）  11324   -795.0
11  12    方正中期（代客）  10958  -4512.0
12  13    瑞达期货（代客）   9038  -2121.0
13  14    国金期货（代客）   9026   3334.0
14  15    广发期货（代客）   8775  -5333.0
15  16    中辉期货（代客）   7746  -4127.0
16  17  国投安信期货（代客）   7739   1295.0
17  18    安粮期货（代客）   7671  -1946.0
18  19    东吴期货（代客）   7639  -4308.0
19  20    东方财富（代客）   7220  -1248.0
```
