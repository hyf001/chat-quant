---
title: "stock_cash_flow_sheet_by_quarterly_em - 现金流量表-按单季度"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cash_flow_sheet_by_quarterly_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财 > 现金流量表-按单季度
- 描述: 东方财富-股票-财务分析-现金流量表-按单季度
- 目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
- 限量: 单次获取指定 symbol 的现金流量表-按单季度数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 现金流量表-按单季度

接口: stock_cash_flow_sheet_by_quarterly_em

目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0

描述: 东方财富-股票-财务分析-现金流量表-按单季度

限量: 单次获取指定 symbol 的现金流量表-按单季度数据

输入参数

| 名称     | 类型  | 描述                      |
|--------|-----|-------------------------|
| symbol | str | symbol="SH600519"; 股票代码 |

输出参数

| 名称  | 类型  | 描述          |
|-----|-----|-------------|
| -   | -   | 315 项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_cash_flow_sheet_by_quarterly_em_df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol="SH600519")
print(stock_cash_flow_sheet_by_quarterly_em_df)
```

数据示例

```
    SECUCODE SECURITY_CODE  ... OPINION_TYPE OSOPINION_TYPE
0   601398.SH        601398  ...         None           None
1   601398.SH        601398  ...         None           None
2   601398.SH        601398  ...      标准无保留意见           None
3   601398.SH        601398  ...         None           None
4   601398.SH        601398  ...         None           None
..        ...           ...  ...          ...            ...
61  601398.SH        601398  ...         None           None
62  601398.SH        601398  ...      标准无保留意见           None
63  601398.SH        601398  ...         None           None
64  601398.SH        601398  ...         None           None
65  601398.SH        601398  ...         None           None
[66 rows x 315 columns]
```
