---
title: "bond_available_index_cbond - 可选指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_available_index_cbond

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中债指数 > 中债指数族系 > 可选指数
- 描述: 中国债券信息网-中债指数-中债指数族系当中, 非指定期限部分的可选指数
- 目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 可选指数

接口: bond_available_index_cbond

目标地址: https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult

描述: 中国债券信息网-中债指数-中债指数族系当中, 非指定期限部分的可选指数

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称    | 类型  | 描述 |
|-------|-----|----|
| index | int | -  |
| value | str | -  |

接口示例

```python
import akshare as ak

bond_available_index_cbond_df = ak.bond_available_index_cbond()
print(bond_available_index_cbond_df)
```

数据示例

```
     index                    value
0        1                    新综合指数
1        2            高等级科技创新债券综合指数
2        3             长江养老年金基金债券指数
3        4  中信证券挂钩DR浮动利率政策性银行债活跃券指数
4        5            股份制商业银行同业存单指数
..     ...                      ...
308    309             粤港澳大湾区债券综合指数
309    310               利差驱动股债稳健指数
310    311           中债信用增进公司增信债券指数
311    312                 银行金融债券指数
312    313               乡村振兴债券综合指数
[313 rows x 2 columns]
```
