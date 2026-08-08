---
title: "index_nei_cx - 中国新经济指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_nei_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 中国新经济指数
- 描述: 财新指数-中国新经济指数
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中国新经济指数

接口: index_nei_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-中国新经济指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 日期      | object  | -   |
| 中国新经济指数 | float64 | -   |
| 变化值     | float64 | -   |

接口示例

```python
import akshare as ak

index_nei_cx_df = ak.index_nei_cx()
print(index_nei_cx_df)
```

数据示例

```
     日期    中国新经济指数       变化值
0   2016-04-30  32.030085  0.000000
1   2016-05-31  34.687431  2.657346
2   2016-06-30  32.163383 -2.524048
3   2016-07-31  31.420723 -0.742660
4   2016-08-31  32.140547  0.719824
..         ...        ...       ...
64  2021-08-31  28.225149 -0.311624
65  2021-09-30  28.885370  0.660221
66  2021-10-31  29.643365  0.757995
67  2021-11-30  28.056617 -1.586748
68  2021-12-31  29.464567  1.407950
```
