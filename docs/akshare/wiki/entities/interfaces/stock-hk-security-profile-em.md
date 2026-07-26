---
title: "stock_hk_security_profile_em - 证券资料"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_security_profile_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 证券资料
- 描述: 东方财富-港股-证券资料
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 证券资料

接口: stock_hk_security_profile_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile

描述: 东方财富-港股-证券资料

限量: 单次返回全部数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="03900" |

输出参数

| 名称             | 类型      | 描述 |
|----------------|---------|----|
| 证券代码           | object  | -  |
| 证券简称           | object  | -  |
| 上市日期           | object  | -  |
| 证券类型           | object  | -  |
| 发行价            | float64 | -  |
| 发行量(股)         | int64   | -  |
| 每手股数           | int64   | -  |
| 每股面值           | object  | -  |
| 交易所            | object  | -  |
| 板块             | object  | -  |
| 年结日            | object  | -  |
| ISIN（国际证券识别编码） | object  | -  |
| 是否沪港通标的        | object  | -  |

接口示例

```python
import akshare as ak

stock_hk_security_profile_em_df = ak.stock_hk_security_profile_em(symbol="03900")
print(stock_hk_security_profile_em_df)
```

数据示例

```
       证券代码  证券简称                 上市日期  ... ISIN（国际证券识别编码）  是否沪港通标的  是否深港通标的
0  03900.HK  绿城中国  2006-07-13 00:00:00  ...   KYG4100M1050        是        是
[1 rows x 14 columns]
```
