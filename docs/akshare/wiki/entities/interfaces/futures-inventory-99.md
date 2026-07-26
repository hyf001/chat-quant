---
title: "futures_inventory_99 - 库存数据-99期货网"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_inventory_99

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 库存数据-99期货网
- 描述: 99 期货网-大宗商品库存数据
- 目标地址: https://www.99qh.com/data/stockIn?productId=61
- 限量: 单次返回指定 symbol 的具体品种的期货库存数据, 仓单日报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 库存数据-99期货网

接口: futures_inventory_99

目标地址: https://www.99qh.com/data/stockIn?productId=61

描述: 99 期货网-大宗商品库存数据

限量: 单次返回指定 symbol 的具体品种的期货库存数据, 仓单日报数据

输入参数

| 名称     | 类型  | 描述                                                                                                     |
|--------|-----|--------------------------------------------------------------------------------------------------------|
| symbol | str | symbol='豆一'; 交易所对应的具体品种中文名称或者英文代码; 如：大连商品交易所的豆一; 具体品种查询：https://www.99qh.com/data/stockIn?productId=61 |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 日期  | object  | -  |
| 收盘价 | float64 | -  |
| 库存  | int64   | -  |

接口示例

```python
import akshare as ak

futures_inventory_99_df = ak.futures_inventory_99(symbol='豆一')
print(futures_inventory_99_df)
```

数据示例

```
         日期     收盘价     库存
0     2005-01-14  3000.0  13107
1     2005-01-21  2627.0  22695
2     2005-01-28  2631.0  25031
3     2005-02-04  2637.0  20023
4     2005-02-18  2680.0  18454
...          ...     ...    ...
4014  2025-02-27  4232.0  37696
4015  2025-02-28  4218.0  37696
4016  2025-03-03  4239.0  37536
4017  2025-03-04  4252.0  37536
4018  2025-03-05  4175.0  37536
[4019 rows x 3 columns]
```
