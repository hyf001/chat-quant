---
title: "amac_fund_abs - 资产支持专项计划"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_fund_abs

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 资产支持专项计划
- 描述: 中国证券投资基金业协会-信息公示-产品公示-资产支持专项计划
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/fund/abs/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 资产支持专项计划

接口: amac_fund_abs

目标地址: https://gs.amac.org.cn/amac-infodisc/res/fund/abs/index.html

描述: 中国证券投资基金业协会-信息公示-产品公示-资产支持专项计划

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 编号     | int64  | -  |
| 备案编号   | object | -  |
| 专项计划全称 | object | -  |
| 管理人    | object | -  |
| 托管人    | object | -  |
| 成立日期   | object | -  |
| 预期到期时间 | object | -  |
| 备案通过时间 | object | -  |

接口示例

```python
import akshare as ak

amac_fund_abs_df = ak.amac_fund_abs()
print(amac_fund_abs_df)
```

数据示例

```
      编号  备案编号  ...   预期到期时间  备案通过时间
0        1  S29340  ...  2018-02-15  2015-04-23
1        2  S33309  ...  2020-01-22  2015-04-23
2        3  S33578  ...  2020-04-14  2015-05-07
3        4  S33490  ...  2020-04-13  2015-05-07
4        5  S34510  ...  2022-03-25  2015-05-07
    ...     ...  ...         ...         ...
8335  8336  S37011  ...  2020-05-19  2015-06-07
8336  8337  S38847  ...  2018-05-17  2015-06-07
8337  8338  S39153  ...  2018-03-07  2015-06-07
8338  8339  S38598  ...  2017-05-18  2015-06-07
8339  8340  S37663  ...  2016-08-21  2015-06-07
[8340 rows x 8 columns]
```
