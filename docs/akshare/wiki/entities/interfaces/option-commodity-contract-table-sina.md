---
title: "option_commodity_contract_table_sina - 当前合约"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_commodity_contract_table_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权-新浪 > 当前合约
- 描述: 新浪财经-商品期权的 T 型报价表
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php
- 限量: 单次返回指定 symbol 和 contract 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 当前合约

接口: option_commodity_contract_table_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php

描述: 新浪财经-商品期权的 T 型报价表

限量: 单次返回指定 symbol 和 contract 的所有数据

输入参数

| 名称       | 类型  | 描述                                                               |
|----------|-----|------------------------------------------------------------------|
| symbol   | str | symbol="玉米期权"                                                    |
| contract | str | contract="au2204"; 可以通过 ak.option_commodity_contract_sina() 接口获取 |

输出参数

| 名称          | 类型      | 描述     |
|-------------|---------|--------|
| 看涨合约-买量     | int64   | -      |
| 看涨合约-买价     | float64 | -      |
| 看涨合约-最新价    | float64 | -      |
| 看涨合约-卖价     | float   | -      |
| 看涨合约-卖量     | int64   | -      |
| 看涨合约-持仓量    | int64   | -      |
| 看涨合约-涨跌     | float64 | -      |
| 行权价         | int64   | -      |
| 看涨合约-看涨期权合约 | object  | 看涨合约代码 |
| 看跌合约-买量     | int64   | -      |
| 看跌合约-买价     | float64 | -      |
| 看跌合约-最新价    | float64 | -      |
| 看跌合约-卖价     | float64 | -      |
| 看跌合约-卖量     | int64   | -      |
| 看跌合约-持仓量    | int64   | -      |
| 看跌合约-涨跌     | float64 | -      |
| 看跌合约-看跌期权合约 | object  | 看跌合约代码 |

接口示例

```python
import akshare as ak

option_commodity_contract_table_sina_df = ak.option_commodity_contract_table_sina(symbol="动力煤期权", contract="zc2103")
print(option_commodity_contract_table_sina_df)
```

数据示例

```
    看涨合约-买量  看涨合约-买价  看涨合约-最新价  看涨合约-卖价  ...  看跌合约-卖量  看跌合约-持仓量  看跌合约-涨跌  看跌合约-看跌期权合约
0       0.0      0.0      52.0      0.0  ...       91       540     0.00   zc2103P500
1       1.0     41.1      51.8      0.0  ...        1       305     0.00   zc2103P510
2       1.0     20.2      45.3     67.0  ...       18       255     0.00   zc2103P520
3       0.0      0.0      53.0      0.0  ...        1       260     0.00   zc2103P530
4       1.0    145.4     196.0    210.2  ...        9       280     0.00   zc2103P540
5       0.0      0.0      57.1      0.0  ...        1       277     0.00   zc2103P550
6       0.0      0.0      46.9      0.0  ...        0       252     0.00   zc2103P560
7       1.0      7.4      45.3      0.0  ...       21       174     0.00   zc2103P570
8       1.0      1.6      32.0      0.0  ...        5       479     0.00   zc2103P580
9       1.0      1.3      23.4      0.0  ...        1       293     0.00   zc2103P590
10      5.0      4.9       4.9     21.7  ...      504      1145   -66.67   zc2103P600
11      2.0      2.9       3.0      3.0  ...       96       451   -83.33   zc2103P610
12      0.0      0.0       0.1      0.1  ...       58       758   -81.82   zc2103P620
13      0.0      0.0       0.1      0.1  ...      103       840   -96.00   zc2103P630
14      0.0      0.0       0.1      0.1  ...       18       414   -98.21   zc2103P640
15      0.0      0.0       0.1      0.1  ...        0       276   -33.64   zc2103P650
16      0.0      0.0       0.1      0.1  ...        6       218    -5.49   zc2103P660
17      0.0      0.0       0.1      0.1  ...        0       164     1.87   zc2103P670
18      0.0      0.0       0.1      0.1  ...        0       199    -3.05   zc2103P680
19      0.0      0.0       0.1      0.1  ...        0       138     1.53   zc2103P690
20      0.0      0.0       0.1      0.1  ...        0       283     0.36   zc2103P700
21      0.0      0.0       0.1      0.1  ...        0       183     0.00   zc2103P710
22      0.0      0.0       0.1      0.1  ...        0       215    88.25   zc2103P720
23      0.0      0.0       0.1      0.1  ...        0       140    52.98   zc2103P730
24      0.0      0.0       0.1      0.1  ...        0       112     1.46   zc2103P740
25      0.0      0.0       0.1      0.1  ...        0       120    18.85   zc2103P750
26      0.0      0.0       0.1      0.1  ...        0       111    48.73   zc2103P760
27      0.0      0.0       0.1      0.1  ...        0       190    37.22   zc2103P770
28      0.0      0.0       0.1      0.1  ...        0       161    -2.29   zc2103P780
29      0.0      0.0       0.1      0.1  ...        0        79     7.46   zc2103P790
30      0.0      0.0       0.1      0.1  ...        1       141    -0.53   zc2103P800
31      0.0      0.0       0.1      0.1  ...        1        83     1.94   zc2103P810
32      0.0      0.0       0.1      0.1  ...        0       113   -10.08   zc2103P820
33      0.0      0.0       0.1      0.1  ...        0        40    25.82   zc2103P830
34      0.0      0.0       0.1      0.1  ...        0        36     6.71   zc2103P840
35      0.0      0.0       0.1      0.1  ...        0        17    16.98   zc2103P850
36      NaN      NaN       NaN      NaN  ...        1        25    16.06   zc2103P860
37      NaN      NaN       NaN      NaN  ...        0         0    14.76   zc2103P870
38      NaN      NaN       NaN      NaN  ...        0         0    13.83   zc2103P880
```
