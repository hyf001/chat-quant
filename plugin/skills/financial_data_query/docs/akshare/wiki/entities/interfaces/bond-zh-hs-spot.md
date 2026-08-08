---
title: "bond_zh_hs_spot - 实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_hs_spot

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深债券 > 实时行情数据
- 描述: 新浪财经-债券-沪深债券-实时行情数据
- 目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_z
- 限量: 单次返回所有沪深债券的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据

接口: bond_zh_hs_spot

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_z

描述: 新浪财经-债券-沪深债券-实时行情数据

限量: 单次返回所有沪深债券的实时行情数据

输入参数

| 名称         | 类型  | 描述                                |
|------------|-----|-----------------------------------|
| start_page | str | start_page="1"; 开始获取的页面，每页 80 条数据 |
| end_page   | str | end_page="10"; 结束获取的页面，每页 80 条数据  |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 代码  | object  | -       |
| 名称  | object  | -       |
| 最新价 | float64 | -       |
| 涨跌额 | float64 | -       |
| 涨跌幅 | float64 | -       |
| 买入  | float64 | -       |
| 卖出  | float64 | -       |
| 昨收  | float64 | -       |
| 今开  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 成交量 | int64   | 注意单位: 手 |
| 成交额 | int64   | 注意单位: 万 |

接口示例

```python
import akshare as ak

bond_zh_hs_spot_df = ak.bond_zh_hs_spot(start_page="1", end_page="5")
print(bond_zh_hs_spot_df)
```

数据示例

```
      代码      名称      最新价   涨跌额  ...   最高       最低    成交量   成交额
0    sh010107   21国债⑺  100.010  0.00  ...    0.000    0.000      0        0
1    sh010303   03国债⑶  100.010  0.00  ...    0.000    0.000      0        0
2    sh010504   05国债⑷  102.396  0.05  ...  102.397  102.395  10390  1063895
3    sh010512   05国债⑿  100.050  0.00  ...    0.000    0.000      0        0
4    sh010609   06国债⑼  100.000  0.00  ...    0.000    0.000      0        0
..        ...     ...      ...   ...  ...      ...      ...    ...      ...
395  sh020418  21贴债21   99.550  0.00  ...    0.000    0.000      0        0
396  sh020419  21贴债22   99.560  0.00  ...    0.000    0.000      0        0
397  sh020420  21贴债23   99.570  0.00  ...    0.000    0.000      0        0
398  sh020421  21贴债24   99.560  0.00  ...    0.000    0.000      0        0
399  sh020422  21贴债25   99.030  0.00  ...    0.000    0.000      0        0
[400 rows x 13 columns]
```
