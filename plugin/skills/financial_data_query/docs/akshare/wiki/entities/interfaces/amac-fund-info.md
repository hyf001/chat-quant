---
title: "amac_fund_info - 私募基金管理人基金产品"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_fund_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 基金产品 > 私募基金管理人基金产品
- 描述: 中国证券投资基金业协会-信息公示-基金产品公示-私募基金管理人基金产品
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html
- 限量: 单次返回指定页码之间的所有历史数据, 其中与每页 100 条的目标网站对应; 默认返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 私募基金管理人基金产品

接口: amac_fund_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html

描述: 中国证券投资基金业协会-信息公示-基金产品公示-私募基金管理人基金产品

限量: 单次返回指定页码之间的所有历史数据, 其中与每页 100 条的目标网站对应; 默认返回所有数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_page | str | start_page='1'; 开始页码  |
| end_page   | str | end_page="2000"; 结束页码 |

输出参数

| 名称        | 类型     | 描述 |
|-----------|--------|----|
| 基金名称      | object | -  |
| 私募基金管理人名称 | object | -  |
| 私募基金管理人类型 | object | -  |
| 运行状态      | object | -  |
| 备案时间      | object | -  |
| 建立时间      | object | -  |
| 托管人名称     | object | -  |

接口示例

```python
import akshare as ak

amac_fund_info_df = ak.amac_fund_info(start_page="1", end_page='100')
print(amac_fund_info_df)
```

数据示例

```
                          基金名称           私募基金管理人名称  ...        建立时间           托管人名称
0               长安万丰贯富4号资产管理计划      上海万丰友方投资管理有限公司  ...  2013-09-22  上海浦东发展银行股份有限公司
1              红塔红土基金—翼虎量化对冲二期       深圳市翼虎投资管理有限公司  ...  2013-02-08      上海银行股份有限公司
2             万家正行季季加利专项资产管理计划    歌斐诺宝（上海）资产管理有限公司  ...  2013-03-11      兴业银行股份有限公司
3           指财通基金-耀之债期1号资产管理计划  上海耀之私募基金管理中心（有限合伙）  ...  2013-11-06    中国光大银行股份有限公司
4     万家共赢歌斐诺宝精选组合3号三期专项资产管理计划    歌斐诺宝（上海）资产管理有限公司  ...  2014-01-13      宁波银行股份有限公司
                        ...                 ...  ...         ...             ...
9995          景泰复利回报第十五期证券投资基金     深圳市景泰利丰投资发展有限公司  ...  2015-04-23      交通银行股份有限公司
9996       浙商证券-望正诚朴1号私募证券投资基金        深圳望正资产管理有限公司  ...  2015-05-19      交通银行股份有限公司
9997                  持赢复利1期基金      南京持赢私募基金管理有限公司  ...  2015-05-01      南京银行股份有限公司
9998              惠正创富私募证券投资基金      广东惠正私募基金管理有限公司  ...  2015-05-27      招商证券股份有限公司
9999        恒天财富稳增金狮1号灵活策略对冲基金        恒天中岩投资管理有限公司  ...  2015-05-20      中信证券股份有限公司
[10000 rows x 7 columns]
```
