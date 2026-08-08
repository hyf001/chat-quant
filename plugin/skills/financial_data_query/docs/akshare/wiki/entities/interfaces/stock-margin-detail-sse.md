---
title: "stock_margin_detail_sse - 融资融券明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_detail_sse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 上海证券交易所 > 融资融券明细
- 描述: 上海证券交易所-融资融券数据-融资融券明细数据
- 目标地址: http://www.sse.com.cn/market/othersdata/margin/detail/
- 限量: 单次返回交易日的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 融资融券明细

接口: stock_margin_detail_sse

目标地址: http://www.sse.com.cn/market/othersdata/margin/detail/

描述: 上海证券交易所-融资融券数据-融资融券明细数据

限量: 单次返回交易日的所有历史数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20210205" |

输出参数

| 名称     | 类型     | 描述      |
|--------|--------|---------|
| 信用交易日期 | object | -       |
| 标的证券代码 | object | -       |
| 标的证券简称 | object | -       |
| 融资余额   | int64  | 注意单位: 元 |
| 融资买入额  | int64  | 注意单位: 元 |
| 融资偿还额  | int64  | 注意单位: 元 |
| 融券余量   | int64  | -       |
| 融券卖出量  | int64  | -       |
| 融券偿还量  | int64  | -       |

接口示例

```python
import akshare as ak

stock_margin_detail_sse_df = ak.stock_margin_detail_sse(date="20230922")
print(stock_margin_detail_sse_df)
```

数据示例

```
      信用交易日期  标的证券代码   标的证券简称  ...  融券余量 融券卖出量  融券偿还量
0     20230922  510050    50ETF  ...  31081200  21114800  11402100
1     20230922  510100  SZ50ETF  ...         0         0         0
2     20230922  510150    消费ETF  ...         0         0         0
3     20230922  510180   180ETF  ...    409300    173200    130900
4     20230922  510210    综指ETF  ...         0         0         0
        ...     ...      ...  ...       ...       ...       ...
1735  20230922  688799     华纳药厂  ...         0         0         0
1736  20230922  688800      瑞可达  ...    124592      3617     21777
1737  20230922  688819     天能股份  ...   1231449     75962      3000
1738  20230922  688981     中芯国际  ...   4747379    389501    606169
1739  20230922  689009     九号公司  ...  11236510    112012     27234
[1740 rows x 9 columns]
```
