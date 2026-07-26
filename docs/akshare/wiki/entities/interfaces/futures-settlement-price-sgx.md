---
title: "futures_settlement_price_sgx - 新加坡交易所期货"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_settlement_price_sgx

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 新加坡交易所期货
- 描述: 新加坡交易所-衍生品-历史数据-历史结算价格; 数据于下个工作日新加坡时间下午 2 点起提供
- 目标地址: https://www.sgx.com/zh-hans/research-education/derivatives
- 限量: 单次获取指定交易日前一日的所有期货品种的结算价数据; 只能获取过去 60 个交易日内的数据; 由于国内网络限制, 请使用代理访问
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新加坡交易所期货

接口: futures_settlement_price_sgx

目标地址: https://www.sgx.com/zh-hans/research-education/derivatives

描述: 新加坡交易所-衍生品-历史数据-历史结算价格; 数据于下个工作日新加坡时间下午 2 点起提供

限量: 单次获取指定交易日前一日的所有期货品种的结算价数据; 只能获取过去 60 个交易日内的数据; 由于国内网络限制, 请使用代理访问

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20231107"; 交易日 |

输出参数

| 名称     | 类型      | 描述     |
|--------|---------|--------|
| DATE   | int64   | 日期     |
| COM    | object  | 品种代码   |
| COM_MM | int64   | 品种到期月份 |
| COM_YY | int64   | 品种年份   |
| OPEN   | float64 | 开盘价    |
| HIGH   | float64 | 最高价    |
| LOW    | float64 | 最低价    |
| CLOSE  | float64 | 收盘价    |
| SETTLE | float64 | 结算价    |
| VOLUME | int64   | 交易量    |
| OINT   | int64   | 未平仓合约  |
| SERIES | object  | 合约代码   |

接口示例

```python
import akshare as ak

futures_settlement_price_sgx_df = ak.futures_settlement_price_sgx(date="20231108")
print(futures_settlement_price_sgx_df)
```

数据示例

```
          DATE    COM  COM_MM  COM_YY  ...  SETTLE  VOLUME  OINT   SERIES
0     20231107  1MF        11    2023  ...  465.34       0     0   1MFX23
1     20231107  1MF        12    2023  ...  462.13       0     0   1MFZ23
2     20231107  1MF         1    2024  ...  457.05       0     0   1MFF24
3     20231107  1MF         2    2024  ...  453.97       0     0   1MFG24
4     20231107  1MF         3    2024  ...  452.39       0     0   1MFH24
        ...    ...     ...     ...  ...     ...     ...   ...      ...
3165  20231107  ZYES       12    2023  ...   16.95       0     0  ZYESZ23
3166  20231107  ZYES        1    2024  ...   17.05       0     0  ZYESF24
3167  20231107  ZZEE       11    2023  ...  263.45     584    90  ZZEEX23
3168  20231107  ZZEE       12    2023  ...  264.80       0     0  ZZEEZ23
3169  20231107  ZZEE        1    2024  ...  266.25       0     0  ZZEEF24
[3170 rows x 12 columns]
```
