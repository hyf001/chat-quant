---
title: "index_bi_cx - 基础指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_bi_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 基础指数
- 描述: 财新指数-基础指数
- 目标地址: https://yun.ccxe.com.cn/indices/dei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基础指数

接口: index_bi_cx

目标地址: https://yun.ccxe.com.cn/indices/dei

描述: 财新指数-基础指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 基础指数 | float64 | -   |
| 变化值  | float64 | -   |

接口示例

```python
import akshare as ak

index_bi_cx_df = ak.index_bi_cx()
print(index_bi_cx_df)
```

数据示例

```
        日期    基础指数    变化值
0   2015-12-31  100.00   0.00
1   2016-01-31   99.15  -0.85
2   2016-02-29  122.47  23.32
3   2016-03-31  106.72 -15.75
4   2016-04-30  117.46  10.74
..         ...     ...    ...
67  2021-07-31   82.76  -5.40
68  2021-08-31   77.20  -5.56
69  2021-09-30   81.56   4.36
70  2021-10-31   83.50   1.94
71  2021-11-30   48.14 -35.36
```
