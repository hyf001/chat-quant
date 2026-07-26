---
title: "bond_index_general_cbond - 指数族系查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_index_general_cbond

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中债指数 > 中债指数族系 > 指数族系查询
- 描述: 中国债券信息网-中债指数-中债指数族系
- 目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 指数族系查询

接口: bond_index_general_cbond

目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult

描述: 中国债券信息网-中债指数-中债指数族系

输入参数

| 名称             | 类型  | 描述                                                                                                                                                                                                       |
|----------------|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| index_category | str | index_category="新综合指数"; index_category 取值参考 `ak.bond_available_index_cbond()` 的返回结果                                                                                                                      |
| indicator      | str | indicator="财富"; choice of {"全价", "净价", "财富", "平均市值法久期", "平均现金流法久期", "平均市值法凸性", "平均现金流法凸性", "平均现金流法到期收益率", "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率", "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"} |
| periods        | str | period="总值"; choice of {"总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上", "0-3个月", "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"}                                                                  |

输出参数

| 名称    | 类型      | 描述   |
|-------|---------|------|
| date  | object  | 时间索引 |
| value | float64 | 注意单位 |

接口示例

```python
import akshare as ak

bond_index_general_cbond_df = ak.bond_index_general_cbond(index_category="新综合指数", indicator="全价", period="总值")
print(bond_index_general_cbond_df)
```

数据示例

```
            date     value
0     2002-01-04   99.9731
1     2002-01-07  100.0149
2     2002-01-08   99.8273
3     2002-01-09  100.0203
4     2002-01-10   99.9317
...          ...       ...
6065  2026-04-03  129.1454
6066  2026-04-07  129.2360
6067  2026-04-08  129.3017
6068  2026-04-09  129.3146
6069  2026-04-10  129.3696
[6070 rows x 2 columns]
```
