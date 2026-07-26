---
title: "index_pmi_ser_cx - 服务业 PMI"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_pmi_ser_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 服务业 PMI
- 描述: 财新数据-指数报告-财新中国 PMI-服务业 PMI
- 目标地址: https://yun.ccxe.com.cn/indices/pmi
- 限量: 该接口返回所有历史数据，该数据更新至 202507 截止；
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 服务业 PMI

接口: index_pmi_ser_cx

目标地址: https://yun.ccxe.com.cn/indices/pmi

描述: 财新数据-指数报告-财新中国 PMI-服务业 PMI

限量: 该接口返回所有历史数据，该数据更新至 202507 截止；

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 服务业PMI | float64 | -   |
| 变化值    | float64 | -   |

接口示例

```python
import akshare as ak

index_pmi_ser_cx_df = ak.index_pmi_ser_cx()
print(index_pmi_ser_cx_df)
```

数据示例

```
       日期  服务业PMI  变化值
0   2014-04-29    51.4  0.0
1   2014-05-30    50.7 -0.7
2   2014-06-29    53.1  2.4
3   2014-07-30    50.0 -3.1
4   2014-08-30    54.1  4.1
..         ...     ...  ...
90  2021-09-29    53.4  6.7
91  2021-10-30    53.8  0.4
92  2021-11-29    52.1 -1.7
93  2021-12-30    53.1  1.0
94  2022-01-30    51.4 -1.7
```
