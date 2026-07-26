---
title: "fund_financial_fund_info_em - 理财型基金-历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_financial_fund_info_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 理财型基金-历史数据
- 描述: 东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细
- 目标地址: http://fundf10.eastmoney.com/jjjz_000791.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 理财型基金-历史数据

接口: fund_financial_fund_info_em

目标地址: http://fundf10.eastmoney.com/jjjz_000791.html

描述: 东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                     |
|--------|-----|------------------------------------------------------------------------|
| symbol | str | symbol="000134"; 基金代码, 可以通过调用 **ak.fund_financial_fund_daily_em()** 获取 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 净值日期 | object  | -       |
| 单位净值 | float64 | -       |
| 累计净值 | float64 | -       |
| 日增长率 | float64 | -       |
| 申购状态 | object  | -       |
| 赎回状态 | object  | -       |
| 分红送配 | object  | 注意单位: % |

接口示例

```python
import akshare as ak

fund_financial_fund_info_em_df = ak.fund_financial_fund_info_em(symbol="000134")
print(fund_financial_fund_info_em_df)
```

数据示例

```
     净值日期    单位净值    累计净值  日增长率    申购状态  赎回状态 分红送配
0    2020-06-23  0.9982  0.9982   NaN    暂停申购  开放赎回
1    2020-06-24  0.9987  0.9987  0.05    暂停申购  开放赎回
2    2020-06-29  0.9994  0.9994  0.07    暂停申购  开放赎回
3    2020-06-30  0.9995  0.9995  0.01    暂停申购  开放赎回
4    2020-07-01  0.9998  0.9998  0.03    暂停申购  开放赎回
..          ...     ...     ...   ...     ...   ...  ...
663  2023-03-16  1.0291  1.0951  0.02  限制大额申购  开放赎回
664  2023-03-17  1.0294  1.0954  0.03  限制大额申购  开放赎回
665  2023-03-20  1.0302  1.0962  0.08  限制大额申购  开放赎回
666  2023-03-21  1.0303  1.0963  0.01  限制大额申购  开放赎回
667  2023-03-22  1.0303  1.0963  0.00  限制大额申购  开放赎回
```
