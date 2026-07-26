---
title: "stock_lh_yyb_control - 龙虎榜-营业部排行-抱团操作实力"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lh_yyb_control

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-营业部排行 > 龙虎榜-营业部排行-抱团操作实力
- 描述: 龙虎榜-营业部排行-抱团操作实力
- 目标地址: https://data.10jqka.com.cn/market/longhu/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 龙虎榜-营业部排行-抱团操作实力

接口: stock_lh_yyb_control

目标地址: https://data.10jqka.com.cn/market/longhu/

描述: 龙虎榜-营业部排行-抱团操作实力

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
| 携手营业部家数   | int64  | -   |
| 年内最佳携手对象  | object | -   |
| 年内最佳携手股票数 | int64  | -   |
| 年内最佳携手成功率 | object | -   |

接口示例

```python
import akshare as ak

stock_lh_yyb_control_df = ak.stock_lh_yyb_control()
print(stock_lh_yyb_control_df)
```

数据示例

```
      序号                         营业部名称  ...  年内最佳携手股票数 年内最佳携手成功率
0      1                   深股通专用  一线游资  ...        207    50.73%
1      2  东方财富证券股份有限公司拉萨金融城南环...  一线游资  ...        240    42.44%
2      3  东方财富证券股份有限公司拉萨团结路第二...  一线游资  ...        241    46.86%
3      4        东方财富证券股份有限公司拉萨团结路第一...  ...        241    46.86%
4      5  东方财富证券股份有限公司拉萨东环路第二...  一线游资  ...        241    46.03%
..   ...                           ...  ...        ...       ...
263  264         海通证券股份有限公司常熟海虞北路证券营业部  ...          1     无符合数据
264  265          兴业证券股份有限公司福州湖东路证券营业部  ...          4     无符合数据
265  266         光大证券股份有限公司贵阳长岭北路证券营业部  ...          2     无符合数据
266  267        华泰证券股份有限公司深圳平安金融中心证...  ...          3     无符合数据
267  268               中信证券股份有限公司深圳分公司  ...          4     无符合数据
[268 rows x 6 columns]
```
