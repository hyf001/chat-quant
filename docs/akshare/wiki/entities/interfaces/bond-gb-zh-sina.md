---
title: "bond_gb_zh_sina - 中国国债收益率行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_gb_zh_sina

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中国国债收益率行情
- 描述: 新浪财经-债券-中国国债收益率行情数据
- 目标地址: https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html
- 限量: 返回最近 1000 个交易日的数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 中国国债收益率行情

接口: bond_gb_zh_sina

目标地址: https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html

描述: 新浪财经-债券-中国国债收益率行情数据

限量: 返回最近 1000 个交易日的数据

输入参数

| 名称     | 类型  | 描述                                                                                                                                   |
|--------|-----|--------------------------------------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="中国10年期国债"; choice of {"中国1年期国债", "中国2年期国债", "中国3年期国债", "中国5年期国债", "中国7年期国债", "中国10年期国债", "中国15年期国债", "中国20年期国债", "中国30年期国债"} |

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

bond_gb_zh_sina_df = ak.bond_gb_zh_sina(symbol="中国10年期国债")
print(bond_gb_zh_sina_df)
```

数据示例

```
           date   open   high    low  close  volume
0    2022-02-28  2.788  2.855  2.776  2.789       0
1    2022-03-01  2.789  2.847  2.785  2.816       0
2    2022-03-02  2.816  2.830  2.816  2.822       0
3    2022-03-03  2.822  2.843  2.821  2.842       0
4    2022-03-04  2.842  2.843  2.825  2.831       0
..          ...    ...    ...    ...    ...     ...
995  2026-01-28  1.824  1.875  1.809  1.810       0
996  2026-01-29  1.810  1.839  1.793  1.809       0
997  2026-01-30  1.808  1.839  1.794  1.804       0
998  2026-02-02  1.804  1.831  1.798  1.810       0
999  2026-02-03  1.810  1.824  1.798  1.816       0
[1000 rows x 6 columns]
```
