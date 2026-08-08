---
title: "fund_financial_fund_daily_em - 理财型基金-实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_financial_fund_daily_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 理财型基金-实时数据
- 描述: 东方财富网-天天基金网-基金数据-理财型基金-实时数据, 此接口数据每个交易日 **16:00～23:00** 更新
- 目标地址: http://fund.eastmoney.com/lcjj.html#1_1__0__ljjz,desc_1_os1
- 限量: 该接口由于目标网站未更新数据，暂时不能返回数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 理财型基金-实时数据

接口: fund_financial_fund_daily_em

目标地址: http://fund.eastmoney.com/lcjj.html#1_1__0__ljjz,desc_1_os1

描述: 东方财富网-天天基金网-基金数据-理财型基金-实时数据, 此接口数据每个交易日 **16:00～23:00** 更新

限量: 该接口由于目标网站未更新数据，暂时不能返回数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称          | 类型    | 描述  |
|-------------|-------|-----|
| 序号          | int   | -   |
| 基金代码        | str   | -   |
| 基金简称        | str   | -   |
| 上一期年化收益率    | float | -   |
| 当前交易日-万份收益  | float | -   |
| 当前交易日-7日年华  | float | -   |
| 前一个交易日-万份收益 | float | -   |
| 前一个交易日-7日年华 | float | -   |
| 封闭期         | float | -   |
| 申购状态        | str   | -   |

接口示例

```python
import akshare as ak

fund_financial_fund_daily_em_df = ak.fund_financial_fund_daily_em()
print(fund_financial_fund_daily_em_df)
```

数据示例

```
   序号 基金代码   基金简称  上一期年化收益率  ... 前一个交易日-万份收益 前一个交易日-7日年华  封闭期 申购状态
0   1  000134     信诚理财28日盈A   2.1010  ...      0.4548      1.8150  28天  限大额
1   2  090021      大成月添利债券A   4.7470  ...      0.5243      1.8540  1个月  限大额
2   3  110051   易方达月月利理财债券B   2.4040  ...      0.6606      2.2450  1个月  限大额
3   4  070035    嘉实理财宝7天债券A   1.8310  ...      0.4871      1.8310   7天  限大额
4   5  660016     农银7天理财债券A   1.6780  ...      0.4567      1.6780   7天  限大额
5   6  000791   银华双月定期理财债券A           ...      0.6134      2.2390  2个月  限大额
6   7  001057    华夏理财30天债券A   3.0650  ...      0.6477      2.2020  1个月  限大额
7   8  110050   易方达月月利理财债券A   2.1140  ...      0.5813      1.9560  1个月  限大额
8   9  090023  大成月月盈短期理财债券A  22.2030  ...      0.4640      1.7510  1个月  限大额
9  10  000322    农银14天理财债券A           ...      0.4592      1.6080  14天  限大额
```
