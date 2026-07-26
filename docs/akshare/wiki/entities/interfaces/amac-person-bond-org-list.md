---
title: "amac_person_bond_org_list - 债券投资交易相关人员公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_person_bond_org_list

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 从业人员信息 > 债券投资交易相关人员公示
- 描述: 中国证券投资基金业协会-信息公示-从业人员信息-债券投资交易相关人员公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/person/personOrgList.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 债券投资交易相关人员公示

接口: amac_person_bond_org_list

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/person/personOrgList.html

描述: 中国证券投资基金业协会-信息公示-从业人员信息-债券投资交易相关人员公示

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 序号   | int64  | -   |
| 机构类型 | object | -   |
| 机构名称 | object | -   |
| 公示网址 | object | -   |

接口示例

```python
import akshare as ak

amac_person_bond_org_list_df = ak.amac_person_bond_org_list()
print(amac_person_bond_org_list_df)
```

数据示例

```
      序号  ...                                               公示网址
0      1  ...  https://www.essencefund.com/mall/views/custser...
1      2  ...  http://www.baijiafunds.com.cn/aboutus/annnounc...
2      3  ...  http://www.byfunds.com/baoying/aboutus/about-u...
3      4  ...  http://www.cdbsfund.com/main/gywm/zzcx/index.s...
4      5  ...  https://www.bxrfund.com/#/list?menuid=10129&se...
..   ...  ...                                                ...
302  303  ...     https://www.citicsam.com/nformation/personnel/
303  304  ...  https://www.tkfunds.com.cn/aboutus/bondstaff/i...
304  305  ...  http://fund.piccamc.com/pc/newsInfo/articleInf...
305  306  ...         http://www.ebscn.com/gdzb/views/index.html
306  307  ...         https://hs.guosen.com.cn/hs/xxgs_zqjy.html
[307 rows x 4 columns]
```
