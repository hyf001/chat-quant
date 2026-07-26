---
title: "stock_hold_change_cninfo - 股本变动"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hold_change_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 股本变动
- 描述: 巨潮资讯-数据中心-专题统计-股东股本-股本变动
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次指定 symbol 的股本变动数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 股本变动

接口: stock_hold_change_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-股东股本-股本变动

限量: 单次指定 symbol 的股本变动数据

输入参数

| 名称     | 类型  | 描述                                                               |
|--------|-----|------------------------------------------------------------------|
| symbol | str | symbol="全部"; choice of {"深市主板", "沪市", "创业板", "科创板", "北交所", "全部"} |

输出参数

| 名称     | 类型      | 描述     |
|--------|---------|--------|
| 证券代码   | object  | -      |
| 证券简称   | object  | -      |
| 交易市场   | object  | -      |
| 公告日期   | object  | -      |
| 变动日期   | object  | -      |
| 变动原因   | object  | -      |
| 总股本    | float64 | 单位: 万股 |
| 已流通股份  | float64 | 单位: 万股 |
| 已流通比例  | float64 | 单位: %  |
| 流通受限股份 | float64 | 单位: 万股 |

接口示例

```python
import akshare as ak

stock_hold_change_cninfo_df = ak.stock_hold_change_cninfo(symbol="全部")
print(stock_hold_change_cninfo_df)
```

数据示例

```
      证券代码   证券简称   交易市场  ...   已流通股份  已流通比例  流通受限股份
0     000001   平安银行  深交所主板  ...  1940561.75  100.00     30.07
1     000002  万  科Ａ  深交所主板  ...  1192344.88   99.94    726.07
2     000004   国华网安  深交所主板  ...    12628.81   95.40    609.22
3     000006   深振业Ａ  深交所主板  ...   134998.74  100.00      0.77
4     000007    全新好  深交所主板  ...    34644.80  100.00       NaN
...      ...    ...    ...  ...         ...     ...       ...
5463  920106   林泰新材    北交所  ...     1210.57   31.04   2689.43
5464  920111   聚星科技    北交所  ...     3688.85   23.78  11826.60
5465  920116   星图测控    北交所  ...     2612.50   23.75   8387.50
5466  920118   太湖远大    北交所  ...     1379.50   27.10   3710.10
5467  920128   胜业电气    北交所  ...     1710.00   21.06   6409.00
[5468 rows x 10 columns]
```
