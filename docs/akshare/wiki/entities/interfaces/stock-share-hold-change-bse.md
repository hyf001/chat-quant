---
title: "stock_share_hold_change_bse - 董监高及相关人员持股变动-北证"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_share_hold_change_bse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 董监高及相关人员持股变动-北证
- 描述: 北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动
- 目标地址: https://www.bse.cn/disclosure/djg_sharehold_change.html
- 限量: 单次获取指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 董监高及相关人员持股变动-北证

接口: stock_share_hold_change_bse

目标地址: https://www.bse.cn/disclosure/djg_sharehold_change.html

描述: 北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动

限量: 单次获取指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                          |
|--------|-----|---------------------------------------------|
| symbol | str | symbol="430489"; choice of {"全部", "具体股票代码"} |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 代码     | object  | -        |
| 简称     | object  | -        |
| 姓名     | object  | -        |
| 职务     | object  | -        |
| 变动日期   | object  | -        |
| 变动股数   | float64 | 注意单位: 万股 |
| 变动前持股数 | float64 | 注意单位: 万股 |
| 变动后持股数 | float64 | 注意单位: 万股 |
| 变动均价   | float64 | 注意单位: 元  |
| 变动原因   | object  | -        |

接口示例

```python
import akshare as ak

stock_share_hold_change_bse_df = ak.stock_share_hold_change_bse(symbol="430489")
print(stock_share_hold_change_bse_df)
```

数据示例

```
   代码    简称   姓名     职务        变动日期   变动股数   变动前持股数   变动后持股数  变动均价  变动原因
0  430489  佳先股份   李兑      董事  2023-07-28  7.151   0.0000   7.1510  4.66  竞价交易
1  430489  佳先股份   李平  高级管理人员  2023-07-14  2.000  23.0565  25.0565  4.64  竞价交易
2  430489  佳先股份  周星源  高级管理人员  2023-06-21  2.000  28.2896  30.2896  4.59  竞价交易
3  430489  佳先股份   汪静  高级管理人员  2023-06-20  1.000  70.0360  71.0360  4.52  竞价交易
4  430489  佳先股份   汪静  高级管理人员  2023-06-19  1.000  69.0360  70.0360  4.56  竞价交易
5  430489  佳先股份   丁柱  高级管理人员  2023-06-16  0.500  53.2920  53.7920  4.50  竞价交易
6  430489  佳先股份   丁柱  高级管理人员  2023-06-15  0.500  52.7920  53.2920  4.48  竞价交易
7  430489  佳先股份   丁柱  高级管理人员  2023-06-14  1.000  51.7920  52.7920  4.48  竞价交易
```
