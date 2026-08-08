---
title: "stock_lh_yyb_most - 龙虎榜-营业部排行-上榜次数最多"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lh_yyb_most

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-营业部排行 > 龙虎榜-营业部排行-上榜次数最多
- 描述: 龙虎榜-营业部排行-上榜次数最多
- 目标地址: https://data.10jqka.com.cn/market/longhu/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 龙虎榜-营业部排行-上榜次数最多

接口: stock_lh_yyb_most

目标地址: https://data.10jqka.com.cn/market/longhu/

描述: 龙虎榜-营业部排行-上榜次数最多

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型     | 描述  |
|-----------|--------|-----|
| 序号        | int64  | -   |
| 营业部名称     | object | -   |
| 上榜次数      | int64  | -   |
| 合计动用资金    | object | -   |
| 年内上榜次数    | int64  | -   |
| 年内买入股票只数  | int64  | -   |
| 年内3日跟买成功率 | object | -   |

接口示例

```python
import akshare as ak

stock_lh_yyb_most_df = ak.stock_lh_yyb_most()
print(stock_lh_yyb_most_df)
```

数据示例

```
      序号                         营业部名称  上榜次数  ... 年内上榜次数  年内买入股票只数  年内3日跟买成功率
0      1  东方财富证券股份有限公司拉萨金融城南环...  一线游资    15  ...   3160      2369     41.40%
1      2  东方财富证券股份有限公司拉萨东环路第二...  一线游资    14  ...   4145      2978     43.94%
2      3  东方财富证券股份有限公司拉萨团结路第二...  一线游资    13  ...   3985      2856     43.21%
3      4        东方财富证券股份有限公司拉萨团结路第一...    13  ...   2685      1858     44.00%
4      5                   深股通专用  一线游资    11  ...   1780      1567     44.99%
..   ...                           ...   ...  ...    ...       ...        ...
288  289  华泰证券股份有限公司上海奉贤区望园南路...  跟风高手     1  ...     37        11    100.00%
289  290          华创证券有限责任公司贵阳北京路证券营业部     1  ...      4         1      无符合数据
290  291        中信建投证券股份有限公司东三环中路证券...     1  ...      4         1      无符合数据
291  292        国泰君安证券股份有限公司深圳福田中心区...     1  ...     43        24     48.00%
292  293         大同证券有限责任公司运城人民北路证券营业部     1  ...      1         1      无符合数据
[293 rows x 7 columns]
```
