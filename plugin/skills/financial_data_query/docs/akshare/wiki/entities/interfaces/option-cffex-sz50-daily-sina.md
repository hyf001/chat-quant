---
title: "option_cffex_sz50_daily_sina - 日频行情-上证50指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_cffex_sz50_daily_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 中金所 > 日频行情-上证50指数
- 描述: 中金所-上证50指数-指定合约-日频行情
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex
- 限量: 单次返回指定合约的日频行情
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 日频行情-上证50指数

接口: option_cffex_sz50_daily_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex

描述: 中金所-上证50指数-指定合约-日频行情

限量: 单次返回指定合约的日频行情

输入参数

| 名称     | 类型  | 描述                                                                                         |
|--------|-----|--------------------------------------------------------------------------------------------|
| symbol | str | symbol="ho2303P2350"; 具体合约代码(包括看涨和看跌标识), 可以通过 ak.option_cffex_sz50_spot_sina 中的 call-标识 获取 |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| date   | object  | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | int64   | -   |

接口示例

```python
import akshare as ak

option_cffex_sz50_daily_sina_df = ak.option_cffex_sz50_daily_sina(symbol="ho2303P2350")
print(option_cffex_sz50_daily_sina_df)
```

数据示例

```
         date  open  high   low  close  volume
0  2022-12-21  16.8  16.8  16.8   16.8       6
1  2022-12-22  11.2  14.0  11.2   14.0      64
2  2022-12-23  14.0  17.8  14.0   16.0      14
3  2022-12-26  14.0  14.6  12.2   14.6      41
4  2022-12-27  11.2  11.4   9.6    9.6      62
5  2022-12-28   9.0  11.0   9.0   10.4     126
6  2022-12-29  10.4  13.0  10.2   10.8      63
7  2022-12-30   9.8  11.8   9.6    9.8      83
8  2023-01-03  10.6  12.0   7.4    7.6       4
```
