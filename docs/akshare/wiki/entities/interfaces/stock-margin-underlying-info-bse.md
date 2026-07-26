---
title: "stock_margin_underlying_info_bse - 标的证券信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_underlying_info_bse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 北京证券交易所 > 标的证券信息
- 描述: 北京证券交易所-融资融券数据-标的证券信息
- 目标地址: https://www.bse.cn/disclosure/rzrq_bdzq_list.html
- 限量: 单次返回指定交易日的全部标的证券信息
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 标的证券信息

接口: stock_margin_underlying_info_bse

目标地址: https://www.bse.cn/disclosure/rzrq_bdzq_list.html

描述: 北京证券交易所-融资融券数据-标的证券信息

限量: 单次返回指定交易日的全部标的证券信息

输入参数

| 名称   | 类型  | 描述                    |
|------|-----|-----------------------|
| date | str | date="20260722"; 交易日期 |

输出参数

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| 证券代码  | object | -   |
| 证券简称  | object | -   |
| 融资标的  | object | -   |
| 融券标的  | object | -   |
| 当日可融资 | object | -   |
| 当日可融券 | object | -   |

接口示例

```python
import akshare as ak

stock_margin_underlying_info_bse_df = ak.stock_margin_underlying_info_bse(date="20260722")
print(stock_margin_underlying_info_bse_df)
```

数据示例

```
     证券代码  证券简称 融资标的 融券标的 当日可融资 当日可融券
0  920000  安徽凤凰    Y    Y     Y     Y
1  920001  纬达光电    Y    Y     Y     Y
2  920002  万达轴承    Y    Y     Y     Y
3  920003  中诚咨询    Y    Y     Y     Y
4  920005  鼎佳精密    Y    Y     Y     Y
```
