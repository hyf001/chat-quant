---
title: "stock_zh_valuation_comparison_em - 估值比较"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_valuation_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 同行比较 > 估值比较
- 描述: 东方财富-行情中心-同行比较-估值比较
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gzbj
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 估值比较

接口: stock_zh_valuation_comparison_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gzbj

描述: 东方财富-行情中心-同行比较-估值比较

限量: 单次返回全部数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="SZ000895"     |

输出参数

| 名称            | 类型      | 描述 |
|---------------|---------|----|
| 排名            | object  | -  |
| 代码            | object  | -  |
| 简称            | object  | -  |
| PEG           | float64 | -  |
| 市盈率-24A       | float64 | -  |
| 市盈率-TTM       | float64 | -  |
| 市盈率-25E       | float64 | -  |
| 市盈率-26E       | float64 | -  |
| 市盈率-27E       | float64 | -  |
| 市销率-24A       | float64 | -  |
| 市销率-TTM       | float64 | -  |
| 市销率-25E       | float64 | -  |
| 市销率-26E       | float64 | -  |
| 市销率-27E       | float64 | -  |
| 市净率-24A       | float64 | -  |
| 市净率-MRQ       | float64 | -  |
| 市现率1-24A      | float64 | -  |
| 市现率1-TTM      | float64 | -  |
| 市现率2-24A      | float64 | -  |
| 市现率2-TTM      | float64 | -  |
| EV/EBITDA-24A | float64 | -  |

接口示例

```python
import akshare as ak

stock_zh_valuation_comparison_em_df = ak.stock_zh_valuation_comparison_em(symbol="SZ000895")
print(stock_zh_valuation_comparison_em_df)
```

数据示例

```
         排名      代码    简称  ...     市现率2-24A     市现率2-TTM  EV/EBITDA-24A
0  42.0/120  000895  双汇发展  ...    29.790457 -1045.264127      12.503574
1       nan    行业平均  行业平均  ...  1036.299305   -81.550319      12.794686
2       nan    行业中值  行业中值  ...   -11.801449   -13.610393      18.565517
3       1.0  920786  骑士乳业  ...   -10.676185   -23.320786      14.613055
4       2.0  002852   道道全  ...    94.382638   -14.822839      10.933433
5       3.0  002840  华统股份  ...   -62.597528    39.150932      19.671557
6       4.0  605077  华康股份  ...    -2.588921   -50.802629      15.723042
7       5.0  002286   保龄宝  ...   257.860564  -114.930447      12.453163
[8 rows x 20 columns]
```
