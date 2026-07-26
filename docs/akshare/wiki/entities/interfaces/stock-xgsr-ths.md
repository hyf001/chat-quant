---
title: "stock_xgsr_ths - 新股上市首日"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_xgsr_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 新股上市首日
- 描述: 同花顺-数据中心-新股数据-新股上市首日
- 目标地址: https://data.10jqka.com.cn/ipo/xgsr/
- 限量: 单次返回当前交易日的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 新股上市首日

接口: stock_xgsr_ths

目标地址: https://data.10jqka.com.cn/ipo/xgsr/

描述: 同花顺-数据中心-新股数据-新股上市首日

限量: 单次返回当前交易日的所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 序号    | int64   | -  |
| 股票代码  | object  | -  |
| 股票简称  | object  | -  |
| 上市日期  | object  | -  |
| 发行价   | float64 | -  |
| 最新价   | float64 | -  |
| 首日开盘价 | float64 | -  |
| 首日收盘价 | float64 | -  |
| 首日最高价 | float64 | -  |
| 首日最低价 | float64 | -  |
| 首日涨跌幅 | float64 | -  |
| 是否破发  | object  | -  |

接口示例

```python
import akshare as ak

stock_xgsr_ths_df = ak.stock_xgsr_ths()
print(stock_xgsr_ths_df)
```

数据示例

```
        序号  股票代码 股票简称  上市日期  ...   首日最高价  首日最低价 首日涨跌幅 是否破发
0        1  920019  铜冠矿建  2024-10-11  ...   55.55  33.33   7.3141     否
1        2  001279  强邦新材  2024-10-11  ...  245.00  87.12  17.3895     否
2        3  301618  长联科技  2024-09-30  ...  408.00  99.00  17.0398     否
3        4  688615  合合信息  2024-09-26  ...  116.30  88.93   1.0591     否
4        5  301551  无线传媒  2024-09-26  ...   39.39  29.11   3.1883     否
...    ...     ...   ...         ...  ...     ...    ...      ...   ...
3780  3781  300042  朗科科技  2010-01-08  ...   56.50  51.00   0.3449     是
3781  3782  601117  中国化学  2010-01-07  ...    5.86   5.65   0.0589     否
3782  3783  002329  皇氏集团  2010-01-06  ...   29.76  27.68   0.4308     是
3783  3784  002330   得利斯  2010-01-06  ...   23.98  21.00   0.8194     是
3784  3785  002331  皖通科技  2010-01-06  ...   45.00  40.62   0.6011     是
[3785 rows x 12 columns]
```
