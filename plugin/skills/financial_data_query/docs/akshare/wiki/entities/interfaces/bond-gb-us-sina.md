---
title: "bond_gb_us_sina - 美国国债收益率行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_gb_us_sina

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 美国国债收益率行情
- 描述: 新浪财经-债券-美国国债收益率行情数据
- 目标地址: https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html
- 限量: 返回最近 1000 个交易日的数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 美国国债收益率行情

接口: bond_gb_us_sina

目标地址: https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html

描述: 新浪财经-债券-美国国债收益率行情数据

限量: 返回最近 1000 个交易日的数据

输入参数

| 名称     | 类型  | 描述                                                                                                                                                                              |
|--------|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="美国10年期国债"; choice of {"美国1月期国债", "美国2月期国债", "美国3月期国债", "美国4月期国债", "美国6月期国债", "美国1年期国债", "美国2年期国债", "美国3年期国债", "美国5年期国债", "美国7年期国债", "美国10年期国债", "美国20年期国债", "美国30年期国债"} |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| date   | object  | -  |
| open   | float64 | -  |
| high   | float64 | -  |
| low    | float64 | -  |
| close  | float64 | -  |
| volume | int64   | -  |

接口示例

```python
import akshare as ak

bond_gb_us_sina_df = ak.bond_gb_us_sina(symbol="美国10年期国债")
print(bond_gb_us_sina_df)
```

数据示例

```
           date    open   high     low   close  volume
0    2022-03-18  2.1550  2.191  2.1330  2.1476       0
1    2022-03-21  2.1476  2.320  2.1476  2.3168       0
2    2022-03-22  2.3110  2.392  2.3110  2.3770       0
3    2022-03-23  2.3860  2.417  2.2860  2.3207       0
4    2022-03-24  2.3080  2.396  2.3040  2.3408       0
..          ...     ...    ...     ...     ...     ...
995  2026-01-28  4.2390  4.273  4.2270  4.2472       0
996  2026-01-29  4.2390  4.271  4.2230  4.2348       0
997  2026-01-30  4.2470  4.279  4.2330  4.2589       0
998  2026-02-02  4.2470  4.283  4.2120  4.2789       0
999  2026-02-03  4.2750  4.299  4.2630  4.2670       0
[1000 rows x 6 columns]
```
