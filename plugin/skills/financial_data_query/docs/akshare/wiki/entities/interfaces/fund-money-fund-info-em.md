---
title: "fund_money_fund_info_em - 货币型基金-历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_money_fund_info_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 货币型基金-历史数据
- 描述: 东方财富网-天天基金网-基金数据-货币型基金-历史净值
- 目标地址: https://fundf10.eastmoney.com/jjjz_000009.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 货币型基金-历史数据

接口: fund_money_fund_info_em

目标地址: https://fundf10.eastmoney.com/jjjz_000009.html

描述: 东方财富网-天天基金网-基金数据-货币型基金-历史净值

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                   |
|--------|-----|----------------------------------------------------------------------|
| symbol | str | symbol="000009"; 需要基金代码, 可以通过调用 **ak.fund_money_fund_daily_em()** 获取 |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 净值日期    | object  | -  |
| 每万份收益   | float64 | -  |
| 7日年化收益率 | float64 | -  |
| 申购状态    | object  | -  |
| 赎回状态    | object  | -  |

接口示例

```python
import akshare as ak

fund_money_fund_info_em_df = ak.fund_money_fund_info_em(symbol="000009")
print(fund_money_fund_info_em_df)
```

数据示例

```
      净值日期    每万份收益  7日年化收益率  申购状态  赎回状态
0     2013-03-25  21.2775    3.485   封闭期   封闭期
1     2013-03-26   0.9561    3.482  开放申购  开放赎回
2     2013-03-27   0.3729    3.175  开放申购  开放赎回
3     2013-03-28   0.7068    3.042  开放申购  开放赎回
4     2013-03-29   0.6744    2.892  开放申购  开放赎回
...          ...      ...      ...   ...   ...
4187  2025-02-27   0.3724    1.371  暂停申购  开放赎回
4188  2025-02-28   0.3789    1.374  暂停申购  开放赎回
4189  2025-03-01   0.3790    1.377  暂停申购  开放赎回
4190  2025-03-02   0.3790    1.381  暂停申购  开放赎回
4191  2025-03-03   0.4081    1.408  暂停申购  开放赎回
[4192 rows x 5 columns]
```
