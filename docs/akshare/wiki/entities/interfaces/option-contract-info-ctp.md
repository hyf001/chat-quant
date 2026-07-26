---
title: "option_contract_info_ctp - 期权合约信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_contract_info_ctp

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 期权合约信息
- 描述: openctp 期权合约信息
- 目标地址: http://openctp.cn/instruments.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期权合约信息

接口: option_contract_info_ctp

目标地址: http://openctp.cn/instruments.html

描述: openctp 期权合约信息

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 交易所ID   | object  | -  |
| 合约ID    | object  | -  |
| 合约名称    | object  | -  |
| 商品类别    | object  | -  |
| 品种ID    | object  | -  |
| 合约乘数    | int64   | -  |
| 最小变动价位  | float64 | -  |
| 做多保证金率  | float64 | -  |
| 做空保证金率  | float64 | -  |
| 做多保证金/手 | float64 | -  |
| 做空保证金/手 | float64 | -  |
| 开仓手续费率  | float64 | -  |
| 开仓手续费/手 | float64 | -  |
| 平仓手续费率  | float64 | -  |
| 平仓手续费/手 | float64 | -  |
| 平今手续费率  | float64 | -  |
| 平今手续费/手 | float64 | -  |
| 交割年份    | int64   | -  |
| 交割月份    | int64   | -  |
| 上市日期    | object  | -  |
| 最后交易日   | object  | -  |
| 交割日     | object  | -  |
| 标的合约ID  | object  | -  |
| 标的合约乘数  | int64   | -  |
| 期权类型    | object  | -  |
| 行权价     | float64 | -  |
| 合约状态    | object  | -  |

接口示例

```python
import akshare as ak

option_contract_info_ctp_df = ak.option_contract_info_ctp()
print(option_contract_info_ctp_df)
```

数据示例

```
       交易所ID     合约ID      合约名称 商品类别  ... 标的合约乘数  期权类型  行权价 合约状态
0      CFFEX  HO2511-C-2500   HO2511-C-2500    2  ...      1     1  2500.0     1
1      CFFEX  HO2511-C-2550   HO2511-C-2550    2  ...      1     1  2550.0     1
2      CFFEX  HO2511-C-2600   HO2511-C-2600    2  ...      1     1  2600.0     1
3      CFFEX  HO2511-C-2650   HO2511-C-2650    2  ...      1     1  2650.0     1
4      CFFEX  HO2511-C-2700   HO2511-C-2700    2  ...      1     1  2700.0     1
...      ...            ...             ...  ...  ...    ...   ...     ...   ...
18741   SZSE       90006532  创业板ETF沽12月3700    2  ...      1     2     3.7     1
18742   SZSE       90006533   创业板ETF购3月3700    2  ...      1     1     3.7     1
18743   SZSE       90006534   创业板ETF沽3月3700    2  ...      1     2     3.7     1
18744   SZSE       90006535   创业板ETF购6月3700    2  ...      1     1     3.7     1
18745   SZSE       90006536   创业板ETF沽6月3700    2  ...      1     2     3.7     1
[18746 rows x 27 columns]
```
