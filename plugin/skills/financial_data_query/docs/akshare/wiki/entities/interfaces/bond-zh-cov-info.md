---
title: "bond_zh_cov_info - 可转债详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_zh_cov_info

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 沪深可转债 > 可转债详情
- 描述: 东方财富网-数据中心-新股数据-可转债详情
- 目标地址: https://data.eastmoney.com/kzz/detail/123121.html
- 限量: 单次返回指定 symbol 的可转债详情数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债详情

接口: bond_zh_cov_info

目标地址: https://data.eastmoney.com/kzz/detail/123121.html

描述: 东方财富网-数据中心-新股数据-可转债详情

限量: 单次返回指定 symbol 的可转债详情数据

输入参数

| 名称        | 类型  | 描述                                                                                  |
|-----------|-----|-------------------------------------------------------------------------------------|
| symbol    | str | symbol="123121"; 可转债代码                                                              |
| indicator | str | indicator="基本信息"; choice of {"基本信息", "中签号", "筹资用途", "重要日期"}, 其中 "可转债重要条款" 在 "基本信息中" |

输出参数

| 名称   | 类型     | 描述        |
|------|--------|-----------|
| 债券代码 | object | 返回 67 个字段 |

接口示例

```python
import akshare as ak

bond_zh_cov_info_df = ak.bond_zh_cov_info(symbol="123121", indicator="基本信息")
print(bond_zh_cov_info_df)
```

数据示例

```
  SECURITY_CODE   SECUCODE TRADE_MARKET  ... IS_CONVERT_STOCK IS_REDEEM IS_SELLBACK
0        123121  123121.SZ       CNSESZ  ...                是         是           是
```
