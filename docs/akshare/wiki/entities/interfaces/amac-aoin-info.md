---
title: "amac_aoin_info - 证券公司直投基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_aoin_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 证券公司直投基金
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司直投基金
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/aoin/product/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 证券公司直投基金

接口: amac_aoin_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/aoin/product/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司直投基金

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| 产品编码  | object | -  |
| 产品名称  | object | -  |
| 直投子公司 | object | -  |
| 管理机构  | object | -  |
| 设立日期  | object | -  |

接口示例

```python
import akshare as ak

amac_aoin_info_df = ak.amac_aoin_info()
print(amac_aoin_info_df)
```

数据示例

```
       产品编码                             产品名称  ...                  管理机构       设立日期
0    S32077            深圳市远盛发展一期股权投资企业（有限合伙）  ...         深圳市远盛投资管理有限公司 2012-12-26
1    S32105             新疆华融天泽鼎鑫投资合伙企业（有限合伙）  ...            华融天泽投资有限公司 2013-03-14
2    S32073               新疆广发信德广电夹层投资有限合伙企业  ...      新疆广发信德稳胜投资管理有限公司 2013-03-25
3    S32644             吉林省国家新材料产业创业投资有限责任公司  ...      北京一创吉星创业投资管理有限公司 2013-05-24
4    S32067                 赣州致发投资合伙企业（有限合伙）  ...        江西致远发展投资管理有限公司 2013-07-09
..      ...                              ...  ...                   ...        ...
219  S32563             桂银柳江新型城镇化城市发展契约型私募基金  ...        贵州兴黔财富资本管理有限公司 2017-06-30
220  S32630                       兴黔一号私募投资基金  ...        贵州兴黔财富资本管理有限公司 2017-07-13
221  S32557                 南宁交轨投资合伙企业（有限合伙）  ...        贵州兴黔财富资本管理有限公司 2017-10-25
222  S32565                南宁桂耀城投资合伙企业（有限合伙）  ...        贵州兴黔财富资本管理有限公司 2017-11-27
223  S32582  深圳润信新观象战略新兴产业私募股权投资基金合伙企业（有限合伙）  ...  深圳市润信新观象股权投资基金管理有限公司 2018-04-24
[224 rows x 5 columns]
```
