---
title: "index_ii_cx - 产业指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_ii_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 产业指数
- 描述: 财新指数-产业指数
- 目标地址: https://yun.ccxe.com.cn/indices/dei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 产业指数

接口: index_ii_cx

目标地址: https://yun.ccxe.com.cn/indices/dei

描述: 财新指数-产业指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 产业指数 | float64 | -   |
| 变化值  | float64 | -   |

接口示例

```python
import akshare as ak

index_ii_cx_df = ak.index_ii_cx()
print(index_ii_cx_df)
```

数据示例

```
        日期    产业指数    变化值
0   2015-12-31  100.00   0.00
1   2016-01-31   83.97 -16.03
2   2016-02-29  139.06  55.09
3   2016-03-31  126.96 -12.10
4   2016-04-30  138.11  11.15
..         ...     ...    ...
67  2021-07-31  434.87  -9.52
68  2021-08-31  353.89 -80.98
69  2021-09-30  260.27 -93.62
70  2021-10-31  261.97   1.70
71  2021-11-30  310.74  48.77
```
