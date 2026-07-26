---
title: "amac_fund_sub_info - 证券公司私募投资基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_fund_sub_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 证券公司私募投资基金
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/subfund/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 证券公司私募投资基金

接口: amac_fund_sub_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/subfund/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称        | 类型     | 描述 |
|-----------|--------|----|
| 产品编码      | object | -  |
| 产品名称      | object | -  |
| 私募基金管理人名称 | object | -  |
| 托管人名称     | object | -  |
| 成立日期      | object | -  |
| 备案日期      | object | -  |

接口示例

```python
import akshare as ak

amac_fund_sub_info_df = ak.amac_fund_sub_info()
print(amac_fund_sub_info_df)
```

数据示例

```
       产品编码                        产品名称  ...       成立日期       备案日期
0     S32080          甘肃现代农业产业创业投资基金有限公司  ... 2012-12-25 2013-10-23
1     SD6315      中信并购投资基金（深圳）合伙企业（有限合伙）  ... 2012-11-15 2014-04-09
2     SD1670              中国－比利时直接股权投资基金  ... 2004-10-18 2014-04-17
3     SD1807      中投长春国家光电信息创业投资基金(有限合伙）  ... 2013-08-30 2014-04-21
4     SD2445      无锡国联领翔中小企业成长投资中心（有限合伙）  ... 2013-12-31 2014-04-22
      ...                         ...  ...        ...        ...
1687  SAGN06    中金辰盛（武汉）创业投资基金合伙企业（有限合伙）  ... 2024-01-12 2024-03-22
1688  SAHR12       温州大罗山瓯财股权投资合伙企业（有限合伙）  ... 2023-05-22 2024-03-22
1689  SAGB78   广州知城琶洲信德产业投资基金合伙企业 （有限合伙）  ... 2024-01-11 2024-03-25
1690  SAHY41  重庆荣昌创新发展私募股权投资基金合伙企业（有限合伙）  ... 2024-03-06 2024-04-03
1691  SAJJ25      广州智源和鑫创业投资基金合伙企业（有限合伙）  ... 2024-03-05 2024-04-03
[1692 rows x 6 columns]
```
