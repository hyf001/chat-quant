---
title: "bond_cb_index_jsl - 集思录可转债等权指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cb_index_jsl

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 集思录可转债等权指数
- 描述: 可转债-集思录可转债等权指数
- 目标地址: https://www.jisilu.cn/web/data/cb/index
- 限量: 单次返回所有历史数据数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

### 集思录可转债等权指数

接口: bond_cb_index_jsl

目标地址: https://www.jisilu.cn/web/data/cb/index

描述: 可转债-集思录可转债等权指数

限量: 单次返回所有历史数据数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称                  | 类型      | 描述        |
|---------------------|---------|-----------|
| price_dt            | object  | 日期        |
| price               | float64 | 指数        |
| amount              | float64 | 剩余规模(亿元)  |
| volume              | float64 | 成交额(亿元)   |
| count               | int64   | 数量        |
| increase_val        | float64 | 涨跌        |
| increase_rt         | float64 | 涨幅        |
| avg_price           | float64 | 平均价格(元)   |
| mid_price           | float64 | 中位数价格(元)  |
| mid_convert_value   | float64 | 中位数转股价值   |
| avg_dblow           | float64 | 平均双底      |
| avg_premium_rt      | float64 | 平均溢价率     |
| mid_premium_rt      | float64 | 中位数溢价率    |
| avg_ytm_rt          | float64 | 平均收益率     |
| turnover_rt         | float64 | 换手率       |
| price_90            | int64   | >90       |
| price_90_100        | int64   | 90~100    |
| price_100_110       | int64   | 100~110   |
| price_110_120       | int64   | 110~120   |
| price_120_130       | int64   | 120~130   |
| price_130           | int64   | >130      |
| increase_rt_90      | float64 | >90涨幅     |
| increase_rt_90_100  | float64 | 90~100涨幅  |
| increase_rt_100_110 | float64 | 100~110涨幅 |
| increase_rt_110_120 | float64 | 110~120涨幅 |
| increase_rt_120_130 | float64 | 120~130涨幅 |
| increase_rt_130     | float64 | >130涨幅    |
| idx_price           | float64 | 沪深300指数   |
| idx_increase_rt     | float64 | 沪深300指数涨幅 |

接口示例

```python
import akshare as ak

bond_cb_index_jsl_df = ak.bond_cb_index_jsl()
print(bond_cb_index_jsl_df)
```

数据示例

```
        price_dt     price  ...  idx_price  idx_increase_rt
0     2017-12-29  1000.000  ...   4030.850             0.30
1     2018-01-02  1008.831  ...   4087.400             1.40
2     2018-01-03  1018.808  ...   4111.390             0.59
3     2018-01-04  1024.344  ...   4128.810             0.42
4     2018-01-05  1034.655  ...   4138.750             0.24
...          ...       ...  ...        ...              ...
1146  2022-09-19  1997.231  ...   3928.000            -0.12
1147  2022-09-20  2012.310  ...   3932.836             0.12
1148  2022-09-21  2019.373  ...   3903.735            -0.74
1149  2022-09-22  2017.313  ...   3869.344            -0.88
1150  2022-09-23  1998.653  ...   3856.021            -0.34
```
