---
title: "option_sse_spot_price_sina - 实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_spot_price_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 实时数据
- 描述: 期权实时数据
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回期权实时数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时数据

接口: option_sse_spot_price_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 期权实时数据

限量: 单次返回期权实时数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="10002273" |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| 字段  | str | -   |
| 值   | str | -   |

接口示例

```python
import akshare as ak

option_sse_spot_price_sina_df = ak.option_sse_spot_price_sina(symbol="10002273")
print(option_sse_spot_price_sina_df)
```

数据示例

```
        字段                    值
0       买量                    1
1       买价               0.4518
2      最新价               0.4550
3       卖价               0.4590
4       卖量                    1
5      持仓量                  979
6       涨幅                -2.57
7      行权价               2.5000
8      昨收价               0.4585
9      开盘价               0.4550
10     涨停价               0.7637
11     跌停价               0.1703
12    申卖价五               0.4735
13    申卖量五                    1
14    申卖价四               0.4700
15    申卖量四                    1
16    申卖价三               0.4684
17    申卖量三                    1
18    申卖价二               0.4600
19    申卖量二                    2
20    申卖价一               0.4590
21    申卖量一                    1
22    申买价一               0.4518
23   申买量一                     1
24    申买价二               0.4500
25    申买量二                    3
26    申买价三               0.4467
27    申买量三                    1
28    申买价四               0.4426
29    申买量四                    1
30    申买价五               0.4419
31    申买量五                    1
32    行情时间  2020-02-21 14:56:45
33  主力合约标识                    0
34     状态码                 E 01
35  标的证券类型                  EBS
36    标的股票               510050
37  期权合约简称         50ETF购2月2500
38      振幅                 7.02
39     最高价               0.4799
40     最低价               0.4477
41     成交量                  626
42     成交额           2851394.00
```
