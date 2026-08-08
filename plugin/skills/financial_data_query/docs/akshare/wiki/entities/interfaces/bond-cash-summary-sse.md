---
title: "bond_cash_summary_sse - 债券现券市场概览"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cash_summary_sse

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 上交所债券 > 债券现券市场概览
- 描述: 上登债券信息网-市场数据-市场统计-市场概览-债券现券市场概览
- 目标地址: https://bond.sse.com.cn/data/statistics/overview/bondow/
- 限量: 单次返回指定交易日的债券现券市场概览数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 债券现券市场概览

接口: bond_cash_summary_sse

目标地址: https://bond.sse.com.cn/data/statistics/overview/bondow/

描述: 上登债券信息网-市场数据-市场统计-市场概览-债券现券市场概览

限量: 单次返回指定交易日的债券现券市场概览数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date='20200111' |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 债券现货 | object  | -        |
| 托管只数 | int64   | -        |
| 托管市值 | float64 | 注意单位: 亿元 |
| 托管面值 | float64 | 注意单位: 亿元 |
| 数据日期 | object  | -        |

接口示例

```python
import akshare as ak

bond_cash_summary_sse_df = ak.bond_cash_summary_sse(date='20210111')
print(bond_cash_summary_sse_df)
```

数据示例

```
        债券现货   托管只数       托管市值       托管面值        数据日期
0         国债    193    6815.47    6758.46  2021-01-11
1        地方债   5317    6713.69    6709.22  2021-01-11
2        金融债     19     989.76     970.70  2021-01-11
3        企业债   2233    7497.15    7433.93  2021-01-11
4  非公开发行公司债券   4974   43857.61   44191.15  2021-01-11
5       可交换债     57    1352.85    1280.10  2021-01-11
6   公开发行公司债券   3393   46382.41   46644.57  2021-01-11
7     可转换公司债    142    3655.79    3179.81  2021-01-11
8     资产支持证券   4141   14838.03   14829.47  2021-01-11
9         合计  20469  132102.75  131997.40  2021-01-11
```
