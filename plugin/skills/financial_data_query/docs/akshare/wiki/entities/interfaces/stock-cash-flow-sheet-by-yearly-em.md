---
title: "stock_cash_flow_sheet_by_yearly_em - 现金流量表-按年度"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cash_flow_sheet_by_yearly_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-东财 > 现金流量表-按年度
- 描述: 东方财富-股票-财务分析-现金流量表-按年度
- 目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
- 限量: 单次获取指定 symbol 的现金流量表-按年度数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 现金流量表-按年度

接口: stock_cash_flow_sheet_by_yearly_em

目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0

描述: 东方财富-股票-财务分析-现金流量表-按年度

限量: 单次获取指定 symbol 的现金流量表-按年度数据

输入参数

| 名称     | 类型  | 描述                      |
|--------|-----|-------------------------|
| symbol | str | symbol="SH600519"; 股票代码 |

输出参数

| 名称  | 类型  | 描述          |
|-----|-----|-------------|
| -   | -   | 314 项，不逐一列出 |

接口示例

```python
import akshare as ak

stock_cash_flow_sheet_by_yearly_em_df = ak.stock_cash_flow_sheet_by_yearly_em(symbol="SH600519")
print(stock_cash_flow_sheet_by_yearly_em_df)
```

数据示例

```
    SECUCODE SECURITY_CODE  ... FBCCE_ADD_YOY CREDIT_IMPAIRMENT_INCOME_YOY
0   601398.SH        601398  ...    238.302033                         None
1   601398.SH        601398  ...   -204.008112                         None
2   601398.SH        601398  ...    676.398241                         None
3   601398.SH        601398  ...   -446.960304                         None
4   601398.SH        601398  ...   -103.265330                         None
5   601398.SH        601398  ...    231.370619                         None
6   601398.SH        601398  ...   -156.355892                         None
7   601398.SH        601398  ...   1112.723130                         None
8   601398.SH        601398  ...    115.092223                         None
9   601398.SH        601398  ...   -169.124835                         None
10  601398.SH        601398  ...     10.647686                         None
11  601398.SH        601398  ...    167.055537                         None
12  601398.SH        601398  ...    160.423857                         None
13  601398.SH        601398  ...           NaN                         None
14  601398.SH        601398  ...           NaN                         None
15  601398.SH        601398  ...           NaN                         None
16  601398.SH        601398  ...           NaN                         None
17  601398.SH        601398  ...           NaN                         None
18  601398.SH        601398  ...           NaN                         None
19  601398.SH        601398  ...           NaN                         None
[20 rows x 314 columns]
```
