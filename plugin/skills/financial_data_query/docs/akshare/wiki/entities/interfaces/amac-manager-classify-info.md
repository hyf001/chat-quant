---
title: "amac_manager_classify_info - 私募基金管理人分类公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_manager_classify_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 私募基金管理人公示 > 私募基金管理人分类公示
- 描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 私募基金管理人分类公示

接口: amac_manager_classify_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html

描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称                    | 类型     | 描述  |
|-----------------------|--------|-----|
| 私募基金管理人名称             | object | -   |
| 法定代表人/执行事务合伙人(委派代表)姓名 | object | -   |
| 机构类型                  | object | -   |
| 登记编号                  | object | -   |
| 注册地                   | object | -   |
| 办公地                   | object | -   |
| 成立时间                  | object | -   |
| 登记时间                  | object | -   |
| 在管基金数量                | int64  | -   |
| 会员类型                  | object | -   |
| 是否有提示信息               | object | -   |
| 是否有诚信信息               | object | -   |

接口示例

```python
import akshare as ak

amac_manager_classify_info_df = ak.amac_manager_classify_info()
print(amac_manager_classify_info_df)
```

数据示例

```
        私募基金管理人名称 法定代表人/执行事务合伙人(委派代表)姓名  ... 是否有提示信息 是否有诚信信息
0      平安道远投资管理（上海）有限公司                    王博  ...       是       否
1        上海重阳投资管理股份有限公司                    王庆  ...       否       否
2          上海景林资产管理有限公司                   高云程  ...       是       否
3        富舜资产管理（上海）有限公司                    周楠  ...       是       否
4            深圳民森投资有限公司                    蔡明  ...       否       否
                 ...                   ...  ...     ...     ...
21087  汉领（上海）私募基金管理有限公司                   夏明晨  ...       是       否
21088    青岛亿洋创业投资管理有限公司                   陆游龙  ...       是       否
21089    广州山岳私募基金管理有限公司                    柯声  ...       是       否
21090   东莞市生技私募基金管理有限公司                    肖丹  ...       是       否
21091  湖北农发创业投资基金管理有限公司                    熊赟  ...       是       否
[21092 rows x 12 columns]
```
