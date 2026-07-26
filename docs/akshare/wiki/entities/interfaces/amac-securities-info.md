---
title: "amac_securities_info - 证券公司集合资管产品公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_securities_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 证券公司集合资管产品公示
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司集合资管产品公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 证券公司集合资管产品公示

接口: amac_securities_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-证券公司集合资管产品公示

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
| 成立日期  | object | -  |
| 到期时间  | object | -  |
| 投资类型  | object | -  |
| 是否分级  | object | -  |
| 托管人名称 | object | -  |
| 备案日期  | object | -  |
| 运作状态  | object | -  |

接口示例

```python
import akshare as ak

amac_securities_info_df = ak.amac_securities_info()
print(amac_securities_info_df)
```

数据示例

```
                                  产品名称    产品编码  ...        备案日期  运作状态
0      华泰拉普拉斯家园1号科创板员工持股集合资产管理计划  SAHB48  ...  2024-04-03  正在运作
1             国泰君安君享兴盈1号集合资产管理计划  SAJN14  ...  2024-04-02  正在运作
2          方正证券满盈12M003号集合资产管理计划  SAHT72  ...  2024-04-02  正在运作
3             光证资管渝选增强1号集合资产管理计划  SAJM87  ...  2024-04-03  正在运作
4            华源证券安鑫周周盈3号集合资产管理计划  SAJN58  ...  2024-04-02  正在运作
                          ...     ...  ...         ...   ...
20286           申银万国宝鼎1期集合资产管理计划  S00792  ...  2013-05-07  正在运作
20287       东方红-先锋2号（展期）集合资产管理计划  S00052  ...  2013-05-07  正在运作
20288           光证资管添盈1号集合资产管理计划  S08647  ...  2013-08-20  正在运作
20289               中金一号集合资产管理计划  S00773  ...  2013-07-01  提前清算
20290            东方红先锋1号集合资产管理计划  S00844  ...  2013-05-07  正在运作
[20291 rows x 10 columns]
```
