---
title: "index_si_cx - 溢出指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_si_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 溢出指数
- 描述: 财新指数-溢出指数
- 目标地址: https://yun.ccxe.com.cn/indices/dei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 溢出指数

接口: index_si_cx

目标地址: https://yun.ccxe.com.cn/indices/dei

描述: 财新指数-溢出指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 溢出指数 | float64 | -   |
| 变化值  | float64 | -   |

接口示例

```python
import akshare as ak

index_si_cx_df = ak.index_si_cx()
print(index_si_cx_df)
```

数据示例

```
        日期    溢出指数  变化值
0   2015-12-31  100.00   0.00
1   2016-01-31  137.07  37.07
2   2016-02-29  127.53  -9.54
3   2016-03-31  168.82  41.29
4   2016-04-30  157.51 -11.31
..         ...     ...    ...
67  2021-07-31   70.23   9.28
68  2021-08-31   25.26 -44.97
69  2021-09-30   29.86   4.60
70  2021-10-31   94.92  65.06
71  2021-11-30   48.24 -46.68
```
