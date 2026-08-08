---
title: "fx_pair_quote - 外币对即期报价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# fx_pair_quote

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 外币对即期报价
- 描述: 外币对即期报价
- 目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/
- 限量: 单次返回当前时点最近更新的即时数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 外币对即期报价

接口: fx_pair_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/

描述: 外币对即期报价

限量: 单次返回当前时点最近更新的即时数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述              |
|-----|---------|-----------------|
| 货币对 | object  | e.g., "AUD/USD" |
| 买报价 | float64 | e.g., "0.68460" |
| 卖报价 | float64 | e.g., "0.68461" |

**注：本行情为询价报价行情(美元为ODM), 实时更新**

接口示例

```python
import akshare as ak

fx_pair_quote_df = ak.fx_pair_quote()
print(fx_pair_quote_df)
```

数据示例

```
        货币对        买报价        卖报价
0   AUD/USD    0.69594    0.69600
1   EUR/JPY  143.80300  143.81500
2   EUR/USD    1.05929    1.05935
3   GBP/USD    1.22733    1.22739
4   USD/CAD    1.28238    1.28247
5   USD/CHF    0.95410    0.95417
6   USD/HKD    7.84744    7.84755
7   USD/JPY  135.75500  135.76000
8   USD/SGD    1.38510    1.38518
9   NZD/USD    0.63003    0.63012
10  EUR/GBP    0.86308    0.86308
```
