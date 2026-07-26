---
title: "index_bei_cx - 基石经济指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_bei_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 基石经济指数
- 描述: 财新指数-基石经济指数
- 目标地址: https://yun.ccxe.com.cn/indices/bei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基石经济指数

接口: index_bei_cx

目标地址: https://yun.ccxe.com.cn/indices/bei

描述: 财新指数-基石经济指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 日期     | object  | -       |
| 基石经济指数 | float64 | -       |
| 变化幅度   | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_bei_cx_df = ak.index_bei_cx()
print(index_bei_cx_df)
```

数据示例

```
         日期      基石经济指数    变化幅度
0     2016-12-26   8337.3924  0.000000
1     2016-12-27   8337.7003  0.003693
2     2016-12-28   8298.5135 -0.469995
3     2016-12-29   8287.3093 -0.135015
4     2016-12-30   8314.6532  0.329949
...          ...         ...       ...
1802  2024-05-29  10352.7516 -0.105441
1803  2024-05-30  10279.0409 -0.711991
1804  2024-05-31  10275.1080 -0.038261
1805  2024-06-03  10217.6457 -0.559238
1806  2024-06-04  10283.8398  0.647841
[1807 rows x 3 columns]
```
