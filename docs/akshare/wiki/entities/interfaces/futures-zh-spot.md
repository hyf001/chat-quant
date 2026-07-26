---
title: "futures_zh_spot - 内盘-实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_zh_spot

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货行情数据 > 内盘-实时行情数据
- 描述: 新浪财经-期货页面的实时行情数据
- 目标地址: https://finance.sina.com.cn/futuremarket/
- 限量: 单次返回当日可以订阅的所有期货品种数据；只能获取近期合约的数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-实时行情数据

接口: futures_zh_spot

目标地址: https://finance.sina.com.cn/futuremarket/

描述: 新浪财经-期货页面的实时行情数据

限量: 单次返回当日可以订阅的所有期货品种数据；只能获取近期合约的数据

输入参数

| 名称             | 类型  | 描述                                                    |
|----------------|-----|-------------------------------------------------------|
| subscribe_list | str | 需要订阅的合约代码; e.g., 按照示例获取                               |
| market         | str | market="CF"; market="CF": 商品期货, market="FF": 金融期货     |
| adjust         | str | adjust='0'; adjust='1': 返回合约、交易所和最小变动单位的实时数据, 返回数据会变慢 |

输出参数

| 名称                | 类型      | 描述                            |
|-------------------|---------|-------------------------------|
| symbol            | object  | 品种                            |
| time              | object  | 时间, e.g., 144050表示下午14点40分50秒 |
| open              | float64 | 开盘                            |
| high              | float64 | 高                             |
| low               | float64 | 低                             |
| current_price     | float64 | 当前价格(买价)                      |
| bid_price         | float64 | 买                             |
| ask_price         | float64 | 卖价                            |
| buy_vol           | int64   | 买量                            |
| sell_vol          | int64   | 卖量                            |
| hold              | float64 | 持仓量                           |
| volume            | int64   | 成交量                           |
| avg_price         | float64 | 均价                            |
| last_close        | float64 | 上一个交易日的收盘价                    |
| last_settle_price | float64 | 上一个交易日的结算价                    |

接口示例-单品种获取

```python
import akshare as ak

futures_zh_spot_df = ak.futures_zh_spot(symbol='V2205', market="CF", adjust='0')
print(futures_zh_spot_df)
```

数据示例-单品种获取

```
    symbol    time    open  ...  avg_price  last_close  last_settle_price
0  PVC2205  151039  8280.0  ...     8449.0      8423.0             8397.0
```

接口示例-多品种获取

```python
import akshare as ak
