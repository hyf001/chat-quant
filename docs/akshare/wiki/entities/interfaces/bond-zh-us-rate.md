---
title: "bond_zh_us_rate - 中美国债收益率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_us_rate

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中美国债收益率
- 描述: 东方财富网-数据中心-经济数据-中美国债收益率历史数据
- 目标地址: https://data.eastmoney.com/cjsj/zmgzsyl.html
- 限量: 返回 start_date 开始后的所有交易日的数据; 数据从 19901219 开始
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 中美国债收益率

接口: bond_zh_us_rate

目标地址: https://data.eastmoney.com/cjsj/zmgzsyl.html

描述: 东方财富网-数据中心-经济数据-中美国债收益率历史数据

限量: 返回 start_date 开始后的所有交易日的数据; 数据从 19901219 开始

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="19901219" |

输出参数

| 名称            | 类型      | 描述  |
|---------------|---------|-----|
| 日期            | object  | -   |
| 中国国债收益率2年     | float64 | -   |
| 中国国债收益率5年     | float64 | -   |
| 中国国债收益率10年    | float64 | -   |
| 中国国债收益率30年    | float64 | -   |
| 中国国债收益率10年-2年 | float64 | -   |
| 中国GDP年增率      | float64 | -   |
| 美国国债收益率2年     | float64 | -   |
| 美国国债收益率5年     | float64 | -   |
| 美国国债收益率10年    | float64 | -   |
| 美国国债收益率30年    | float64 | -   |
| 美国国债收益率10年-2年 | float64 | -   |
| 美国GDP年增率      | float64 | -   |

接口示例

```python
import akshare as ak

bond_zh_us_rate_df = ak.bond_zh_us_rate(start_date="19901219")
print(bond_zh_us_rate_df)
```

数据示例

```
     日期  中国国债收益率2年  中国国债收益率5年  ...  美国国债收益率30年  美国国债收益率10年-2年  美国GDP年增率
0     1990-12-19        NaN        NaN  ...        8.19           0.79       NaN
1     1990-12-20        NaN        NaN  ...        8.22           0.80       NaN
2     1990-12-21        NaN        NaN  ...        8.28           0.81       NaN
3     1990-12-24        NaN        NaN  ...        8.36           0.85       NaN
4     1990-12-26        NaN        NaN  ...        8.30           0.88       NaN
          ...        ...        ...  ...         ...            ...       ...
8595  2023-11-27     2.4719     2.6012  ...        4.53          -0.45       NaN
8596  2023-11-28     2.4369     2.5762  ...        4.52          -0.39       NaN
8597  2023-11-29     2.4460     2.5840  ...        4.44          -0.37       NaN
8598  2023-11-30     2.4259     2.5691  ...        4.54          -0.36       NaN
8599  2023-12-01     2.4169     2.5665  ...        4.40          -0.34       NaN
[8600 rows x 13 columns]
```
