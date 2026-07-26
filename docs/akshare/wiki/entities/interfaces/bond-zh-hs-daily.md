---
title: "bond_zh_hs_daily - 历史行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_hs_daily

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深债券 > 历史行情数据
- 描述: 新浪财经-债券-沪深债券-历史行情数据, 历史数据按日频率更新
- 目标地址: https://money.finance.sina.com.cn/bond/quotes/sh019315.html
- 限量: 单次返回具体某个沪深转债的所有历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情数据

接口: bond_zh_hs_daily

目标地址: https://money.finance.sina.com.cn/bond/quotes/sh019315.html

描述: 新浪财经-债券-沪深债券-历史行情数据, 历史数据按日频率更新

限量: 单次返回具体某个沪深转债的所有历史行情数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="sh010107" |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| date   | object  | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | float64 | -   |

接口示例

```python
import akshare as ak

bond_zh_hs_daily_df = ak.bond_zh_hs_daily(symbol="sh010107")
print(bond_zh_hs_daily_df)
```

数据示例

```
            date     open     high      low    close    volume
0     2001-08-20  101.255  102.835  101.255  102.695  60765500
1     2001-08-21  102.743  103.213  102.683  103.133  19927710
2     2001-08-22  103.332  103.402  103.022  103.222  13132740
3     2001-08-23  103.260  103.300  103.080  103.110   9544530
4     2001-08-24  103.158  103.158  102.908  102.958   7068480
          ...      ...      ...      ...      ...       ...
4801  2021-07-26  100.030  100.060  100.000  100.010   1757900
4802  2021-07-27  100.010  100.030  100.000  100.030   1635540
4803  2021-07-28  100.010  100.030  100.000  100.020   1425370
4804  2021-07-29  100.000  100.020  100.000  100.010    244680
4805  2021-07-30  100.000  100.010   99.990  100.010    150850
[4806 rows x 6 columns]
```
