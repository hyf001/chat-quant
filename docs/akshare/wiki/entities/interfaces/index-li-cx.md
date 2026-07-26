---
title: "index_li_cx - 劳动力投入指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_li_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 劳动力投入指数
- 描述: 财新指数-劳动力投入指数
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 劳动力投入指数

接口: index_li_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-劳动力投入指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 日期      | object  | -   |
| 劳动力投入指数 | float64 | -   |
| 变化值     | float64 | -   |

接口示例

```python
import akshare as ak

index_li_cx_df = ak.index_li_cx()
print(index_li_cx_df)
```

数据示例

```
     日期       劳动力投入指数    变化值
0   2015-07-31  29.741385   0.000000
1   2015-08-31  28.091280  -1.650105
2   2015-09-30  42.663765  14.572485
3   2015-10-31  32.824430  -9.839335
4   2015-11-30  38.791985   5.967555
..         ...        ...        ...
73  2021-08-31  20.802475  -3.385175
74  2021-09-30  22.275790   1.473315
75  2021-10-31  25.326500   3.050710
76  2021-11-30  23.458940  -1.867560
77  2021-12-31  22.587685  -0.871255
```
