---
title: "option_cffex_zz1000_spot_sina - 实时行情-中证1000指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_cffex_zz1000_spot_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 中金所 > 实时行情-中证1000指数
- 描述: 新浪财经-中金所-中证1000指数-指定合约-实时行情
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回指定合约的实时行情
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时行情-中证1000指数

接口: option_cffex_zz1000_spot_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 新浪财经-中金所-中证1000指数-指定合约-实时行情

限量: 单次返回指定合约的实时行情

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="mo2208" |

输出参数

| 名称       | 类型      | 描述     |
|----------|---------|--------|
| 看涨合约-买量  | int64   | -      |
| 看涨合约-买价  | float64 | -      |
| 看涨合约-最新价 | float64 | -      |
| 看涨合约-卖价  | float   | -      |
| 看涨合约-卖量  | int64   | -      |
| 看涨合约-持仓量 | int64   | -      |
| 看涨合约-涨跌  | float64 | -      |
| 行权价      | int64   | -      |
| 看涨合约-标识  | object  | 看涨合约代码 |
| 看跌合约-买量  | int64   | -      |
| 看跌合约-买价  | float64 | -      |
| 看跌合约-最新价 | float64 | -      |
| 看跌合约-卖价  | float64 | -      |
| 看跌合约-卖量  | int64   | -      |
| 看跌合约-持仓量 | int64   | -      |
| 看跌合约-涨跌  | float64 | -      |
| 看跌合约-标识  | object  | 看跌合约代码 |

接口示例

```python
import akshare as ak

option_cffex_zz1000_spot_sina_df = ak.option_cffex_zz1000_spot_sina(symbol="mo2208")
print(option_cffex_zz1000_spot_sina_df)
```

数据示例

```
    看涨合约-买量  看涨合约-买价  看涨合约-最新价  ...  看跌合约-持仓量  看跌合约-涨跌      看跌合约-标识
0         1    760.4     783.2  ...       644   353.13  mo2208P6200
1         1    666.8     690.0  ...       719   304.65  mo2208P6300
2         1    575.0     644.0  ...       586   265.00  mo2208P6400
3         1    494.4     491.4  ...      1018   236.90  mo2208P6500
4         1    408.4     405.6  ...       829   210.34  mo2208P6600
5         1    329.8     321.2  ...       894   179.04  mo2208P6700
6         1    257.8     257.6  ...      1081   147.93  mo2208P6800
7         1    197.4     197.4  ...      1155   122.44  mo2208P6900
8         1    138.6     138.6  ...      1295   106.80  mo2208P7000
9         1     96.6      96.8  ...       846    87.83  mo2208P7100
10        1     63.8      63.8  ...       356    78.02  mo2208P7200
11        1     40.2      40.2  ...       146    64.20  mo2208P7300
12        2     26.0      26.0  ...       129    54.71  mo2208P7400
13        1     16.2      16.4  ...       104    49.04  mo2208P7500
14        1     10.6      10.6  ...        39    33.54  mo2208P7600
15        1      6.8       7.0  ...        41    21.32  mo2208P7700
16       14      5.0       5.2  ...        37    34.30  mo2208P7800
17        6      3.4       3.6  ...        21    30.39  mo2208P7900
```
