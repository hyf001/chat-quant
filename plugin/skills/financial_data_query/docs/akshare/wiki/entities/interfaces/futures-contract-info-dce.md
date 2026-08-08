---
title: "futures_contract_info_dce - 大连商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_info_dce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 合约信息 > 大连商品交易所
- 描述: 大连商品交易所-数据中心-业务数据-交易参数-合约信息
- 目标地址: http://www.dce.com.cn/dce/channel/list/180.html
- 限量: 单次返回最近交易日的期货合约信息数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 大连商品交易所

接口: futures_contract_info_dce

目标地址: http://www.dce.com.cn/dce/channel/list/180.html

描述: 大连商品交易所-数据中心-业务数据-交易参数-合约信息

限量: 单次返回最近交易日的期货合约信息数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| 品种     | object  | -  |
| 合约代码   | object  | -  |
| 交易单位   | int64   | -  |
| 最小变动价位 | float64 | -  |
| 开始交易日  | object  | -  |
| 最后交易日  | object  | -  |
| 最后交割日  | object  | -  |

接口示例

```python
import akshare as ak

futures_contract_info_dce_df = ak.futures_contract_info_dce()
print(futures_contract_info_dce_df)
```

数据示例

```
    品种名称 合约  交易单位  最小变动价位  开始交易日 最后交易日   最后交割日
0     豆一  a2511    10     1.0  2024-11-15  2025-11-14  2025-11-19
1     豆一  a2601    10     1.0  2025-01-16  2026-01-15  2026-01-20
2     豆一  a2603    10     1.0  2025-03-17  2026-03-13  2026-03-18
3     豆一  a2605    10     1.0  2025-05-20  2026-05-19  2026-05-22
4     豆一  a2607    10     1.0  2025-07-15  2026-07-14  2026-07-17
..   ...    ...   ...     ...         ...         ...         ...
232   豆油  y2603    10     2.0  2025-03-17  2026-03-13  2026-03-18
233   豆油  y2605    10     2.0  2025-05-20  2026-05-19  2026-05-22
234   豆油  y2607    10     2.0  2025-07-15  2026-07-14  2026-07-17
235   豆油  y2608    10     2.0  2025-08-15  2026-08-14  2026-08-19
236   豆油  y2609    10     2.0  2025-09-15  2026-09-14  2026-09-17
[237 rows x 7 columns]
```
