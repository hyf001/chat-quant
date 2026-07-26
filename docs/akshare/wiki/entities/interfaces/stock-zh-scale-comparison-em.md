---
title: "stock_zh_scale_comparison_em - 公司规模"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_scale_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 同行比较 > 公司规模
- 描述: 东方财富-行情中心-同行比较-公司规模
- 目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gsgm
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 公司规模

接口: stock_zh_scale_comparison_em

目标地址: https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gsgm

描述: 东方财富-行情中心-同行比较-公司规模

限量: 单次返回全部数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="SZ000895"     |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| 代码     | object  | -  |
| 简称     | object  | -  |
| 总市值    | float64 | -  |
| 总市值排名  | int64   | -  |
| 流通市值   | float64 | -  |
| 流通市值排名 | int64   | -  |
| 营业收入   | float64 | -  |
| 营业收入排名 | int64   | -  |
| 净利润    | float64 | -  |
| 净利润排名  | int64   | -  |

接口示例

```python
import akshare as ak

stock_zh_scale_comparison_em_df = ak.stock_zh_scale_comparison_em(symbol="SZ000895")
print(stock_zh_scale_comparison_em_df)
```

数据示例

```
       代码    简称           总市值  总市值排名    流通市值  流通市值排名          营业收入  营业收入排名           净利润  净利润排名
0  000895  双汇发展  8.685906e+10      5  868.48       4  2.850309e+10       3  2.351218e+09      4
```
