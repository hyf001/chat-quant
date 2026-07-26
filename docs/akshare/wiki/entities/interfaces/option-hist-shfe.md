---
title: "option_hist_shfe - 上海期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_hist_shfe

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 上海期货交易所
- 描述: 上海期货交易所-商品期权数据
- 目标地址: https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/
- 限量: 单次返回指定 symbol 和 trade_date 的期权行情数据, 只能获取 20200824 之后的数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上海期货交易所

接口: option_hist_shfe

目标地址: https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/

描述: 上海期货交易所-商品期权数据

限量: 单次返回指定 symbol 和 trade_date 的期权行情数据, 只能获取 20200824 之后的数据

输入参数

| 名称         | 类型  | 描述                                                                                                                              |
|------------|-----|---------------------------------------------------------------------------------------------------------------------------------|
| symbol     | str | symbol="铜期权"; choice of {'原油期权', '铜期权', '铝期权', '锌期权', '铅期权', '螺纹钢期权', '镍期权', '锡期权', '氧化铝期权', '黄金期权', '白银期权', '丁二烯橡胶期权', '天胶期权'} |
| trade_date | str | trade_date="20191017"                                                                                                           |

输出参数

Part-1: 上海期货交易所期权合约行情

| 名称    | 类型      | 描述    |
|-------|---------|-------|
| 合约代码  | object  |       |
| 开盘价   | float64 |       |
| 最高价   | float64 |       |
| 最低价   | float64 |       |
| 收盘价   | float64 |       |
| 前结算价  | float64 |       |
| 结算价   | float64 |       |
| 涨跌1   | float64 |       |
| 涨跌2   | float64 |       |
| 成交量   | float64 |       |
| 持仓量   | float64 |       |
| 持仓量变化 | float64 |       |
| 成交额   | float64 |       |
| 德尔塔   | float64 | Delta |
| 行权量   | float64 |       |

注:
1. 期权报价单位: 铜、天然橡胶为元/吨.
2. 期权交易单位: 铜为 5 吨/手；天然橡胶为 10 吨/手.
3. 成交量、持仓量、持仓量变化单位为手, 双边计算；成交额双边计算.
4. 涨跌1=收盘价-前结算价, 涨跌2=结算价-前结算价.
5. 合约系列: 具有相同月份标的期货合约的所有期权合约的统称.
6. 隐含波动率: 根据期权市场交易价格, 利用期权定价模型计算出来的标的期货合约的价格波动率数值.

Part-2: 上海期货交易所隐含波动参考值

| 名称    | 类型      | 描述     |
|-------|---------|--------|
| 合约系列  | object  |        |
| 成交量   | float64 | 注意单位：手 |
| 持仓量   | float64 | 注意单位：手 |
| 持仓量变化 | float64 | 注意单位：手 |
| 成交额   | float64 | 注意单位：手 |
| 行权量   | float64 | 注意单位：手 |
| 隐含波动率 | float64 |        |

接口示例

```python
import akshare as ak

option_hist_shfe_df = ak.option_hist_shfe(symbol="铝期权", trade_date="20200827")
print(option_hist_shfe_df)

option_vol_shfe_df = ak.option_vol_shfe(symbol="天胶期权", trade_date="20250418")
print(option_vol_shfe_df)
```

数据示例

part_1: 上海期货交易所期权合约行情

```
     合约代码 开盘价 最高价 最低价  ...  持仓量变化  成交额       德尔塔  行权量
588  al2010C12400                                ...      0  0.0  0.999999    0
589  al2010C12500                                ...      0  0.0  0.999999    0
590  al2010C12600                                ...      0  0.0  0.999842    0
591  al2010C12700                                ...      0  0.0  0.998645    0
592  al2010C12800                                ...      0  0.0  0.996855    0
..                              ...  ..  ..  ..  ...    ...  ...       ...  ...
901  al2101P15500                                ...      0  0.0 -0.835443    0
902  al2101P15600                                ...      0  0.0 -0.853291    0
903  al2101P15700                                ...      0  0.0 -0.869626    0
904  al2101P15800                                ...      0  0.0 -0.884810    0
905  al2101P15900                                ...      0  0.0 -0.898378    0
```

part_2: 上海期货交易所隐含波动参考值

```
   合约系列   成交量   持仓量  持仓量变化       成交额 行权量     隐含波动率
11  al2010                          2008  8373    435  135.3745   0  0.178040
12  al2011                           292   906      0   12.1665   0  0.150241
13  al2012                             0    66      0    0.0000   0  0.150241
14  al2101                             0    66      0    0.0000   0  0.150241
```
