---
title: "fund_money_fund_daily_em - 货币型基金-实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_money_fund_daily_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 货币型基金-实时数据
- 描述: 东方财富网-天天基金网-基金数据-货币型基金收益, 此接口数据每个交易日 **16:00～23:00**
- 目标地址: http://fund.eastmoney.com/HBJJ_pjsyl.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 货币型基金-实时数据

接口: fund_money_fund_daily_em

目标地址: http://fund.eastmoney.com/HBJJ_pjsyl.html

描述: 东方财富网-天天基金网-基金数据-货币型基金收益, 此接口数据每个交易日 **16:00～23:00**

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称          | 类型    | 描述  |
|-------------|-------|-----|
| 基金代码        | str   | -   |
| 基金简称        | str   | -   |
| 当前交易日-万份收益  | float | -   |
| 当前交易日-7日年化% | float | -   |
| 当前交易日-单位净值  | float | -   |
| 前一交易日-万份收益  | float | -   |
| 前一交易日-7日年化% | float | -   |
| 前一交易日-单位净值  | float | -   |
| 日涨幅         | str   | -   |
| 成立日期        | str   | -   |
| 基金经理        | str   | -   |
| 手续费         | str   | -   |
| 可购全部        | str   | -   |

接口示例

```python
import akshare as ak

fund_money_fund_daily_em_df = ak.fund_money_fund_daily_em()
print(fund_money_fund_daily_em_df)
```

数据示例

```
       基金代码        基金简称 当前交易日-万份收益 当前交易日-7日年化%  ...        成立日期  基金经理  手续费 可购全部
2    004186     江信增利货币B     0.4461     4.1720%  ...  2017-08-03    杨淳  0费率   购买
3    002884  华润元大现金通货币B     0.8919     3.9870%  ...  2016-07-27  李仆 等  0费率   购买
4    004185     江信增利货币A     0.4065     3.9620%  ...  2017-08-03    杨淳  0费率   购买
5    002883  华润元大现金通货币A     0.8585     3.8460%  ...  2016-07-27  李仆 等  0费率   购买
6    740602       长安货币B     0.4641     3.7260%  ...  2013-01-25    孟楠  0费率   购买
..      ...         ...        ...         ...  ...         ...   ...  ...  ...
448  519513    万家日日薪货币R        ---         ---  ...  2013-01-15    郅元  0费率   购买
449  005202    兴业稳天盈货币B        ---         ---  ...  2017-09-11  丁进 等  0费率   购买
450  000908   农银红利日结货币B        ---         ---  ...  2014-12-19  许娅 等  0费率   购买
451  000907   农银红利日结货币A        ---         ---  ...  2014-12-19  许娅 等  0费率   购买
452  519507       万家货币B        ---         ---  ...  2013-08-15    郅元  0费率   购买
```
