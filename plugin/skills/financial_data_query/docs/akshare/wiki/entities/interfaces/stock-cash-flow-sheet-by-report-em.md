---
title: "stock_cash_flow_sheet_by_report_em - 现金流量表-按报告期"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cash_flow_sheet_by_report_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财 > 现金流量表-按报告期
- 描述: 东方财富-股票-财务分析-现金流量表-按报告期
- 目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
- 限量: 单次获取指定 symbol 的现金流量表-按报告期数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 现金流量表-按报告期

接口: stock_cash_flow_sheet_by_report_em

目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0

描述: 东方财富-股票-财务分析-现金流量表-按报告期

限量: 单次获取指定 symbol 的现金流量表-按报告期数据

输入参数

| 名称     | 类型  | 描述                      |
|--------|-----|-------------------------|
| symbol | str | symbol="SH600519"; 股票代码 |

输出参数

| 名称  | 类型  | 描述          |
|-----|-----|-------------|
| -   | -   | 252 项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_cash_flow_sheet_by_report_em_df = ak.stock_cash_flow_sheet_by_report_em(symbol="SH600519")
print(stock_cash_flow_sheet_by_report_em_df)
```

数据示例

```
    SECUCODE SECURITY_CODE  ... MINORITY_INTEREST MINORITY_INTEREST_YOY
0   600519.SH        600519  ...               NaN                   NaN
1   600519.SH        600519  ...               NaN                   NaN
2   600519.SH        600519  ...               NaN                   NaN
3   600519.SH        600519  ...               NaN                   NaN
4   600519.SH        600519  ...               NaN                   NaN
..        ...           ...  ...               ...                   ...
83  600519.SH        600519  ...               NaN                   NaN
84  600519.SH        600519  ...               NaN                   NaN
85  600519.SH        600519  ...               NaN                   NaN
86  600519.SH        600519  ...               NaN                   NaN
87  600519.SH        600519  ...               NaN                   NaN
[88 rows x 252 columns]
```
