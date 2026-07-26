---
title: "crypto_bitcoin_cme - CME-成交量报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, crypto, parameters, returns, example]
sources: [raw/data-dictionary/dc/dc.md]
confidence: high
---
# crypto_bitcoin_cme

- 分类: [[dc-dc|AKShare 加密货币数据]]
- 主题路径: AKShare 加密货币数据 > CME-成交量报告
- 描述: 芝加哥商业交易所-比特币成交量报告
- 目标地址: https://datacenter.jin10.com/reportType/dc_cme_btc_report
- 限量: 单次返回指定交易日的比特币成交量报告数据
- 来源页面: https://akshare.akfamily.xyz/data/dc/dc.html

## 相关

- [[dc-dc|AKShare 加密货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### CME-成交量报告

接口: crypto_bitcoin_cme

目标地址: https://datacenter.jin10.com/reportType/dc_cme_btc_report

描述: 芝加哥商业交易所-比特币成交量报告

限量: 单次返回指定交易日的比特币成交量报告数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20230830" |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| 商品     | object  | -  |
| 类型     | object  | -  |
| 电子交易合约 | int64   | -  |
| 场内成交合约 | float64 | -  |
| 场外成交合约 | int64   | -  |
| 成交量    | int64   | -  |
| 未平仓合约  | int64   | -  |
| 持仓变化   | int64   | -  |

接口示例

```python
import akshare as ak

crypto_bitcoin_cme_df = ak.crypto_bitcoin_cme(date="20230830")
print(crypto_bitcoin_cme_df)
```

数据示例

```
      商品  类型  电子交易合约  场内成交合约  场外成交合约   成交量  未平仓合约  持仓变化
0    比特币  期货    7895     NaN     366  8261  15364  -808
1    比特币  看涨      38     NaN       0    38   3260    11
2    比特币  期权     113     NaN       0   113   5871   -27
3    比特币  看跌      75     NaN       0    75   2611   -38
4  微型比特币  期货    7818     NaN       0  7818   8353  -425
```
