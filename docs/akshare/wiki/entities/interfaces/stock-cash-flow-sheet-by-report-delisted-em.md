---
title: "stock_cash_flow_sheet_by_report_delisted_em - 现金流量表-按报告期"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cash_flow_sheet_by_report_delisted_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财-已退市股票 > 现金流量表-按报告期
- 描述: 东方财富-股票-财务分析-现金流量表-已退市股票-按报告期
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ000013#/cwfx/xjllb
- 限量: 单次获取指定 symbol 的现金流量表-按报告期数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 现金流量表-按报告期

接口: stock_cash_flow_sheet_by_report_delisted_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ000013#/cwfx/xjllb

描述: 东方财富-股票-财务分析-现金流量表-已退市股票-按报告期

限量: 单次获取指定 symbol 的现金流量表-按报告期数据

输入参数

| 名称     | 类型  | 描述                               |
|--------|-----|----------------------------------|
| symbol | str | symbol="SZ000013"; 带市场标识的已退市股票代码 |

输出参数

| 名称  | 类型  | 描述          |
|-----|-----|-------------|
| -   | -   | 252 项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_cash_flow_sheet_by_report_delisted_em_df = ak.stock_cash_flow_sheet_by_report_delisted_em(symbol="SZ000013")
print(stock_cash_flow_sheet_by_report_delisted_em_df)
```

数据示例

```
     SECUCODE SECURITY_CODE  ... MINORITY_INTEREST MINORITY_INTEREST_YOY
0   000013.SZ        000013  ...       18337254.13                   NaN
1   000013.SZ        000013  ...       14847516.38            -19.030863
2   000013.SZ        000013  ...        9677540.34                   NaN
3   000013.SZ        000013  ...       23357763.71             57.317649
4   000013.SZ        000013  ...        9262252.60             -4.291253
5   000013.SZ        000013  ...       -3961320.04           -116.959329
6   000013.SZ        000013  ...       -1234838.91           -113.331950
7   000013.SZ        000013  ...      -35258015.13           -790.057223
8   000013.SZ        000013  ...        -179278.95                   NaN
9   000013.SZ        000013  ...       -4739838.45           -283.842654
10  000013.SZ        000013  ...      -28385113.99                   NaN
11  000013.SZ        000013  ...               NaN                   NaN
12  000013.SZ        000013  ...               NaN                   NaN
13  000013.SZ        000013  ...               NaN                   NaN
14  000013.SZ        000013  ...               NaN                   NaN
15  000013.SZ        000013  ...               NaN                   NaN
16  000013.SZ        000013  ...               NaN                   NaN
17  000013.SZ        000013  ...               NaN                   NaN
18  000013.SZ        000013  ...               NaN                   NaN
19  000013.SZ        000013  ...               NaN                   NaN
20  000013.SZ        000013  ...               NaN                   NaN
[21 rows x 252 columns]
```
