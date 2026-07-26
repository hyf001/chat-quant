---
title: "option_hist_gfex - 广州期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_hist_gfex

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 广州期货交易所
- 描述: 广州期货交易所-商品期权数据
- 目标地址: http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml
- 限量: 单次返回指定 symbol 和 trade_date 的期权行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 广州期货交易所

接口: option_hist_gfex

目标地址: http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml

描述: 广州期货交易所-商品期权数据

限量: 单次返回指定 symbol 和 trade_date 的期权行情数据

输入参数

| 名称         | 类型  | 描述                                     |
|------------|-----|----------------------------------------|
| symbol     | str | symbol="工业硅"; choice of {"工业硅", "碳酸锂"} |
| trade_date | str | trade_date="20230724"; 交易日             |

输出参数

广州期货交易所期权合约行情

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 商品名称  | object  |    |
| 合约名称  | object  |    |
| 开盘价   | float64 |    |
| 最高价   | float64 |    |
| 最低价   | float64 |    |
| 收盘价   | float64 |    |
| 前结算价  | float64 |    |
| 结算价   | float64 |    |
| 涨跌    | float64 |    |
| 涨跌1   | float64 |    |
| Delta | float64 |    |
| 成交量   | int64   |    |
| 持仓量   | int64   |    |
| 持仓量变化 | int64   |    |
| 成交额   | float64 |    |
| 行权量   | int64   |    |
| 隐含波动率 | float64 |    |

说明:

1. 价格：元/吨
2. 成交量、持仓量、持仓量变化：手（按单边计算）
3. 成交额：万元（按单边计算）
4. 涨跌＝收盘价-前结算价
5. 涨跌1=今结算价-前结算价
6. 合约系列：具有相同月份标的期货合约的所有期权合约的统称
7. 隐含波动率：根据期权市场价格，利用期权定价模型计算的标的期货合约价格波动率

接口示例-广州期货交易所期权合约行情(工业硅)

```python
import akshare as ak

option_hist_gfex_df = ak.option_hist_gfex(symbol="工业硅", trade_date="20230418")
print(option_hist_gfex_df)
```

数据示例-广州期货交易所期权合约行情(工业硅)

```
      商品名称  合约名称  开盘价  最高价  ...  持仓量变化      成交额  行权量      隐含波动率
0      工业硅  si2308-C-13000  0.0  0.0  ...      0    0.000    0  22.436477
1      工业硅  si2308-C-13200  0.0  0.0  ...      0    0.000    0  22.538374
2      工业硅  si2308-C-13400  0.0  0.0  ...      0    0.000    0  22.493164
3      工业硅  si2308-C-13600  0.0  0.0  ...      0    0.000    0  22.467333
4      工业硅  si2308-C-13800  0.0  0.0  ...      0    0.000    0  22.530720
..     ...             ...  ...  ...  ...    ...      ...  ...        ...
597    工业硅  si2403-P-17800  0.0  0.0  ...      0    0.000    0  19.727143
598    工业硅  si2403-P-18000  0.0  0.0  ...      0    0.000    0  19.728669
599    工业硅  si2403-P-18200  0.0  0.0  ...      0    0.000    0  19.719663
600  工业硅小计                  NaN  NaN  ...   -427  494.246    1        NaN
601     总计                  NaN  NaN  ...   -427  494.246    1        NaN
```
