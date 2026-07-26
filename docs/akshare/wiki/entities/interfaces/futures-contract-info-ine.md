---
title: "futures_contract_info_ine - 上海国际能源交易中心"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_info_ine

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 合约信息 > 上海国际能源交易中心
- 描述: 上海国际能源交易中心-业务指南-交易参数汇总(期货)
- 目标地址: https://www.ine.cn/bourseService/summary/?name=currinstrumentprop
- 限量: 单次返回指定 date 的期货合约信息数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海国际能源交易中心

接口: futures_contract_info_ine

目标地址: https://www.ine.cn/bourseService/summary/?name=currinstrumentprop

描述: 上海国际能源交易中心-业务指南-交易参数汇总(期货)

限量: 单次返回指定 date 的期货合约信息数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20241129"; 交易日 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 合约代码  | object  | -  |
| 上市日   | object  | -  |
| 到期日   | object  | -  |
| 开始交割日 | object  | -  |
| 最后交割日 | object  | -  |
| 挂牌基准价 | float64 | -  |
| 交易日   | object  | -  |

接口示例

```python
import akshare as ak

futures_contract_info_ine_df = ak.futures_contract_info_ine(date="20241129")
print(futures_contract_info_ine_df)
```

数据示例

```
    合约代码  上市日       到期日      开始交割日    最后交割日   挂牌基准价    交易日
0   sc2412  2021-12-01  2024-11-29  2024-12-02  2024-12-06   420.0  2024-11-29
1   sc2501  2024-01-02  2024-12-31  2025-01-06  2025-01-10   551.7  2024-11-29
2   sc2502  2024-02-01  2025-01-31  2025-02-03  2025-02-07   567.2  2024-11-29
3   sc2503  2022-03-01  2025-02-28  2025-03-03  2025-03-07   494.0  2024-11-29
4   sc2504  2024-04-01  2025-03-31  2025-04-01  2025-04-07   593.4  2024-11-29
..     ...         ...         ...         ...         ...     ...         ...
57  ec2502  2024-02-27  2025-02-24  2025-02-24  2025-02-24  1359.8  2024-11-29
58  ec2504  2024-04-30  2025-04-28  2025-04-28  2025-04-28  2158.3  2024-11-29
59  ec2506  2024-06-25  2025-06-30  2025-06-30  2025-06-30  2403.8  2024-11-29
60  ec2508  2024-08-27  2025-08-25  2025-08-25  2025-08-25  1509.4  2024-11-29
61  ec2510  2024-10-29  2025-10-27  2025-10-27  2025-10-27  1920.9  2024-11-29
[62 rows x 7 columns]
```
