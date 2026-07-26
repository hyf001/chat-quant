---
title: "option_sse_codes_sina - 所有合约的代码"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_codes_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 所有合约的代码
- 描述: 新浪期权-看涨看跌合约合约的代码
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回指定 symbol 合约的代码
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 所有合约的代码

接口: option_sse_codes_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 新浪期权-看涨看跌合约合约的代码

限量: 单次返回指定 symbol 合约的代码

输入参数

| 名称         | 类型  | 描述                                        |
|------------|-----|-------------------------------------------|
| symbol     | str | symbol="看涨期权"; choice of {"看涨期权", "看跌期权"} |
| trade_date | str | trade_date="202002";                      |
| underlying | str | underlying="510300"                       |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 序号   | int64  | -   |
| 期权代码 | object | -   |

接口示例

```python
import akshare as ak

option_sse_codes_sina_df = ak.option_sse_codes_sina(trade_date="202002", underlying="510300")
print(option_sse_codes_sina_df)
```

数据示例

```
    序号   期权代码
0    1  10003887
1    2  10003765
2    3  10003709
3    4  10003766
4    5  10003710
5    6  10003767
6    7  10003711
7    8  10003768
8    9  10003712
9   10  10003769
10  11  10003713
11  12  10003770
12  13  10003714
13  14  10003771
14  15  10003715
15  16  10003772
16  17  10003716
17  18  10003773
18  19  10003717
19  20  10003821
20  21  10003829
```
