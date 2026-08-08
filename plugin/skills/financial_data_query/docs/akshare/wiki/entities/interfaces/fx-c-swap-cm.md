---
title: "fx_c_swap_cm - 外汇掉期 C-Swap 定盘曲线"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# fx_c_swap_cm

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 外汇掉期 C-Swap 定盘曲线
- 描述: 中国外汇交易中心暨全国银行间同业拆借中心-基准-外汇市场-外汇掉期曲线-外汇掉期 C-Swap 定盘曲线
- 目标地址: https://www.chinamoney.org.cn/chinese/bkcurvfsw
- 限量: 单次返回所有行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 外汇掉期 C-Swap 定盘曲线

接口: fx_c_swap_cm

目标地址: https://www.chinamoney.org.cn/chinese/bkcurvfsw

描述: 中国外汇交易中心暨全国银行间同业拆借中心-基准-外汇市场-外汇掉期曲线-外汇掉期 C-Swap 定盘曲线

限量: 单次返回所有行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型      | 描述 |
|-----------|---------|----|
| 日期时间      | object  | -  |
| 期限品种      | object  | -  |
| 掉期点(Pips) | float64 | -  |
| 掉期点数据源    | object  |    |
| 全价汇率      | float64 |    |

接口示例

```python
import akshare as ak

fx_c_swap_cm_df = ak.fx_c_swap_cm()
print(fx_c_swap_cm_df)
```

数据示例

```
         日期时间 期限品种  掉期点(Pips) 掉期点数据源    全价汇率
0   2025-09-26 16:30:00.0   ON     -15.00   报价数据  7.1374
1   2025-09-26 16:30:00.0   TN      -4.75   报价数据  7.1359
2   2025-09-26 16:30:00.0   SN     -16.74   报价数据  7.1337
3   2025-09-26 16:30:00.0   1W     -16.74   报价数据  7.1337
4   2025-09-26 16:30:00.0   2W     -41.80   报价数据  7.1312
5   2025-09-26 16:30:00.0   3W     -76.05   报价数据  7.1278
6   2025-09-26 16:30:00.0   1M    -122.74   报价数据  7.1231
7   2025-09-26 16:30:00.0   2M    -239.50   报价数据  7.1115
8   2025-09-26 16:30:00.0   3M    -373.75   报价数据  7.0980
9   2025-09-26 16:30:00.0   6M    -706.75   报价数据  7.0647
10  2025-09-26 16:30:00.0   9M   -1030.50   报价数据  7.0324
11  2025-09-26 16:30:00.0   1Y   -1337.01   报价数据  7.0017
```
