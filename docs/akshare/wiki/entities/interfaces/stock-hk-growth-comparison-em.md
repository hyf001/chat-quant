---
title: "stock_hk_growth_comparison_em - 成长性对比"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_growth_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 行业对比 > 成长性对比
- 描述: 东方财富-港股-行业对比-成长性对比
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 成长性对比

接口: stock_hk_growth_comparison_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison

描述: 东方财富-港股-行业对比-成长性对比

限量: 单次返回全部数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="03900" |

输出参数

| 名称                  | 类型      | 描述 |
|---------------------|---------|----|
| 代码                  | object  | -  |
| 简称                  | object  | -  |
| 基本每股收益同比增长率         | float64 | -  |
| 基本每股收益同比增长率排名       | int64   | -  |
| 营业收入同比增长率           | float64 | -  |
| 营业收入同比增长率排名         | int64   | -  |
| 营业利润率同比增长率          | float64 | -  |
| 营业利润率同比增长率排名        | int64   | -  |
| 基本每股收总资产同比增长率益同比增长率 | float64 | -  |
| 总资产同比增长率排名          | int64   | -  |

接口示例

```python
import akshare as ak

stock_hk_growth_comparison_em_df = ak.stock_hk_growth_comparison_em(symbol="03900")
print(stock_hk_growth_comparison_em_df)
```

数据示例

```
      代码    简称  基本每股收益同比增长率  基本每股收益同比增长率排名 ...  总资产同比增长率排名
0  03900  绿城中国   -90.123457            171          ...          91
```
