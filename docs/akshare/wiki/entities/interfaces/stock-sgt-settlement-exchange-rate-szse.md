---
title: "stock_sgt_settlement_exchange_rate_szse - 结算汇率-深港通"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sgt_settlement_exchange_rate_szse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 沪深港通持股 > 结算汇率-深港通
- 描述: 深港通-港股通业务信息-结算汇率
- 目标地址: https://www.szse.cn/szhk/hkbussiness/exchangerate/index.html
- 限量: 单次获取所有深港通结算汇率数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 结算汇率-深港通

接口: stock_sgt_settlement_exchange_rate_szse

目标地址: https://www.szse.cn/szhk/hkbussiness/exchangerate/index.html

描述: 深港通-港股通业务信息-结算汇率

限量: 单次获取所有深港通结算汇率数据

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

stock_sgt_settlement_exchange_rate_szse_df = ak.stock_sgt_settlement_exchange_rate_szse()
print(stock_sgt_settlement_exchange_rate_szse_df)
```

数据示例

```
     适用日期  买入结算汇兑比率  卖出结算汇兑比率 货币种类
0     2016-12-05   0.88621   0.88679  HKD
1     2016-12-06   0.88698   0.88682  HKD
2     2016-12-07   0.88525   0.88935  HKD
3     2016-12-08   0.89041   0.88899  HKD
4     2016-12-09   0.88567   0.89133  HKD
          ...       ...       ...  ...
1371  2022-09-23   0.90209   0.90311  HKD
1372  2022-09-26   0.90826   0.90814  HKD
1373  2022-09-27   0.91179   0.91181  HKD
1374  2022-09-28   0.91024   0.91636  HKD
1375  2022-09-29   0.93270   0.91810  HKD
```
