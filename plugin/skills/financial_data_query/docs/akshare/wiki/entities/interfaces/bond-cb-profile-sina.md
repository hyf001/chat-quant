---
title: "bond_cb_profile_sina - 可转债-详情资料"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cb_profile_sina

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债-详情资料
- 描述: 新浪财经-债券-可转债-详情资料
- 目标地址: https://money.finance.sina.com.cn/bond/info/sz128039.html
- 限量: 单次返回指定 symbol 的可转债-详情资料数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债-详情资料

接口: bond_cb_profile_sina

目标地址: https://money.finance.sina.com.cn/bond/info/sz128039.html

描述: 新浪财经-债券-可转债-详情资料

限量: 单次返回指定 symbol 的可转债-详情资料数据

输入参数

| 名称     | 类型  | 描述                            |
|--------|-----|-------------------------------|
| symbol | str | symbol="sz128039"; 带市场标识的转债代码 |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

bond_cb_profile_sina_df = ak.bond_cb_profile_sina(symbol="sz128039")
print(bond_cb_profile_sina_df)
```

数据示例

```
        item                                              value
0       债券名称                          2018年三力士股份有限公司公开发行可转换公司债券
1       债券简称                                               三力转债
2       债券代码                                           sz128039
3       债券类型                                             可转换企业债
4    债券面值（元）                                                100
5    债券年限（年）                                                  6
6    票面利率（%）                                                 --
7        到期日                                         2024-06-08
8        兑付日                                         2024-06-08
9        摘牌日                                                 --
10      计息方式                                               递进利率
11      利率说明  本次发行的可转债票面利率第一年0.3%、第二年0.5%、第三年1.0%、第四年1.3%、第五...
12      付息方式                                              周期性付息
13      起息日期                                         2018-06-08
14      止息日期                                         2024-06-07
15      付息日期                                              06-08
16     年付息次数                                                  1
17   发行价格（元）                                                100
18  发行规模（亿元）                                                6.2
19      发行日期                                         2018-06-08
20      上市日期                                         2018-06-29
21      上市场所                                              深圳交易所
22      信用等级                                                 A+
23  内部信用增级方式                                                 --
24  外部信用增级方式                                                 --
```
