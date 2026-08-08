---
title: "futures_hq_subscribe_exchange_symbol - 外盘-品种代码表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_hq_subscribe_exchange_symbol

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 外盘-品种代码表
- 描述: 新浪财经-外盘商品期货品种代码表数据
- 目标地址: https://finance.sina.com.cn/money/future/hf.html
- 限量: 单次返回当前交易日的订阅的所有期货品种的品种代码表数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 外盘-品种代码表

接口: futures_hq_subscribe_exchange_symbol

目标地址: https://finance.sina.com.cn/money/future/hf.html

描述: 新浪财经-外盘商品期货品种代码表数据

限量: 单次返回当前交易日的订阅的所有期货品种的品种代码表数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型     | 描述  |
|--------|--------|-----|
| symbol | object | -   |
| code   | object | -   |

接口示例

```python
import akshare as ak

futures_hq_subscribe_exchange_symbol_df = ak.futures_hq_subscribe_exchange_symbol()
print(futures_hq_subscribe_exchange_symbol_df)
```

数据示例

```
      symbol  code
0   NYBOT-棉花    CT
1    LME镍3个月   NID
2    LME铅3个月   PBD
3    LME锡3个月   SND
4    LME锌3个月   ZSD
5    LME铝3个月   AHD
6    LME铜3个月   CAD
7    CBOT-黄豆     S
8    CBOT-小麦     W
9    CBOT-玉米     C
10  CBOT-黄豆油    BO
11  CBOT-黄豆粉    SM
12      日本橡胶   TRB
13    COMEX铜    HG
14  NYMEX天然气    NG
15   NYMEX原油    CL
16   COMEX白银    SI
17   COMEX黄金    GC
18   CME-瘦肉猪   LHC
19     布伦特原油   OIL
20       伦敦金   XAU
21       伦敦银   XAG
22      伦敦铂金   XPT
23      伦敦钯金   XPD
24       马棕油  FCPO
25     欧洲碳排放   EUA
```
