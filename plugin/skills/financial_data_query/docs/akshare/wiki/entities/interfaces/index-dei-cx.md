---
title: "index_dei_cx - 数字经济指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_dei_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 数字经济指数
- 描述: 财新指数-数字经济指数
- 目标地址: https://yun.ccxe.com.cn/indices/dei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 数字经济指数

接口: index_dei_cx

目标地址: https://yun.ccxe.com.cn/indices/dei

描述: 财新指数-数字经济指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 数字经济指数 | float64 | -   |
| 变化值    | float64 | -   |

接口示例

```python
import akshare as ak

index_dei_cx_df = ak.index_dei_cx()
print(index_dei_cx_df)
```

数据示例

```
     日期      数字经济指数 变化值
0   2015-12-31  100.00    0.00
1   2016-01-31   89.63  -10.37
2   2016-02-29  107.70   18.07
3   2016-03-31  116.13    8.43
4   2016-04-30  126.67   10.54
..         ...     ...     ...
67  2021-07-31  585.00    6.00
68  2021-08-31  439.00 -146.00
69  2021-09-30  413.00  -26.00
70  2021-10-31  593.00  180.00
71  2021-11-30  435.00 -158.00
```
