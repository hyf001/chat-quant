---
title: "crypto_js_spot - 实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, crypto, parameters, returns, example]
sources: [raw/data-dictionary/dc/dc.md]
confidence: high
---
# crypto_js_spot

- 分类: [[dc-dc|AKShare 加密货币数据]]
- 主题路径: AKShare 加密货币数据 > 实时数据
- 描述: 加密货币实时行情
- 目标地址: https://datacenter.jin10.com/reportType/dc_bitcoin_current
- 限量: 单次返回主流加密货币当前时点行情数据
- 来源页面: https://akshare.akfamily.xyz/data/dc/dc.html

## 相关

- [[dc-dc|AKShare 加密货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### 实时数据

接口: crypto_js_spot

目标地址: https://datacenter.jin10.com/reportType/dc_bitcoin_current

描述: 加密货币实时行情

限量: 单次返回主流加密货币当前时点行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述     |
|---------|---------|--------|
| 市场      | object  | -      |
| 交易品种    | object  | -      |
| 最近报价    | float64 | -      |
| 涨跌额     | float64 | -      |
| 涨跌幅     | float64 | -      |
| 24小时最高  | float64 | -      |
| 24小时最低  | float64 | 注意货币币种 |
| 24小时成交量 | float64 | 注意货币币种 |
| 更新时间    | float64 | -      |

接口示例

```python
import akshare as ak

crypto_js_spot_df = ak.crypto_js_spot()
print(crypto_js_spot_df)
```

数据示例

```
               市场    交易品种  ...   24小时成交量        更新时间
0    Bitfinex(香港)  LTCUSD  ...  23157.88  2022-03-15 16:02:03
1    Bitflyer(日本)  BTCJPY  ...   2031.26  2022-03-15 16:02:03
2    Bitstamp(美国)  BTCUSD  ...   1380.17  2022-03-15 16:02:03
3      CEX.IO(伦敦)  BTCUSD  ...     54.51  2022-03-15 16:02:03
4  Kraken_EUR(美国)  BTCEUR  ...   1342.40  2022-03-15 16:02:03
5      Kraken(美国)  LTCUSD  ...  21871.79  2022-03-15 16:02:03
6      OKCoin(中国)  BTCUSD  ...    239.14  2022-03-15 16:02:03
7    Bitfinex(香港)  BCHUSD  ...      0.00  2020-11-16 21:02:04
8    Bitfinex(香港)  BTCUSD  ...   7496.55  2022-03-15 16:02:03
9      Kraken(美国)  BTCUSD  ...   3147.43  2022-03-15 16:02:03
```
