---
title: "index_neaw_cx - 新经济行业入职平均工资水平"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_neaw_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 新经济行业入职平均工资水平
- 描述: 财新指数-新经济行业入职平均工资水平
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新经济行业入职平均工资水平

接口: index_neaw_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-新经济行业入职平均工资水平

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型      | 描述  |
|---------------|---------|-----|
| 日期            | object  | -   |
| 新经济行业入职平均工资水平 | float64 | -   |
| 变化值           | float64 | -   |

接口示例

```python
import akshare as ak

index_neaw_cx_df = ak.index_neaw_cx()
print(index_neaw_cx_df)
```

数据示例

```
    日期    新经济行业入职平均工资水平  变化值
0   2015-07-31      7409.0000    0.0000
1   2015-08-31      7307.0000 -102.0000
2   2015-09-30      7367.0000   60.0000
3   2015-10-31      7298.0000  -69.0000
4   2015-11-30      7494.0000  196.0000
..         ...            ...       ...
73  2021-08-31     12905.0505  -27.7426
74  2021-09-30     13100.2551  195.2046
75  2021-10-31     13112.4344   12.1793
76  2021-11-30     13124.6137   12.1793
77  2021-12-31     13241.5176  116.9039
```
