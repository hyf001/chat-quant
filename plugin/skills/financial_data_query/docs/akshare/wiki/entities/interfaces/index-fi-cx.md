---
title: "index_fi_cx - 融合指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_fi_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 融合指数
- 描述: 财新指数-融合指数
- 目标地址: https://yun.ccxe.com.cn/indices/dei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 融合指数

接口: index_fi_cx

目标地址: https://yun.ccxe.com.cn/indices/dei

描述: 财新指数-融合指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 融合指数 | float64 | -   |
| 变化值  | float64 | -   |

接口示例

```python
import akshare as ak

index_fi_cx_df = ak.index_fi_cx()
print(index_fi_cx_df)
```

数据示例

```
      日期      融合指数    变化值
0   2015-12-31  100.00   0.00
1   2016-01-31   83.26 -16.74
2   2016-02-29   86.49   3.23
3   2016-03-31   80.90  -5.59
4   2016-04-30   84.22   3.32
..         ...     ...    ...
67  2021-07-31  254.47  -6.94
68  2021-08-31  244.25 -10.22
69  2021-09-30  246.41   2.16
70  2021-10-31  222.03 -24.38
71  2021-11-30  253.82  31.79
```
