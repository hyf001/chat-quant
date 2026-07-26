---
title: "amac_manager_info - 私募基金管理人综合查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_manager_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 私募基金管理人公示 > 私募基金管理人综合查询
- 描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 私募基金管理人综合查询

接口: amac_manager_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html

描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称                    | 类型     | 描述 |
|-----------------------|--------|----|
| 私募基金管理人名称             | object | -  |
| 法定代表人/执行事务合伙人(委派代表)姓名 | object | -  |
| 机构类型                  | object | -  |
| 注册地                   | object | -  |
| 登记编号                  | object | -  |
| 成立时间                  | object | -  |
| 登记时间                  | object | -  |

接口示例

```python
import akshare as ak

amac_manager_info_df = ak.amac_manager_info()
print(amac_manager_info_df)
```

数据示例

```
              私募基金管理人名称 法定代表人/执行事务合伙人(委派代表)姓名  ...        成立时间        登记时间
0      平安道远投资管理（上海）有限公司                    王博  ...  2011-03-15  2014-03-17
1        上海重阳投资管理股份有限公司                    王庆  ...  2009-06-26  2014-03-17
2          上海景林资产管理有限公司                   高云程  ...  2012-06-06  2014-03-17
3        富舜资产管理（上海）有限公司                    周楠  ...  2012-02-10  2014-03-17
4            深圳民森投资有限公司                    蔡明  ...  2007-04-05  2014-03-17
                 ...                   ...  ...         ...         ...
21087  汉领（上海）私募基金管理有限公司                   夏明晨  ...  2022-09-07  2024-03-18
21088    青岛亿洋创业投资管理有限公司                   陆游龙  ...  2024-02-05  2024-03-25
21089    广州山岳私募基金管理有限公司                    柯声  ...  2023-08-15  2024-03-25
21090   东莞市生技私募基金管理有限公司                    肖丹  ...  2022-10-28  2024-04-01
21091  湖北农发创业投资基金管理有限公司                    熊赟  ...  2023-08-21  2024-04-01
[21092 rows x 7 columns]
```
