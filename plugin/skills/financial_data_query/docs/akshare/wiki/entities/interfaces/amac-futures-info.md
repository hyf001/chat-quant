---
title: "amac_futures_info - 期货公司集合资管产品公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_futures_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 期货公司集合资管产品公示
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/futures/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期货公司集合资管产品公示

接口: amac_futures_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/futures/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| 产品名称  | object | -  |
| 产品编码  | object | -  |
| 管理人名称 | object | -  |
| 托管人名称 | object | -  |
| 成立日期  | object | -  |
| 投资类型  | object | -  |
| 是否分级  | object | -  |
| 备案日期  | object | -  |
| 到期日   | object | -  |
| 运作状态  | object | -  |

接口示例

```python
import akshare as ak

amac_futures_info_df = ak.amac_futures_info()
print(amac_futures_info_df)
```

数据示例

```
              产品名称    产品编码       管理人名称  ...        备案日期         到期日  运作状态
0          大越期货高益集合资产管理计划  SAGG91  大越期货股份有限公司  ...  2024-04-03  2034-03-25  正在运作
1        大地期货新辰一号集合资产管理计划  SAHK47    大地期货有限公司  ...  2024-03-28  2029-03-26  正在运作
2        冠通资管兆享7号集合资产管理计划  SAHR85  冠通期货股份有限公司  ...  2024-04-03  2029-03-24  正在运作
3        盛达期货鑫鼎1号集合资产管理计划  SAHX81    盛达期货有限公司  ...  2024-04-01  2030-03-21  正在运作
4        华鑫期货鑫诚一号集合资产管理计划  SAFX88    华鑫期货有限公司  ...  2024-03-26  2039-03-18  正在运作
                   ...     ...         ...  ...         ...         ...   ...
9643       浙商期货春晓1号资产管理计划  S24005    浙商期货有限公司  ...  2015-05-21  2016-01-06  正常清算
9644      浙商多策略精选2号资产管理计划  S24001    浙商期货有限公司  ...  2015-05-12  2015-12-24  正常清算
9645       新湖资管稳健1号资产管理计划  S24002  新湖期货股份有限公司  ...  2015-06-01  2034-12-23  正在运作
9646  海证期货巨杉净值线1号集合资产管理计划  S94010    海证期货有限公司  ...  2014-06-03  2033-09-04  正在运作
9647      美尔雅-北极星1号资产管理计划  S30147    正信期货有限公司  ...  2015-06-04  2016-04-20  正常清算
[9648 rows x 10 columns]
```
