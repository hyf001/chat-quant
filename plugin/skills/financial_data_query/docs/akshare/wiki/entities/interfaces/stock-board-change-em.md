---
title: "stock_board_change_em - 板块异动详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_board_change_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 板块异动详情
- 描述: 东方财富-行情中心-当日板块异动详情
- 目标地址: https://quote.eastmoney.com/changes/
- 限量: 返回最近交易日的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 板块异动详情

接口: stock_board_change_em

目标地址: https://quote.eastmoney.com/changes/

描述: 东方财富-行情中心-当日板块异动详情

限量: 返回最近交易日的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称                  | 类型      | 描述        |
|---------------------|---------|-----------|
| 板块名称                | object  | -         |
| 涨跌幅                 | float64 | 注意单位: %   |
| 主力净流入               | float64 | 注意单位: 万元  |
| 板块异动总次数             | float64 | -         |
| 板块异动最频繁个股及所属类型-股票代码 | object  | -         |
| 板块异动最频繁个股及所属类型-股票名称 | object  | -         |
| 板块异动最频繁个股及所属类型-买卖方向 | object  | -         |
| 板块具体异动类型列表及出现次数     | object  | 返回具体异动的字典 |

接口示例

```python
import akshare as ak

stock_board_change_em_df = ak.stock_board_change_em()
print(stock_board_change_em_df)
```

数据示例

```
       板块名称  ...                                    板块具体异动类型列表及出现次数
0      融资融券  ...  [{'t': 8201, 'ct': 10821}, {'t': 8219, 'ct': 1...
1       深股通  ...  [{'t': 8219, 'ct': 4564}, {'t': 8201, 'ct': 38...
2      创业板综  ...  [{'t': 8201, 'ct': 5584}, {'t': 8203, 'ct': 40...
3       沪股通  ...  [{'t': 8219, 'ct': 4973}, {'t': 8201, 'ct': 27...
4      富时罗素  ...  [{'t': 8219, 'ct': 4654}, {'t': 8201, 'ct': 26...
..      ...  ...                                                ...
563    千金藤素  ...  [{'t': 8201, 'ct': 18}, {'t': 8219, 'ct': 13},...
564  同步磁阻电机  ...  [{'t': 8201, 'ct': 18}, {'t': 8219, 'ct': 18},...
565  第四代半导体  ...  [{'t': 8201, 'ct': 10}, {'t': 8203, 'ct': 10},...
566  光伏高速公路  ...  [{'t': 8219, 'ct': 17}, {'t': 8201, 'ct': 11},...
567    赛马概念  ...  [{'t': 8219, 'ct': 17}, {'t': 8203, 'ct': 10},...
[568 rows x 8 columns]
```
