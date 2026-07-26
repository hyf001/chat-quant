---
title: "stock_margin_detail_szse - 融资融券明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_detail_szse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 深圳证券交易所 > 融资融券明细
- 描述: 深证证券交易所-融资融券数据-融资融券交易明细数据
- 目标地址: https://www.szse.cn/disclosure/margin/margin/index.html
- 限量: 单次返回指定 date 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 融资融券明细

接口: stock_margin_detail_szse

目标地址: https://www.szse.cn/disclosure/margin/margin/index.html

描述: 深证证券交易所-融资融券数据-融资融券交易明细数据

限量: 单次返回指定 date 的所有历史数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20220118" |

输出参数

| 名称     | 类型     | 描述        |
|--------|--------|-----------|
| 证券代码   | object | -         |
| 证券简称   | object | -         |
| 融资买入额  | int64  | 注意单位: 元   |
| 融资余额   | int64  | 注意单位: 元   |
| 融券卖出量  | int64  | 注意单位: 股/份 |
| 融券余量   | int64  | 注意单位: 股/份 |
| 融券余额   | int64  | 注意单位: 元   |
| 融资融券余额 | int64  | 注意单位: 元   |

接口示例

```python
import akshare as ak

stock_margin_detail_sse_df = ak.stock_margin_detail_szse(date="20230925")
print(stock_margin_detail_sse_df)
```

数据示例

```
        证券代码   证券简称     融资买入额  ...     融券余量      融券余额      融资融券余额
0     000001   平安银行  67452975  ...  1791277  20098128  4365763792
1     000002  万  科Ａ  78869157  ...  6637572  87217696  4819262864
2     000006   深振业Ａ  11862407  ...   893154   4037056   471912480
3     000008   神州高铁   6467970  ...    37100     89411   264908600
4     000009   中国宝安   5545586  ...  2540168  26036723  1501197300
      ...    ...       ...  ...      ...       ...         ...
1806  301528    多浦乐   9457046  ...      600     52212    60245085
1807  301529   福赛科技  10576005  ...    67138   3056121    41545975
1808  301533   威马农机   1615519  ...     1000     43110    23167466
1809  301548  C崇德科技  23852209  ...        0         0    41105017
1810  301550   斯菱股份  17612051  ...     2300     98486    36562401
[1811 rows x 8 columns]
```
