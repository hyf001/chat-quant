---
title: "futures_inventory_em - 库存数据-东方财富"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_inventory_em

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 库存数据-东方财富
- 描述: 东方财富网-期货数据-库存数据; 近 60 个交易日的期货库存日频率数据
- 目标地址: http://data.eastmoney.com/ifdata/kcsj.html
- 限量: 返回指定交易所指定品种的期货库存数据, 仓单日报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 库存数据-东方财富

接口: futures_inventory_em

目标地址: http://data.eastmoney.com/ifdata/kcsj.html

描述: 东方财富网-期货数据-库存数据; 近 60 个交易日的期货库存日频率数据

限量: 返回指定交易所指定品种的期货库存数据, 仓单日报数据

输入参数

| 名称     | 类型  | 描述                                                                         |
|--------|-----|----------------------------------------------------------------------------|
| symbol | str | symbol="A"; 支持品种代码和中文名称，中文名称参见：https://data.eastmoney.com/ifdata/kcsj.html |

输出参数

| 名称  | 类型      | 描述          |
|-----|---------|-------------|
| 日期  | object  | 日期          |
| 库存  | int64   | 库存数据        |
| 增减  | float64 | 相对前一个交易日的增减 |

接口示例

```python
import akshare as ak

futures_inventory_em_df = ak.futures_inventory_em(symbol="A")
print(futures_inventory_em_df)
```

数据示例

```
        日期     库存     增减
0   2024-11-19  15522    NaN
1   2024-11-20  15522    0.0
2   2024-11-21  16322  800.0
3   2024-11-22  16902  580.0
4   2024-11-25  17139  237.0
..         ...    ...    ...
61  2025-02-21  38028    0.0
62  2025-02-24  38146  118.0
63  2025-02-25  38146    0.0
64  2025-02-26  37696 -450.0
65  2025-02-27  37696    0.0
[66 rows x 3 columns]
```
