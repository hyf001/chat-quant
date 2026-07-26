---
title: "option_vol_gfex - 广州期货交易所-隐含波动参考值"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_vol_gfex

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 广州期货交易所-隐含波动参考值
- 描述: 广州期货交易所-商品期权数据-隐含波动参考值
- 目标地址: http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml
- 限量: 单次返回指定 symbol 和 trade_date 的期权行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 广州期货交易所-隐含波动参考值

接口: option_vol_gfex

目标地址: http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml

描述: 广州期货交易所-商品期权数据-隐含波动参考值

限量: 单次返回指定 symbol 和 trade_date 的期权行情数据

输入参数

| 名称         | 类型  | 描述                                     |
|------------|-----|----------------------------------------|
| symbol     | str | symbol="工业硅"; choice of {"工业硅", "碳酸锂"} |
| trade_date | str | trade_date="20230724"                  |

输出参数

广州期货交易所-隐含波动参考值

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 合约系列  | object  |    |
| 隐含波动率 | float64 |    |

说明:

1. 价格：元/吨
2. 成交量、持仓量、持仓量变化：手（按单边计算）
3. 成交额：万元（按单边计算）
4. 涨跌＝收盘价-前结算价
5. 涨跌1=今结算价-前结算价
6. 合约系列：具有相同月份标的期货合约的所有期权合约的统称
7. 隐含波动率：根据期权市场价格，利用期权定价模型计算的标的期货合约价格波动率

接口示例-广州期货交易所-隐含波动参考值(工业硅)

```python
import akshare as ak

option_vol_gfex_df = ak.option_vol_gfex(symbol="工业硅", trade_date="20230418")
print(option_vol_gfex_df)
```

数据示例-广州期货交易所-隐含波动参考值(工业硅)

```
   合约系列  隐含波动率
0  si2308  22.542314
1  si2309  21.018517
2  si2310  21.018517
3  si2311  21.018517
4  si2312  19.894257
5  si2401  19.894257
6  si2402  19.894257
7  si2403  19.729307
```
