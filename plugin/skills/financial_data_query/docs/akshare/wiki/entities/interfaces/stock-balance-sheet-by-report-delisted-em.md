---
title: "stock_balance_sheet_by_report_delisted_em - 资产负债表-按报告期"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_balance_sheet_by_report_delisted_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财-已退市股票 > 资产负债表-按报告期
- 描述: 东方财富-股票-财务分析-资产负债表-已退市股票-按报告期
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ000013#/cwfx/zcfzb
- 限量: 单次获取指定 symbol 的资产负债表-按报告期数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 资产负债表-按报告期

接口: stock_balance_sheet_by_report_delisted_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ000013#/cwfx/zcfzb

描述: 东方财富-股票-财务分析-资产负债表-已退市股票-按报告期

限量: 单次获取指定 symbol 的资产负债表-按报告期数据

输入参数

| 名称     | 类型  | 描述                               |
|--------|-----|----------------------------------|
| symbol | str | symbol="SZ000013"; 带市场标识的已退市股票代码 |

输出参数

| 名称  | 类型  | 描述         |
|-----|-----|------------|
| -   | -   | 319项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_balance_sheet_by_report_delisted_em_df = ak.stock_balance_sheet_by_report_delisted_em(symbol="SZ000013")
print(stock_balance_sheet_by_report_delisted_em_df)
```

数据示例

```
     SECUCODE SECURITY_CODE  ... OSOPINION_TYPE LISTING_STATE
0   000013.SZ        000013  ...           None             2
1   000013.SZ        000013  ...           None             2
2   000013.SZ        000013  ...           None             2
3   000013.SZ        000013  ...           None             2
4   000013.SZ        000013  ...           None             2
5   000013.SZ        000013  ...           None             2
6   000013.SZ        000013  ...           None             2
7   000013.SZ        000013  ...           None             2
8   000013.SZ        000013  ...           None             2
9   000013.SZ        000013  ...           None             2
10  000013.SZ        000013  ...           None             2
11  000013.SZ        000013  ...           None             2
12  000013.SZ        000013  ...           None             2
13  000013.SZ        000013  ...           None             2
14  000013.SZ        000013  ...           None             2
15  000013.SZ        000013  ...           None             2
16  000013.SZ        000013  ...           None             2
17  000013.SZ        000013  ...           None             2
18  000013.SZ        000013  ...           None             2
19  000013.SZ        000013  ...           None             2
20  000013.SZ        000013  ...           None             2
21  000013.SZ        000013  ...           None             2
22  000013.SZ        000013  ...           None             2
23  000013.SZ        000013  ...           None             2
24  000013.SZ        000013  ...           None             2
25  000013.SZ        000013  ...           None             2
26  000013.SZ        000013  ...           None             2
27  000013.SZ        000013  ...           None             2
28  000013.SZ        000013  ...           None             2
29  000013.SZ        000013  ...           None             2
30  000013.SZ        000013  ...           None             2
31  000013.SZ        000013  ...           None             2
32  000013.SZ        000013  ...           None             2
33  000013.SZ        000013  ...           None             2
34  000013.SZ        000013  ...           None             2
35  000013.SZ        000013  ...           None             2
36  000013.SZ        000013  ...           None             2
37  000013.SZ        000013  ...           None             2
[38 rows x 319 columns]
```
