---
title: "index_ci_cx - 资本投入指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_ci_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 资本投入指数
- 描述: 财新指数-资本投入指数
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 资本投入指数

接口: index_ci_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-资本投入指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 资本投入指数 | float64 | -   |
| 变化值    | float64 | -   |

接口示例

```python
import akshare as ak

index_ci_cx_df = ak.index_ci_cx()
print(index_ci_cx_df)
```

数据示例

```
    日期        资本投入指数      变化值
0   2015-07-31  31.994724   0.000000
1   2015-08-31  34.098210   2.103486
2   2015-09-30  22.844344 -11.253866
3   2015-10-31  35.136466  12.292122
4   2015-11-30  28.143112  -6.993354
..         ...        ...        ...
73  2021-08-31  37.308966   3.053250
74  2021-09-30  37.306790  -0.002176
75  2021-10-31  35.004714  -2.302076
76  2021-11-30  34.531942  -0.472772
77  2021-12-31  39.438158   4.906216
```
