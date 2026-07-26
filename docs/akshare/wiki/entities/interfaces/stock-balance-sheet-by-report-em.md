---
title: "stock_balance_sheet_by_report_em - 资产负债表-按报告期"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_balance_sheet_by_report_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财 > 资产负债表-按报告期
- 描述: 东方财富-股票-财务分析-资产负债表-按报告期
- 目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
- 限量: 单次获取指定 symbol 的资产负债表-按报告期数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 资产负债表-按报告期

接口: stock_balance_sheet_by_report_em

目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0

描述: 东方财富-股票-财务分析-资产负债表-按报告期

限量: 单次获取指定 symbol 的资产负债表-按报告期数据

输入参数

| 名称     | 类型  | 描述                      |
|--------|-----|-------------------------|
| symbol | str | symbol="SH600519"; 股票代码 |

输出参数

| 名称  | 类型  | 描述          |
|-----|-----|-------------|
| -   | -   | 319 项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol="SH600519")
print(stock_balance_sheet_by_report_em_df)
```

数据示例

```
     SECUCODE SECURITY_CODE  ... OSOPINION_TYPE LISTING_STATE
0   600519.SH        600519  ...           None             0
1   600519.SH        600519  ...           None             0
2   600519.SH        600519  ...           None             0
3   600519.SH        600519  ...           None             0
4   600519.SH        600519  ...           None             0
..        ...           ...  ...            ...           ...
87  600519.SH        600519  ...           None             0
88  600519.SH        600519  ...           None             0
89  600519.SH        600519  ...           None             0
90  600519.SH        600519  ...           None             0
91  600519.SH        600519  ...           None             0
[92 rows x 319 columns]
```
