---
title: "option_sse_daily_sina - 期权行情日数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_daily_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 期权行情日数据
- 描述: 期权行情日数据
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回期权行情日数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期权行情日数据

接口: option_sse_daily_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 期权行情日数据

限量: 单次返回期权行情日数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="10002273" |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 时间  | object  | -   |
| 开盘  | float64 | -   |
| 最高  | float64 | -   |
| 最低  | float64 | -   |
| 收盘  | float64 | -   |
| 成交  | int64   | -   |

接口示例

```python
import akshare as ak

option_sse_daily_sina_df = ak.option_sse_daily_sina(symbol="10002273")
print(option_sse_daily_sina_df)
```

数据示例

```
     日期      开盘      最高      最低      收盘        成交
0   2020-02-04  0.2200  0.2870  0.2151  0.2850  13729899
1   2020-02-05  0.2868  0.3159  0.2711  0.3010  10716172
2   2020-02-06  0.3050  0.3581  0.2939  0.3420   8849637
3   2020-02-07  0.3265  0.3416  0.3110  0.3410   3538617
4   2020-02-10  0.3251  0.3389  0.3117  0.3390   3569910
5   2020-02-11  0.3402  0.3737  0.3391  0.3621   4518172
6   2020-02-12  0.3600  0.3776  0.3550  0.3721   1020605
7   2020-02-13  0.3756  0.3898  0.3556  0.3610   1956981
8   2020-02-14  0.3662  0.3848  0.3626  0.3833   1130476
9   2020-02-17  0.3800  0.4415  0.3800  0.4359   2606707
10  2020-02-18  0.4250  0.4334  0.4042  0.4121    827370
11  2020-02-19  0.4066  0.4300  0.4051  0.4122    720243
12  2020-02-20  0.4200  0.4666  0.4050  0.4585   2621812
13  2020-02-21  0.4550  0.4799  0.4477  0.4550   1892291
```
