---
title: "fund_etf_fund_info_em - 场内交易基金-历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_fund_info_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 场内交易基金-历史数据
- 描述: 东方财富网站-天天基金网-基金数据-场内交易基金-历史净值数据
- 目标地址: http://fundf10.eastmoney.com/jjjz_004186.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 场内交易基金-历史数据

接口: fund_etf_fund_info_em

目标地址: http://fundf10.eastmoney.com/jjjz_004186.html

描述: 东方财富网站-天天基金网-基金数据-场内交易基金-历史净值数据

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称         | 类型  | 描述                                                             |
|------------|-----|----------------------------------------------------------------|
| fund       | str | fund="511280"; 基金代码, 可以通过调用 **ak.fund_etf_fund_daily_em()** 获取 |
| start_date | str | start_date="20000101"; 开始时间                                    |
| end_date   | str | end_date="20500101"; 结束时间                                      |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 净值日期 | object  | -       |
| 单位净值 | float64 | -       |
| 累计净值 | float64 | -       |
| 日增长率 | float64 | 注意单位: % |
| 申购状态 | object  | -       |
| 赎回状态 | object  | -       |

接口示例

```python
import akshare as ak

fund_etf_fund_info_em_df = ak.fund_etf_fund_info_em(fund="511280", start_date="20000101", end_date="20500101")
print(fund_etf_fund_info_em_df)
```

数据示例

```
     净值日期      单位净值    累计净值  日增长率  申购状态  赎回状态
0    2018-05-03    1.0000  1.0000   NaN   封闭期   封闭期
1    2018-05-04    1.0003  1.0003  0.03   封闭期   封闭期
2    2018-05-11    1.0006  1.0006   NaN   封闭期   封闭期
3    2018-05-14  100.0804  1.0008  0.02   封闭期   封闭期
4    2018-05-18  100.1054  1.0011   NaN   封闭期   封闭期
..          ...       ...     ...   ...   ...   ...
779  2021-07-28  110.8370  1.1084 -0.02  场内买入  场内卖出
780  2021-07-29  110.8154  1.1082 -0.02  场内买入  场内卖出
781  2021-07-30  110.7640  1.1076 -0.05  场内买入  场内卖出
782  2021-08-02  110.6097  1.1061 -0.14  场内买入  场内卖出
783  2021-08-03  113.8015  1.1380  2.89  暂停申购  暂停赎回
[784 rows x 6 columns]
```
