---
title: "forex_spot_em - 实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# forex_spot_em

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 实时行情数据
- 描述: 东方财富网-行情中心-外汇市场-所有汇率-实时行情数据
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#forex_all
- 限量: 单次返回所有实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 实时行情数据

接口: forex_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#forex_all

描述: 东方财富网-行情中心-外汇市场-所有汇率-实时行情数据

限量: 单次返回所有实时行情数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 序号  | int64   | -  |
| 代码  | object  | -  |
| 名称  | object  | -  |
| 最新价 | float64 | -  |
| 涨跌额 | float64 | -  |
| 涨跌幅 | float64 | -  |
| 今开  | float64 | -  |
| 最高  | float64 | -  |
| 最低  | float64 | -  |
| 昨收  | float64 | -  |

接口示例

```python
import akshare as ak

forex_spot_em_df = ak.forex_spot_em()
print(forex_spot_em_df)
```

数据示例

```
     序号  代码           名称  ...          最高        最低        昨收
0      1   USDZAR      美元兑南非兰特  ...   17.7123   17.5129   17.5916
1      2   HKDJPY        港币兑日元  ...   18.3602   18.2621   18.2684
2      3   USDJPY        美元兑日元  ...  144.1268  143.3220  143.4055
3      4   CADJPY        加元兑日元  ...  105.5900  105.0575  105.0855
4      5   CNHJPY     离岸人民币兑日元  ...   20.1081   20.0145   20.0260
..   ...      ...          ...  ...       ...       ...       ...
185  186   JPYHKD     100日元兑港币  ...    5.4757    5.4466    5.4739
186  187   JPYTRY  100日元兑土耳其里拉  ...   27.7972   27.6140   27.7796
187  188  CNYZARC   人民币南非兰特中间价  ...    2.4602    2.4602    2.4773
188  189   ZARUSD      南非兰特兑美元  ...    0.0569    0.0565    0.0569
189  190   HUFUSD     匈牙利福林兑美元  ...    0.0030    0.0029    0.0030
[190 rows x 10 columns]
```
