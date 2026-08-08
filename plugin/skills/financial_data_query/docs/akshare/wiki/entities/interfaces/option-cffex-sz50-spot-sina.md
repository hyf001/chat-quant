---
title: "option_cffex_sz50_spot_sina - 实时行情-上证50指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_cffex_sz50_spot_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 中金所 > 实时行情-上证50指数
- 描述: 新浪财经-中金所-上证50指数-指定合约-实时行情
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex
- 限量: 单次返回指定合约的实时行情
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时行情-上证50指数

接口: option_cffex_sz50_spot_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex

描述: 新浪财经-中金所-上证50指数-指定合约-实时行情

限量: 单次返回指定合约的实时行情

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="ho2303" |

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

option_cffex_sz50_spot_sina_df = ak.option_cffex_sz50_spot_sina(symbol="ho2303")
print(option_cffex_sz50_spot_sina_df)
```

数据示例

```
    看涨合约-买量  看涨合约-买价  看涨合约-最新价  ...  看跌合约-持仓量  看跌合约-涨跌      看跌合约-标识
0         1    301.2     318.4  ...        82    10.71  ho2303P2325
1         6    302.4     306.0  ...        86    -7.89  ho2303P2350
2         1    270.8     276.2  ...        67   -19.67  ho2303P2375
3         1    265.6     269.8  ...        45    14.67  ho2303P2400
4         1    222.2     219.0  ...        18    -5.06  ho2303P2425
5         1    225.2     234.6  ...        29    -3.09  ho2303P2450
6         1    184.0     188.0  ...        13   -14.40  ho2303P2475
7         1    184.2     178.0  ...        50    19.02  ho2303P2500
8         1    148.6     157.0  ...        42    -5.96  ho2303P2550
9         1    117.0     115.8  ...       117    -9.39  ho2303P2600
10        1     91.2      94.4  ...        74    -0.68  ho2303P2650
11       28     69.2      74.0  ...       670    -5.25  ho2303P2700
12        1     52.0      53.0  ...        11    -3.49  ho2303P2750
13        1     38.0      38.8  ...         9    -2.91  ho2303P2800
14       22     26.8      28.0  ...        14     9.94  ho2303P2850
15       32     19.0      20.4  ...         3    -5.88  ho2303P2900
16       10     13.6      13.6  ...         6    -3.05  ho2303P2950
17        6     10.0      10.4  ...         6    15.58  ho2303P3000
```
