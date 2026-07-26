---
title: "option_hist_czce - 郑州商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_hist_czce

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 郑州商品交易所
- 描述: 郑州商品交易所-商品期权数据
- 目标地址: http://www.czce.com.cn/cn/jysj/mrhq/H770301index_1.htm
- 限量: 单次返回指定 symbol 和 trade_date 的期权行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 郑州商品交易所

接口: option_hist_czce

目标地址: http://www.czce.com.cn/cn/jysj/mrhq/H770301index_1.htm

描述: 郑州商品交易所-商品期权数据

限量: 单次返回指定 symbol 和 trade_date 的期权行情数据

输入参数

| 名称         | 类型  | 描述                                              |
|------------|-----|-------------------------------------------------|
| symbol     | str | symbol="白糖期权"; 交易所上市的期权品种，最早上市的为 20170419 的白糖期权 |
| trade_date | str | trade_date="20191017"                           |

输出参数

郑州商品交易所-期权合约行情

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 品种代码    | object  |     |
| 昨结算     | float64 |     |
| 今开盘     | float64 |     |
| 最高价     | float64 |     |
| 最低价     | float64 |     |
| 今收盘     | float64 |     |
| 今结算     | float64 |     |
| 涨跌1     | float64 |     |
| 涨跌2     | float64 |     |
| 成交量(手)  | float64 |     |
| 空盘量     | float64 |     |
| 增减量     | float64 |     |
| 成交额(万元) | float64 |     |
| DELTA   | float64 |     |
| 隐含波动率   | float64 |     |
| 行权量     | float64 |     |

说明:

1. 价格: 元/吨
2. 成交量、空盘量: 手
3. 成交额: 万元
4. 涨跌一: 今收盘-昨结算
5. 涨跌二: 今结算-昨结算
6. 隐含波动率: 将当日期权合约的结算价代入期权定价模型, 反推出来的波动率数值
7. 交易所早期的字段名不统一，本接口字段统一为最新值

接口示例

```python
import akshare as ak

option_hist_czce_df = ak.option_hist_czce(symbol="白糖期权", trade_date="20240711")
print(option_hist_czce_df)
```

数据示例

```
      合约代码    昨结算   今开盘   最高价 最低价  ... 增减量 成交额(万元) DELTA 隐含波动率 行权量
0    SR409C5400  774.5    0.0    0.0    0.0  ...  0.0     0.00  0.9888  20.73  0.0
1    SR409C5500  675.0  691.0  696.0  691.0  ... -1.0     2.77  0.9814  19.42  0.0
2    SR409C5600  576.0    0.0    0.0    0.0  ...  0.0     0.00  0.9701  18.06  0.0
3    SR409C5700  478.0  507.0  509.0  507.0  ... -2.0     1.51  0.9529  16.65  0.0
4    SR409C5800  381.5  382.5  411.0  382.5  ... -8.0    60.66  0.9259  15.18  0.0
..          ...    ...    ...    ...    ...  ...  ...      ...     ...    ...  ...
177  SR505P6100  375.5    0.0    0.0    0.0  ...  0.0     0.00 -0.6236  11.80  0.0
178  SR505P6200  446.5    0.0    0.0    0.0  ...  0.0     0.00 -0.6807  11.86  0.0
179  SR505P6300  522.5    0.0    0.0    0.0  ...  0.0     0.00 -0.7318  11.97  0.0
180  SR505P6400  604.0    0.0    0.0    0.0  ...  0.0     0.00 -0.7763  12.18  0.0
181  SR505P6500  686.5    0.0    0.0    0.0  ...  0.0     0.00 -0.8193  12.18  0.0
[182 rows x 16 columns]
```
