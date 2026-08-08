---
title: "stock_margin_detail_bse - 融资融券明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_detail_bse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 北京证券交易所 > 融资融券明细
- 描述: 北京证券交易所-融资融券数据-融资融券交易明细数据
- 目标地址: https://www.bse.cn/disclosure/rzrq_trans_list.html
- 限量: 单次返回指定交易日的全部明细数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 融资融券明细

接口: stock_margin_detail_bse

目标地址: https://www.bse.cn/disclosure/rzrq_trans_list.html

描述: 北京证券交易所-融资融券数据-融资融券交易明细数据

限量: 单次返回指定交易日的全部明细数据

输入参数

| 名称   | 类型  | 描述                    |
|------|-----|-----------------------|
| date | str | date="20260721"; 交易日期 |

输出参数

| 名称     | 类型     | 描述      |
|--------|--------|---------|
| 证券代码   | object | -       |
| 证券简称   | object | -       |
| 融资买入额  | int64  | 注意单位: 元 |
| 融资余额   | int64  | 注意单位: 元 |
| 融券卖出量  | int64  | 注意单位: 股 |
| 融券余量   | int64  | 注意单位: 股 |
| 融券余额   | int64  | 注意单位: 元 |
| 融资融券余额 | int64  | 注意单位: 元 |

接口示例

```python
import akshare as ak

stock_margin_detail_bse_df = ak.stock_margin_detail_bse(date="20260721")
print(stock_margin_detail_bse_df)
```

数据示例

```
     证券代码  证券简称    融资买入额      融资余额  融券卖出量  融券余量  融券余额   融资融券余额
0  920000  安徽凤凰   840755   9269780      0     0     0   9269780
1  920001  纬达光电   893619  15053483      0     0     0  15053483
2  920002  万达轴承  3293111  41220315      0     0     0  41220315
3  920003  中诚咨询    91099   5146247      0     0     0   5146247
4  920005  鼎佳精密    72870  17284516      0     0     0  17284516
```
