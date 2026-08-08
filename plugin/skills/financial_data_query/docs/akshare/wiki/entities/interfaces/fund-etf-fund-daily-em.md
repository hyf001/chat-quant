---
title: "fund_etf_fund_daily_em - 场内交易基金-实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_fund_daily_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 场内交易基金-实时数据
- 描述: 东方财富网站-天天基金网-基金数据-场内交易基金-实时数据, 此接口数据每个交易日 **16:00～23:00**
- 目标地址: http://fund.eastmoney.com/cnjy_dwjz.html
- 限量: 单次返回当前时刻所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 场内交易基金-实时数据

接口: fund_etf_fund_daily_em

目标地址: http://fund.eastmoney.com/cnjy_dwjz.html

描述: 东方财富网站-天天基金网-基金数据-场内交易基金-实时数据, 此接口数据每个交易日 **16:00～23:00**

限量: 单次返回当前时刻所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称          | 类型      | 描述            |
|-------------|---------|---------------|
| 基金代码        | object  | -             |
| 基金简称        | object  | -             |
| 类型          | float64 | -             |
| 当前交易日-单位净值  | float64 | 会返回具体的日期值作为字段 |
| 当前交易日-累计净值  | float64 | 会返回具体的日期值作为字段 |
| 前一个交易日-单位净值 | float64 | 会返回具体的日期值作为字段 |
| 前一个交易日-累计净值 | float64 | 会返回具体的日期值作为字段 |
| 增长值         | float64 | -             |
| 增长率         | object  | -             |
| 市价          | object  | -             |
| 折价率         | object  | -             |

接口示例

```python
import akshare as ak

fund_etf_fund_daily_em_df = ak.fund_etf_fund_daily_em()
print(fund_etf_fund_daily_em_df)
```

数据示例

```
       基金代码             基金简称      类型  ...     增长率      市价     折价率
0    159909   招商深证TMT50ETF行情  ETF-场内  ...   0.12%  7.0200   0.14%
1    159991     招商创业板大盘ETF行情  ETF-场内  ...   0.64%  1.4840   0.02%
2    150270    招商中证白酒指数分级B行情    分级杠杆  ...   2.61%  1.4650  -1.16%
3    150262    华宝中证医疗指数分级B行情    分级杠杆  ...   0.81%  1.3930   2.64%
4    150250    招商中证银行指数分级B行情    分级杠杆  ...  -1.06%  1.3380  -0.62%
..      ...              ...     ...  ...     ...     ...     ...
474  510860      兴业上证50ETF行情  ETF-场内  ...     ---     ---     ---
475  150175    银华恒生国企指数分级A行情    固定收益  ...     ---     ---     ---
476  150205    鹏华中证国防指数分级A行情    固定收益  ...     ---     ---     ---
477  150321    富国中证煤炭指数分级A行情    固定收益  ...     ---     ---     ---
478  515790  华泰柏瑞中证光伏产业ETF行情  ETF-场内  ...     ---     ---     ---
```
