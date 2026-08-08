---
title: "stock_sgt_settlement_exchange_rate_sse - 结算汇率-沪港通"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sgt_settlement_exchange_rate_sse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 沪深港通持股 > 结算汇率-沪港通
- 描述: 沪港通-港股通信息披露-结算汇兑
- 目标地址: http://www.sse.com.cn/services/hkexsc/disclo/ratios
- 限量: 单次获取所有沪港通结算汇率数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 结算汇率-沪港通

接口: stock_sgt_settlement_exchange_rate_sse

目标地址: http://www.sse.com.cn/services/hkexsc/disclo/ratios

描述: 沪港通-港股通信息披露-结算汇兑

限量: 单次获取所有沪港通结算汇率数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述  |
|----------|---------|-----|
| 适用日期     | object  | -   |
| 买入结算汇兑比率 | float64 | -   |
| 卖出结算汇兑比率 | float64 | -   |
| 货币种类     | object  | -   |

接口示例

```python
import akshare as ak

stock_sgt_settlement_exchange_rate_sse_df = ak.stock_sgt_settlement_exchange_rate_sse()
print(stock_sgt_settlement_exchange_rate_sse_df)
```

数据示例

```
      适用日期  买入结算汇兑比率  卖出结算汇兑比率 货币种类
0     2014-11-17   0.79143   0.79017  HKD
1     2014-11-18   0.79068   0.78932  HKD
2     2014-11-19   0.78873   0.78927  HKD
3     2014-11-20   0.78980   0.78980  HKD
4     2014-11-21   0.79021   0.78999  HKD
          ...       ...       ...  ...
1860  2022-09-23   0.90170   0.90350  HKD
1861  2022-09-26   0.90812   0.90828  HKD
1862  2022-09-27   0.91177   0.91183  HKD
1863  2022-09-28   0.91038   0.91622  HKD
1864  2022-09-29   0.93260   0.91820  HKD
```
