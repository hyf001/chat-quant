---
title: "futures_comex_inventory - COMEX 库存数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_comex_inventory

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > COMEX 库存数据
- 描述: 东方财富网-数据中心-期货期权-COMEX 库存数据
- 目标地址: https://data.eastmoney.com/pmetal/comex/by.html
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### COMEX 库存数据

接口: futures_comex_inventory

目标地址: https://data.eastmoney.com/pmetal/comex/by.html

描述: 东方财富网-数据中心-期货期权-COMEX 库存数据

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                  |
|--------|-----|-------------------------------------|
| symbol | str | symbol="黄金"; choice of {"黄金", "白银"} |

输出参数

| 名称                  | 类型      | 描述       |
|---------------------|---------|----------|
| 序号                  | int64   | -        |
| 日期                  | object  | -        |
| COMEX{symbol}库存量-吨  | float64 | 注意单位: 盎司 |
| COMEX{symbol}库存量-盎司 | float64 | 注意单位: 吨  |

接口示例

```python
import akshare as ak

futures_comex_inventory_df = ak.futures_comex_inventory(symbol="黄金")
print(futures_comex_inventory_df)
```

数据示例

```
     序号      日期  COMEX白银库存量-吨  COMEX白银库存量-盎司
0        1  2018-11-15    249.638588   8.026061e+06
1        2  2018-11-16    249.638588   8.026061e+06
2        3  2018-11-19    249.618620   8.025419e+06
3        4  2018-11-20    249.318222   8.015761e+06
4        5  2018-11-21    249.318222   8.015761e+06
    ...         ...           ...            ...
1244  1245  2023-11-08    618.567383   1.988739e+07
1245  1246  2023-11-09    618.564383   1.988729e+07
1246  1247  2023-11-10    618.462382   1.988401e+07
1247  1248  2023-11-13    618.461542   1.988399e+07
1248  1249  2023-11-14    618.461542   1.988399e+07
[1249 rows x 4 columns]
```
