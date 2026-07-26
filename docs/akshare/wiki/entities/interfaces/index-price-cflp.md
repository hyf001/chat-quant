---
title: "index_price_cflp - 中国公路物流运价指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_price_cflp

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 公路物流指数 > 中国公路物流运价指数
- 描述: 获取指定 symbol 的中国公路物流运价指数的数据
- 目标地址: http://index.0256.cn/expx.htm
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中国公路物流运价指数

接口: index_price_cflp

目标地址: http://index.0256.cn/expx.htm

描述: 获取指定 symbol 的中国公路物流运价指数的数据

输入参数

| 名称     | 类型  | 描述                                                     |
|--------|-----|--------------------------------------------------------|
| symbol | str | symbol="周指数"; choice of {"周指数", "月指数", "季度指数", "年度指数"} |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 定基指数 | float64 | -   |
| 环比指数 | float64 | -   |
| 同比指数 | float64 | -   |

接口示例

```python
import akshare as ak

index_price_cflp_df = ak.index_price_cflp(symbol="周指数")
print(index_price_cflp_df)
```

数据示例

```
       日期     定基指数    环比指数   同比指数
0    2015-02-11  1119.47  1000.00  1000.00
1    2015-12-02  1051.89   988.25   960.54
2    2015-12-09  1028.40   977.67   981.28
3    2015-12-16   991.78   964.39   935.04
4    2015-12-23   995.84  1004.10   956.45
..          ...      ...      ...      ...
432  2024-04-24  1040.15  1015.40  1001.07
433  2024-05-01  1024.09   984.55   998.50
434  2024-05-08  1024.10  1000.01   997.71
435  2024-05-15  1024.11  1000.01   998.13
436  2024-05-22  1051.10  1026.36  1024.44
[437 rows x 4 columns]
```
