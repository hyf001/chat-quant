---
title: "stock_lhb_ggtj_sina - 龙虎榜-个股上榜统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_ggtj_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 龙虎榜-个股上榜统计
- 描述: 新浪财经-龙虎榜-个股上榜统计
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 龙虎榜-个股上榜统计

接口: stock_lhb_ggtj_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml

描述: 新浪财经-龙虎榜-个股上榜统计

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                                |
|--------|-----|-----------------------------------------------------------------------------------|
| symbol | str | symbol="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;} |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 股票代码  | object  | -       |
| 股票名称  | object  | -       |
| 上榜次数  | int64   | -       |
| 累积购买额 | float64 | 注意单位: 万 |
| 累积卖出额 | float64 | 注意单位: 万 |
| 净额    | float64 | 注意单位: 万 |
| 买入席位数 | int64   | -       |
| 卖出席位数 | int64   | -       |

接口示例

```python
import akshare as ak

stock_lhb_ggtj_sina_df = ak.stock_lhb_ggtj_sina(symbol="5")
print(stock_lhb_ggtj_sina_df)
```

数据示例

```
     股票代码 股票名称  上榜次数  累积购买额   累积卖出额   净额  买入席位数  卖出席位数
0    300364  中文在线     2  171289.25   97538.13   73751.12      9      9
1    000001  平安银行     1  126080.24   64719.50   61360.74      5      4
2    002673  西部证券     1   22404.44    8677.21   13727.22      5      4
3    601595  上海电影     1   26953.47   13537.77   13415.70      3      4
4    601136  首创证券     2   50349.55   37874.81   12474.74      9      7
..      ...   ...   ...        ...        ...        ...    ...    ...
310  001314  亿道信息     4   27524.67   46756.32  -19231.65     13     10
311  300502   新易盛     1  122834.08  142750.78  -19916.70      5      5
312  002229  鸿博股份     2  116669.40  137884.32  -21214.92     10      9
313  000628  高新发展     4  372969.77  421664.91  -48695.14     14     15
314  603259  药明康德     1   66436.38  248845.50 -182409.12      5      3
[315 rows x 8 columns]
```
