---
title: "stock_lh_yyb_capital - 龙虎榜-营业部排行-资金实力最强"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lh_yyb_capital

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-营业部排行 > 龙虎榜-营业部排行-资金实力最强
- 描述: 龙虎榜-营业部排行-资金实力最强
- 目标地址: https://data.10jqka.com.cn/market/longhu/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 龙虎榜-营业部排行-资金实力最强

接口: stock_lh_yyb_capital

目标地址: https://data.10jqka.com.cn/market/longhu/

描述: 龙虎榜-营业部排行-资金实力最强

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型     | 描述  |
|----------|--------|-----|
| 序号       | int64  | -   |
| 营业部名称    | object | -   |
| 今日最高操作   | int64  | -   |
| 今日最高金额   | object | -   |
| 今日最高买入金额 | object | -   |
| 累计参与金额   | object | -   |
| 累计买入金额   | object | -   |

接口示例

```python
import akshare as ak

stock_lh_yyb_capital_df = ak.stock_lh_yyb_capital()
print(stock_lh_yyb_capital_df)
```

数据示例

```
      序号                         营业部名称  今日最高操作  今日最高金额 今日最高买入金额  累计参与金额  累计买入金额
0      1   华宝证券股份有限公司上海东大名路证券营业部  一线游资       5  14.72亿    7.35亿  20.32亿  10.18亿
1      2  东方证券股份有限公司上海松江区沪亭北路...  知名游资       2   8.98亿    4.49亿  10.80亿   5.40亿
2      3         华鑫证券有限责任公司上海分公司  一线游资       8   8.63亿    4.32亿  12.23亿   6.52亿
3      4        国泰君安证券股份有限公司成都双庆路证券...       2   8.00亿    4.00亿   9.77亿   4.88亿
4      5        东方证券股份有限公司上海静安区延平路证...       2   4.60亿    2.30亿   6.36亿   3.18亿
..   ...                           ...     ...     ...      ...     ...     ...
288  289        长江证券股份有限公司北京百万庄大街证券...       1   2.00万    2.00万   2.00万   2.00万
289  290          国联证券股份有限公司无锡中山路证券营业部       1   1.87万     0.00   1.87万    0.00
290  291        中信建投证券股份有限公司武汉建设八路证...       1   1.79万    1.79万   1.79万   1.79万
291  292          长江证券股份有限公司成都东大街证券营业部       1   1.74万     0.00   1.74万    0.00
292  293           中国银河证券股份有限公司德清证券营业部       1   1.21万     0.00   1.21万    0.00
[293 rows x 7 columns]
```
