---
title: "currency_pair_map - 指定币种的所有货币对"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# currency_pair_map

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 指定币种的所有货币对
- 描述: 指定币种的所有能够获取到的货币对信息，历史数据可以调用 **ak.currency_history()** 获取
- 目标地址: https://cn.investing.com/currencies/cny-jmd
- 限量: 单次返回指定币种的所有能获取数据的货币对
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 指定币种的所有货币对

接口: currency_pair_map

目标地址: https://cn.investing.com/currencies/cny-jmd

描述: 指定币种的所有能够获取到的货币对信息，历史数据可以调用 **ak.currency_history()** 获取

限量: 单次返回指定币种的所有能获取数据的货币对

输入参数

| 名称     | 类型  | 描述                                                                                       |
|--------|-----|------------------------------------------------------------------------------------------|
| symbol | str | symbol="人民币"; 此处提供中文的币种名称, 可以访问[网页](https://cn.investing.com/currencies/cny-jmd) 的页面下方查看 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| name | object  | 货币对中文简称 |
| code | float64 | 货币对代码   |

接口示例

```python
import akshare as ak

currency_pair_map_df = ak.currency_pair_map(symbol="人民币")
print(currency_pair_map_df)
```

数据示例

```
         name     code
0     人民币-丹麦克朗  cny-dkk
1     丹麦克朗-人民币  dkk-cny
2     人民币-瑞士法郎  cny-chf
3     瑞士法郎-人民币  chf-cny
4     人民币-捷克克朗  cny-czk
..         ...      ...
85   人民币-澳大利亚元  cny-aud
86   澳大利亚元-人民币  aud-cny
87    人民币-新西兰元  cny-nzd
88    新西兰元-人民币  nzd-cny
89  人民币-巴拿马巴波亚  cny-pab
[90 rows x 2 columns]
```
