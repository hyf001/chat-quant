---
title: "option_daily_stats_sse - 每日统计-上海证券交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_daily_stats_sse

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-三大交易所 > 每日统计-上海证券交易所
- 描述: 上海证券交易所-产品-股票期权-每日统计
- 目标地址: http://www.sse.com.cn/assortment/options/date/
- 限量: 单次返回指定 date 的数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 每日统计-上海证券交易所

接口: option_daily_stats_sse

目标地址: http://www.sse.com.cn/assortment/options/date/

描述: 上海证券交易所-产品-股票期权-每日统计

限量: 单次返回指定 date 的数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20240626"; 交易日 |

输出参数

| 名称       | 类型           | 描述       |
|----------|--------------|----------|
| 合约标的代码   | object       | -        |
| 合约标的名称   | object       | -        |
| 合约数量     | int64        | -        |
| 总成交额     | int64        | 注意单位: 万元 |
| 总成交量     | int64        | 注意单位: 张  |
| 认购成交量    | int64        | 注意单位: 张  |
| 认沽成交量    | int64        | 注意单位: 张  |
| 认沽/认购    | float64      | 注意单位: %  |
| 未平仓合约总数  | int64        | -        |
| 未平仓认购合约数 | floaint64t64 | -        |
| 未平仓认沽合约数 | int64        | -        |

接口示例

```python
import akshare as ak

option_daily_stats_sse_df = ak.option_daily_stats_sse(date="20240626")
print(option_daily_stats_sse_df)
```

数据示例

```
   合约标的代码 合约标的名称 合约数量 总成交额  ... 未平仓合约总数  未平仓认购合约数  未平仓认沽合约数   交易日
0  510050   上证50ETF   126   47808  ...  1162840    623212    539628  2024-06-26
1  510300  沪深300ETF   126   60857  ...   963032    540989    422043  2024-06-26
2  510500  中证500ETF   178  127869  ...   803581    434857    368724  2024-06-26
3  588000   科创50ETF    92   15273  ...   790569    526095    264474  2024-06-26
4  588080  科创板50ETF    92    7633  ...   377438    232943    144495  2024-06-26
[5 rows x 12 columns]
```
