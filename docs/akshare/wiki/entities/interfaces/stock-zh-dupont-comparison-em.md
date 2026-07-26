---
title: "stock_zh_dupont_comparison_em - 杜邦分析比较"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_dupont_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 同行比较 > 杜邦分析比较
- 描述: 东方财富-行情中心-同行比较-杜邦分析比较
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/dbfxbj
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 杜邦分析比较

接口: stock_zh_dupont_comparison_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/dbfxbj

描述: 东方财富-行情中心-同行比较-杜邦分析比较

限量: 单次返回全部数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="SZ000895"     |

输出参数

| 名称          | 类型      | 描述 |
|-------------|---------|----|
| 代码          | object  | -  |
| 简称          | object  | -  |
| ROE-3年平均    | float64 | -  |
| ROE-22A     | float64 | -  |
| ROE-23A     | float64 | -  |
| ROE-24A     | float64 | -  |
| 净利率-3年平均    | float64 | -  |
| 净利率-22A     | float64 | -  |
| 净利率-23A     | float64 | -  |
| 净利率-24A     | float64 | -  |
| 总资产周转率-3年平均 | float64 | -  |
| 总资产周转率-22A  | float64 | -  |
| 总资产周转率-23A  | float64 | -  |
| 总资产周转率-24A  | float64 | -  |
| 权益乘数-3年平均   | float64 | -  |
| 权益乘数-22A    | float64 | -  |
| 权益乘数-23A    | float64 | -  |
| 权益乘数-24A    | float64 | -  |
| ROE-3年平均排名  | float64 | -  |


接口示例

```python
import akshare as ak

stock_zh_dupont_comparison_em_df = ak.stock_zh_dupont_comparison_em(symbol="SZ000895")
print(stock_zh_dupont_comparison_em_df)
```

数据示例

```
    代码    简称  ROE-3年平均  ROE-22A  ...  权益乘数-22A  权益乘数-23A  权益乘数-24A  ROE-3年平均排名
0    行业平均  行业平均      5.70     5.51  ...    191.76    189.10   185.080         NaN
1    行业中值  行业中值      7.71     7.89  ...    149.35    142.50   143.105         NaN
2  605499  东鹏饮料     38.09    30.97  ...    234.37    232.62   294.820         1.0
3  002847  盐津铺子     36.48    30.03  ...    213.82    196.34   203.650         2.0
4  000895  双汇发展     24.21    25.17  ...    164.15    173.44   174.840         3.0
5  603262  技源集团     24.02    28.06  ...    152.21    132.11   125.360         4.0
6  603288  海天味业     22.24    24.89  ...    126.69    132.34   130.110         5.0
7  000848  承德露露     21.92    23.53  ...    136.51    133.85   133.510         6.0
[8 rows x 19 columns]
```
