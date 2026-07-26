---
title: "option_sse_greeks_sina - 期权希腊字母信息表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_greeks_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 期权希腊字母信息表
- 描述: 新浪财经-期权希腊字母信息表
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回当前交易日的期权希腊字母信息表
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期权希腊字母信息表

接口: option_sse_greeks_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 新浪财经-期权希腊字母信息表

限量: 单次返回当前交易日的期权希腊字母信息表

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="10002273" |

输出参数

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 字段  | object | -   |
| 值   | object | -   |

接口示例

```python
import akshare as ak

option_sse_greeks_sina_df = ak.option_sse_greeks_sina(symbol="10002273")
print(option_sse_greeks_sina_df)
```

数据示例

```
        字段                  值
0   期权合约简称       50ETF购2月2500
1      成交量                626
2    Delta                  1
3    Gamma                  0
4    Theta               -0.1
5     Vega                  0
6    隐含波动率             0.0008
7      最高价             0.4799
8      最低价             0.4477
9     交易代码  510050C2002M02500
10     行权价             2.5000
11     最新价             0.4550
12    理论价值             0.4591
```
