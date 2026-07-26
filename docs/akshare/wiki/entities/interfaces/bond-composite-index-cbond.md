---
title: "bond_composite_index_cbond - 综合指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_composite_index_cbond

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中债指数 > 总指数 > 综合类指数 > 综合指数
- 描述: 中国债券信息网-中债指数-中债指数族系-分类指数-按待偿期限
- 目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/single_index_query
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 综合指数

接口: bond_composite_index_cbond

目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/single_index_query

描述: 中国债券信息网-中债指数-中债指数族系-分类指数-按待偿期限

输入参数

| 名称        | 类型  | 描述                                                                                                                                                                                                       |
|-----------|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| indicator | str | indicator="财富"; choice of {"全价", "净价", "财富", "平均市值法久期", "平均现金流法久期", "平均市值法凸性", "平均现金流法凸性", "平均现金流法到期收益率", "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率", "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"} |
| period    | str | period="总值"; choice of {"总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上", "0-3个月", "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"}                                                                  |

输出参数

| 名称    | 类型      | 描述   |
|-------|---------|------|
| date  | object  | -    |
| value | float64 | 注意单位 |

接口示例

```python
import akshare as ak

bond_composite_index_cbond_df = ak.bond_composite_index_cbond(indicator="财富", period="总值")
print(bond_composite_index_cbond_df)
```

数据示例

```
            date     value
0     2002-01-03   99.9731
1     2002-01-06  100.0149
2     2002-01-07   99.8273
3     2002-01-08  100.0203
4     2002-01-09   99.9317
          ...       ...
5429  2023-09-11  232.4624
5430  2023-09-12  232.5571
5431  2023-09-13  232.6593
5432  2023-09-14  232.5994
5433  2023-09-17  232.5021
[5434 rows x 2 columns]
```
