---
title: "index_cci_cx - 大宗商品指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_cci_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 大宗商品指数
- 描述: 财新指数-大宗商品指数
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 大宗商品指数

接口: index_cci_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-大宗商品指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 大宗商品指数 | float64 | -   |
| 变化值    | float64 | -   |

接口示例

```python
import akshare as ak

index_cci_cx_df = ak.index_cci_cx()
print(index_cci_cx_df)
```

数据示例

```
          日期      大宗商品指数    变化值
0     2009-01-09  100.000000  0.000000
1     2009-01-12  101.643734  1.643734
2     2009-01-13   98.992944 -2.607922
3     2009-01-14  100.396208  1.417539
4     2009-01-15  100.151055 -0.244186
...          ...         ...       ...
3735  2024-05-29  361.046067  0.890980
3736  2024-05-30  356.980276 -1.126114
3737  2024-05-31  355.491012 -0.417184
3738  2024-06-03  350.137547 -1.505935
3739  2024-06-04  347.889373 -0.642083
[3740 rows x 3 columns]
```
