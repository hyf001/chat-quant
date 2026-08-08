---
title: "index_component_sw - 申万指数成分股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_component_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 申万指数成分股
- 描述: 申万宏源研究-指数发布-指数详情-成分股
- 目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801001&name=申万中小
- 限量: 该接口返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 申万指数成分股

接口: index_component_sw

目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801001&name=申万中小

描述: 申万宏源研究-指数发布-指数详情-成分股

限量: 该接口返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                               |
|--------|-----|--------------------------------------------------|
| symbol | str | symbol="801001"; 指数代码                            |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 序号   | int64   | -   |
| 证券代码 | object  | -   |
| 证券名称 | object  | -   |
| 最新权重 | float64 | -   |
| 计入日期 | object  | -   |

接口示例

```python
import akshare as ak

index_component_sw_df = ak.index_component_sw(symbol="801001")
print(index_component_sw_df)
```

数据示例

```
      序号 证券代码  证券名称  最新权重  计入日期
0      1  000001  平安银行  1.2094  2023-07-03
1      2  000002   万科A  1.1122  2023-07-03
2      3  000063  中兴通讯  1.1810  2023-07-03
3      4  000333  美的集团  3.5702  2023-07-03
4      5  000568  泸州老窖  2.2004  2023-07-03
..   ...     ...   ...     ...         ...
145  146  601919  中远海控  0.6996  2024-07-01
146  147  603259  药明康德  1.2209  2024-07-01
147  148  603993  洛阳钼业  0.7059  2024-07-01
148  149  688041  海光信息  1.2586  2024-07-01
149  150  688111  金山办公  0.6166  2024-07-01
[150 rows x 5 columns]
```
