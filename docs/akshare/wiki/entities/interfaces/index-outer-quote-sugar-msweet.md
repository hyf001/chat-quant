---
title: "index_outer_quote_sugar_msweet - 配额外进口糖估算指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_outer_quote_sugar_msweet

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 配额外进口糖估算指数
- 描述: 沐甜科技数据中心-配额外进口糖估算指数
- 目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 配额外进口糖估算指数

接口: index_outer_quote_sugar_msweet

目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html

描述: 沐甜科技数据中心-配额外进口糖估算指数

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型      | 描述  |
|-----------|---------|-----|
| 日期        | object  | -   |
| 巴西糖进口成本   | float64 | -   |
| 泰国糖进口利润空间 | float64 | -   |
| 巴西糖进口利润空间 | float64 | -   |
| 泰国糖进口成本   | float64 | -   |
| 日照现货价     | float64 | -   |

接口示例

```python
import akshare as ak

index_outer_quote_sugar_msweet_df = ak.index_outer_quote_sugar_msweet()
print(index_outer_quote_sugar_msweet_df)
```

数据示例

```
      日期  巴西糖进口成本  泰国糖进口利润空间  巴西糖进口利润空间  泰国糖进口成本  日照现货价
0     2014-12-05   4637.0     4491.0       4770    133.0  279.0
1     2014-12-08   4697.0     4549.0       4770     73.0  221.0
2     2014-12-09   4774.0     4590.0       4770     -4.0  180.0
3     2014-12-10   4782.0     4607.0       4820     38.0  213.0
4     2014-12-11   4758.0     4772.0       4870    112.0   98.0
          ...      ...        ...        ...      ...    ...
1775  2023-01-13   6380.0     6416.0       6260   -156.0 -120.0
1776  2023-01-17   6529.0     6552.0       6260   -292.0 -269.0
1777  2023-01-18   6439.0     6462.0       6260   -202.0 -179.0
1778  2023-01-30   6782.0     6808.0       6260   -548.0 -522.0
1779  2023-01-31   6938.0     6964.0       6260   -704.0 -678.0
[1780 rows x 6 columns]
```
