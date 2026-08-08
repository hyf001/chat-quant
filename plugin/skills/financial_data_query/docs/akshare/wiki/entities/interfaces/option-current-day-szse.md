---
title: "option_current_day_szse - 当日合约-深圳证券交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_current_day_szse

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-三大交易所 > 当日合约-深圳证券交易所
- 描述: 深圳证券交易所-期权子网-行情数据-当日合约
- 目标地址: https://www.sse.org.cn/option/quotation/contract/daycontract/index.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 当日合约-深圳证券交易所

接口: option_current_day_szse

目标地址: https://www.sse.org.cn/option/quotation/contract/daycontract/index.html

描述: 深圳证券交易所-期权子网-行情数据-当日合约

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称           | 类型      | 描述 |
|--------------|---------|----|
| 序号           | int64   | -  |
| 合约编码         | int64   | -  |
| 合约代码         | object  | -  |
| 合约简称         | object  | -  |
| 标的证券简称(代码)   | object  | -  |
| 合约类型         | object  | -  |
| 行权价          | float64 | -  |
| 合约单位         | int64   | -  |
| 最后交易日        | object  | -  |
| 行权日          | object  | -  |
| 到期日          | object  | -  |
| 交收日          | object  | -  |
| 新挂           | object  | -  |
| 涨停价格         | float64 | -  |
| 跌停价格         | float64 | -  |
| 前结算价         | float64 | -  |
| 合约调整         | object  | -  |
| 停牌           | object  | -  |
| 合约总持仓        | float64 | -  |
| 挂牌原因         | object  | -  |
| 原合约代码        | object  | -  |
| 原合约简称        | object  | -  |
| 原行权价格        | float64 | -  |
| 原合约单位        | int64   | -  |
| 合约到期剩余交易天数   | int64   | -  |
| 合约到期剩余自然天数   | int64   | -  |
| 下次合约调整剩余交易天数 | int64   | -  |
| 下次合约调整剩余自然天数 | int64   | -  |
| 交易日期         | object  | -  |

接口示例

```python
import akshare as ak

option_current_day_szse_df = ak.option_current_day_szse()
print(option_current_day_szse_df)
```

数据示例

```
      序号 合约编码   合约代码  ... 下次合约调整剩余交易天数 下次合约调整剩余自然天数 交易日期
0      1  90005043  159901C2509M002500  ...            0            0  2025-09-12
1      2  90005044  159901C2509M002550  ...            0            0  2025-09-12
2      3  90005045  159901C2509M002600  ...            0            0  2025-09-12
3      4  90005046  159901C2509M002650  ...            0            0  2025-09-12
4      5  90005047  159901C2509M002700  ...            0            0  2025-09-12
..   ...       ...                 ...  ...          ...          ...         ...
651  652  90006280  159915P2510M003400  ...            0            0  2025-09-12
652  653  90006281  159915C2512M003400  ...            0            0  2025-09-12
653  654  90006282  159915P2512M003400  ...            0            0  2025-09-12
654  655  90006283  159915C2603M003400  ...            0            0  2025-09-12
655  656  90006284  159915P2603M003400  ...            0            0  2025-09-12
[656 rows x 29 columns]
```
