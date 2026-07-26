---
title: "broker_positions_process - 建仓过程"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_positions_process

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 建仓过程
- 描述: 建仓过程数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 建仓过程

### 接口名称

broker_positions_process

### 接口描述

建仓过程数据接口

### 请求参数

| 参数名        | 说明   | 举例                 |
|:-----------|:-----|--------------------|
| broker     | 席位   | 永安期货               |
| code       | 合约代号 | rb1810             |
| start_date | 开始日期 | "2020-02-03"; 可选参数 |
| end_date   | 结束日期 | "2020-06-03"; 可选参数 |

### 返回参数

| 参数名          | 类型     | 说明                     |
|:-------------|:-------|------------------------|
| long         | int    | 多头持仓                   |
| short        | int    | 空头持仓                   |
| trans_date   | date   | 日期                     |
| code         | string | 合约代号                   |
| profit       | float  | 当日盈亏金额，正数为盈利，负数为亏损，单位元 |
| net_hold     | int    | 净持仓，多头持仓-空头持仓          |
| total_profit | float  | 累计盈亏金额，正数为盈利，负数为亏损，单位元 |
| cost         | float  | 估算盈亏平衡价格               |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_positions_process_df = pro.broker_positions_process(broker="永安期货", code="rb2010", start_date="2020-02-03", end_date="2020-06-03")
print(broker_positions_process_df)
```

### 返回示例

```
      long  short  trans_date  ... settle_price  total_profit     cost
0    42187  17225  2020-02-03  ...         3196     -26297250  3301.35
1    50394  17694  2020-02-04  ...         3260     -10321570  3291.56
2    52270  20802  2020-02-05  ...         3292        142430  3291.55
3    63213  24253  2020-02-06  ...         3312       6436030  3295.48
4    64025  27434  2020-02-07  ...         3337      16176030  3292.79
..     ...    ...         ...  ...          ...           ...      ...
79  101358  80513  2020-05-28  ...         3492     101931690  3003.00
80   99001  73076  2020-05-29  ...         3533     110478140  3106.85
81   95185  55351  2020-06-01  ...         3580     122662890  3272.06
82  133541  62476  2020-06-02  ...         3608     133816410  3419.70
83  144905  55558  2020-06-03  ...         3640     156557210  3464.78
```
