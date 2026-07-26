---
title: "futures_index_ccidx - 中证商品指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_index_ccidx

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 中证商品指数 > 中证商品指数
- 描述: 中证商品指数
- 目标地址: http://www.ccidx.com/index.html
- 限量: 单次返回指定 symbol 的指数日频率数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中证商品指数

接口: futures_index_ccidx

目标地址: http://www.ccidx.com/index.html

描述: 中证商品指数

限量: 单次返回指定 symbol 的指数日频率数据

输入参数

| 名称     | 类型  | 描述                                                        |
|--------|-----|-----------------------------------------------------------|
| symbol | str | symbol="中证商品期货指数"; choice of {"中证商品期货指数", "中证商品期货价格指数", } |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
| 指数代码 | object  | -  |
| 收盘点位 | float64 | -  |
| 结算点位 | float64 | -  |
| 涨跌   | float64 | -  |
| 涨跌幅  | float64 | -  |

接口示例

```python
import akshare as ak

futures_index_ccidx_df = ak.futures_index_ccidx(symbol="中证商品期货指数")
print(futures_index_ccidx_df)
```

数据示例

```
     日期        指数代码      收盘点位  结算点位   涨跌   涨跌幅
0    2021-02-18  100001.CCI  1421.18  1414.30  45.82  3.35
1    2021-02-19  100001.CCI  1420.86  1419.17   4.87  0.34
2    2021-02-22  100001.CCI  1439.96  1437.49  18.32  1.29
3    2021-02-23  100001.CCI  1447.08  1445.75   8.26  0.57
4    2021-02-24  100001.CCI  1449.70  1443.34  -2.41 -0.17
..          ...         ...      ...      ...    ...   ...
960  2025-02-06  100001.CCI  1965.37  1958.64   3.38  0.17
961  2025-02-07  100001.CCI  1977.99  1972.23  13.59  0.69
962  2025-02-10  100001.CCI  1984.26  1979.65   7.42  0.38
963  2025-02-11  100001.CCI  1981.76  1985.65   6.00  0.30
964  2025-02-12  100001.CCI  1986.45  1981.82  -3.83 -0.19
[965 rows x 6 columns]
```
