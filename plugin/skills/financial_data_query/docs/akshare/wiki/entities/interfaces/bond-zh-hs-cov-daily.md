---
title: "bond_zh_hs_cov_daily - 历史行情数据-日频"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_hs_cov_daily

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 历史行情数据-日频
- 描述: 新浪财经-历史行情数据，日频率更新, 新上的标的需要次日更新数据
- 目标地址: https://biz.finance.sina.com.cn/suggest/lookup_n.php?q=sh110048
- 限量: 单次返回具体某个沪深可转债的所有历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情数据-日频

接口: bond_zh_hs_cov_daily

目标地址: https://biz.finance.sina.com.cn/suggest/lookup_n.php?q=sh110048

描述: 新浪财经-历史行情数据，日频率更新, 新上的标的需要次日更新数据

限量: 单次返回具体某个沪深可转债的所有历史行情数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="sh113542" |

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

bond_zh_hs_cov_daily_df = ak.bond_zh_hs_cov_daily(symbol="sz128039")
print(bond_zh_hs_cov_daily_df)
```

数据示例

```
            date     open     high      low    close   volume
0     2018-06-29   91.470   95.200   89.400   89.500  1456563
1     2018-07-02   90.100   91.000   88.202   88.279   465913
2     2018-07-03   88.400   89.400   88.010   89.400   430800
3     2018-07-04   89.397   89.448   88.515   88.608   215772
4     2018-07-05   88.580   88.690   88.103   88.200   117494
          ...      ...      ...      ...      ...      ...
1370  2024-02-22  108.000  108.555  107.901  108.200   182005
1371  2024-02-23  108.200  109.296  107.600  107.800   125660
1372  2024-02-26  107.800  108.254  107.555  108.099   118131
1373  2024-02-27  107.980  108.222  107.672  107.800    81086
1374  2024-02-28  107.878  108.106  105.847  105.980   149757
[1375 rows x 6 columns]
```
