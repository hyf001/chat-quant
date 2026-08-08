---
title: "bond_cb_summary_sina - 可转债-债券概况"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cb_summary_sina

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债-债券概况
- 描述: 新浪财经-债券-可转债-债券概况
- 目标地址: https://money.finance.sina.com.cn/bond/quotes/sh155255.html
- 限量: 单次返回指定 symbol 的可转债-债券概况数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债-债券概况

接口: bond_cb_summary_sina

目标地址: https://money.finance.sina.com.cn/bond/quotes/sh155255.html

描述: 新浪财经-债券-可转债-债券概况

限量: 单次返回指定 symbol 的可转债-债券概况数据

输入参数

| 名称     | 类型  | 描述                            |
|--------|-----|-------------------------------|
| symbol | str | symbol="sh155255"; 带市场标识的转债代码 |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

bond_cb_summary_sina_df = ak.bond_cb_summary_sina(symbol="sh155255")
print(bond_cb_summary_sina_df)
```

数据示例

```
        item       value
0       债券类型       普通企业债
1       计息方式        固定利率
2       付息方式       周期性付息
3    票面利率（%）        5.50
4      每年付息日       03-20
5    发行价格（元）         100
6   发行规模（亿元）          17
7    债券面值（元）         100
8    债券年限（年）           5
9       到期日期  2024-03-20
10     全价（元）          --
11   剩余年限（年）        0.62
12  到期收益率（%）          --
13      修正久期          --
14        凸性          --
```
