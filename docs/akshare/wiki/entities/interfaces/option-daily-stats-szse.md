---
title: "option_daily_stats_szse - 每日统计-深圳证券交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_daily_stats_szse

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-三大交易所 > 每日统计-深圳证券交易所
- 描述: 深圳证券交易所-市场数据-期权数据-日度概况
- 目标地址: https://investor.szse.cn/market/option/day/index.html
- 限量: 单次返回指定 date 的数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 每日统计-深圳证券交易所

接口: option_daily_stats_szse

目标地址: https://investor.szse.cn/market/option/day/index.html

描述: 深圳证券交易所-市场数据-期权数据-日度概况

限量: 单次返回指定 date 的数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20240626"; 交易日 |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 合约标的代码   | object  | -       |
| 合约标的名称   | object  | -       |
| 成交量      | int64   | 注意单位: 张 |
| 认购成交量    | int64   | 注意单位: 张 |
| 认沽成交量    | int64   | 注意单位: 张 |
| 认沽/认购持仓比 | float64 | 注意单位: % |
| 未平仓合约总数  | int64   | 注意单位: 张 |
| 未平仓认购合约数 | int64   | 注意单位: 张 |
| 未平仓认沽合约数 | int64   | 注意单位: 张 |
| 交易日      | object  | -       |


接口示例

```python
import akshare as ak

option_daily_stats_szse_df = ak.option_daily_stats_szse(date="20240626")
print(option_daily_stats_szse_df)
```

数据示例

```
   合约标的代码 合约标的名称 成交量 认购成交量  ... 未平仓合约总数 未平仓认购合约数 未平仓认沽合约数  交易日
0  159901  深证100ETF    87949   47218  ...    89303     45316     43987  2024-06-26
1  159915    创业板ETF  1059560  578092  ...   772281    429029    343252  2024-06-26
2  159919  沪深300ETF   249020  122046  ...   178740     96555     82185  2024-06-26
3  159922  中证500ETF   313967  155196  ...   206706    113215     93491  2024-06-26
[4 rows x 10 columns]
```
