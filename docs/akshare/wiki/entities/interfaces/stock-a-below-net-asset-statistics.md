---
title: "stock_a_below_net_asset_statistics - 破净股统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_a_below_net_asset_statistics

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 破净股统计
- 描述: 乐咕乐股-A 股破净股统计数据
- 目标地址: https://www.legulegu.com/stockdata/below-net-asset-statistics
- 限量: 单次获取指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 破净股统计

接口: stock_a_below_net_asset_statistics

目标地址: https://www.legulegu.com/stockdata/below-net-asset-statistics

描述: 乐咕乐股-A 股破净股统计数据

限量: 单次获取指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                          |
|--------|-----|-------------------------------------------------------------|
| symbol | str | symbol="全部A股"; choice of {"全部A股", "沪深300", "上证50", "中证500"} |

说明:

- 当前源站返回字段为驼峰命名, 且 `date` 为日期字符串, 接口内部已完成兼容处理
- 对外输出列仍保持为 `date`, `below_net_asset`, `total_company`, `below_net_asset_ratio`

输出参数-全部A股

| 名称                    | 类型      | 描述    |
|-----------------------|---------|-------|
| date                  | object  | 交易日   |
| below_net_asset       | float64 | 破净股家数 |
| total_company         | float64 | 总公司数  |
| below_net_asset_ratio | float64 | 破净股比率 |

接口示例-全部 A 股

```python
import akshare as ak

stock_a_below_net_asset_statistics_df = ak.stock_a_below_net_asset_statistics(symbol="全部A股")
print(stock_a_below_net_asset_statistics_df)
```

数据示例-全部 A 股

```
            date  below_net_asset  total_company  below_net_asset_ratio
0     2005-01-05               36           1352                 0.0266
1     2005-01-06               31           1352                 0.0229
2     2005-01-07               32           1352                 0.0237
3     2005-01-10               33           1352                 0.0244
4     2005-01-11               29           1352                 0.0214
          ...              ...            ...                    ...
4682  2024-04-21              577           5114                 0.1128
4683  2024-04-22              561           5114                 0.1097
4684  2024-04-23              551           5114                 0.1077
4685  2024-04-24              533           5114                 0.1042
4686  2024-04-25              516           5113                 0.1009
[4687 rows x 4 columns]
```

输出参数-沪深 300

| 名称                    | 类型      | 描述    |
|-----------------------|---------|-------|
| date                  | object  | 交易日   |
| below_net_asset       | float64 | 破净股家数 |
| total_company         | float64 | 总公司数  |
| below_net_asset_ratio | float64 | 破净股比率 |

接口示例-沪深 300

```python
import akshare as ak

stock_a_below_net_asset_statistics_df = ak.stock_a_below_net_asset_statistics(symbol="沪深300")
print(stock_a_below_net_asset_statistics_df)
```

数据示例-沪深 300

```
            date  below_net_asset  total_company  below_net_asset_ratio
0     2005-04-08               22            299                 0.0736
1     2005-04-11               21            299                 0.0702
2     2005-04-12               23            299                 0.0769
3     2005-04-13               20            299                 0.0669
4     2005-04-14               22            299                 0.0736
          ...              ...            ...                    ...
4627  2024-04-21               63            300                 0.2100
4628  2024-04-22               63            300                 0.2100
4629  2024-04-23               63            300                 0.2100
4630  2024-04-24               63            300                 0.2100
4631  2024-04-25               62            300                 0.2067
[4632 rows x 4 columns]
```
