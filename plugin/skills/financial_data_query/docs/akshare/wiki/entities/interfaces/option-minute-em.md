---
title: "option_minute_em - 期权行情分时数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_minute_em

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 期权行情分时数据-东财
- 描述: 东方财富网-行情中心-期权市场-分时行情
- 目标地址: https://wap.eastmoney.com/quote/stock/151.cu2404P61000.html
- 限量: 单次返回指定 symbol 的分时行情数据; 只能获取近期合约的数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期权行情分时数据-东财

接口: option_minute_em

目标地址: https://wap.eastmoney.com/quote/stock/151.cu2404P61000.html

描述: 东方财富网-行情中心-期权市场-分时行情

限量: 单次返回指定 symbol 的分时行情数据; 只能获取近期合约的数据

输入参数

| 名称     | 类型  | 描述                                                       |
|--------|-----|----------------------------------------------------------|
| symbol | str | symbol="MO2402-C-5400"; 通过 **ak.option_current_em()** 获取 |

输出参数

| 名称     | 类型     | 描述      |
|--------|--------|---------|
| time   | object | -       |
| close  | int64  | -       |
| high   | int64  | -       |
| low    | int64  | -       |
| volume | int64  | 注意单位: 手 |
| amount | int64  | -       |

接口示例

```python
import akshare as ak

option_minute_em_df = ak.option_minute_em(symbol="MO2402-C-5400")
print(option_minute_em_df)
```

数据示例

```
                 time  close  high   low  volume    amount
0    2024-01-31 09:30   16.4  16.4  16.4       0       0.0
1    2024-01-31 09:31   20.8  21.6  16.2     103  193580.0
2    2024-01-31 09:32   20.8  21.6  20.0      63  130940.0
3    2024-01-31 09:33   21.2  21.8  20.4      97  206420.0
4    2024-01-31 09:34   21.0  21.0  20.0      63  130580.0
..                ...    ...   ...   ...     ...       ...
236  2024-01-31 14:56    9.2   9.8   9.2      19   18060.0
237  2024-01-31 14:57    9.4   9.4   9.2      25   23380.0
238  2024-01-31 14:58    9.4   9.4   9.4       0       0.0
239  2024-01-31 14:59    9.4   9.4   9.4       0       0.0
240  2024-01-31 15:00    9.2   9.2   9.2      64   92200.0
[241 rows x 6 columns]
```
