---
title: "amac_fund_account_info - 基金公司及子公司集合资管产品公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_fund_account_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 基金公司及子公司集合资管产品公示
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 基金公司及子公司集合资管产品公示

接口: amac_fund_account_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| 成立日期  | object | -  |
| 产品编码  | object | -  |
| 产品名称  | object | -  |
| 管理人名称 | object | -  |

接口示例

```python
import akshare as ak

amac_fund_account_info_df = ak.amac_fund_account_info()
print(amac_fund_account_info_df)
```

数据示例

```
         成立日期    产品编码                         产品名称           管理人名称
0     2024-04-02  SAHT40          建信尊享吉康一年13号集合资产管理计划    建信基金管理有限责任公司
1     2024-04-01  SAJA72  华夏资本-AU9999龙腾宁惠跃享6号集合资产管理计划      华夏资本管理有限公司
2     2024-03-29  SAJL52            创金合信创力20号集合资产管理计划    创金合信基金管理有限公司
3     2024-03-29  SAJD21          招商财富-丰利联动1号集合资产管理计划    招商财富资产管理有限公司
4     2024-03-29  SACX99             创金合信聚睿6号集合资产管理计划    创金合信基金管理有限公司
          ...     ...                          ...             ...
38244        NaT  S93786              千石资本-天演5期资产管理计划  北京千石创富资本管理有限公司
38245        NaT  ST3713        汇添富资本-添添富理财7天专项资产管理计划     汇添富资本管理有限公司
38246        NaT  S88308         金元惠理江阴首府花园1号专项资产管理计划  上海金元百利资产管理有限公司
38247        NaT  S92026          中银资产-信利系列5号专项资产管理计划      中银资产管理有限公司
38248        NaT  S88283         金元惠理延安保障房12号专项资产管理计划  上海金元百利资产管理有限公司
[38249 rows x 4 columns]
```
