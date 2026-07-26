---
title: "fund_portfolio_hold_em - 基金持仓"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_portfolio_hold_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金持仓
- 描述: 天天基金网-基金档案-投资组合-基金持仓
- 目标地址: https://fundf10.eastmoney.com/ccmx_000001.html
- 限量: 单次返回指定 symbol 和 date 的所有持仓数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金持仓

接口: fund_portfolio_hold_em

目标地址: https://fundf10.eastmoney.com/ccmx_000001.html

描述: 天天基金网-基金档案-投资组合-基金持仓

限量: 单次返回指定 symbol 和 date 的所有持仓数据

输入参数

| 名称     | 类型  | 描述                                                       |
|--------|-----|----------------------------------------------------------|
| symbol | str | symbol="000001"; 基金代码, 可以通过调用 **ak.fund_name_em()** 接口获取 |
| date   | str | date="2024"; 指定年份, 传入空字符串 `""` 时返回最新可用年份数据          |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 序号    | int64   | -        |
| 股票代码  | object  | -        |
| 股票名称  | object  | -        |
| 占净值比例 | float64 | 注意单位: %  |
| 持股数   | float64 | 注意单位: 万股 |
| 持仓市值  | float64 | 注意单位: 万元 |
| 季度    | object  | -        |

接口示例

```python
import akshare as ak

fund_portfolio_hold_em_df = ak.fund_portfolio_hold_em(symbol="000001", date="2024")
print(fund_portfolio_hold_em_df)
```

数据示例

```
   序号 股票代码  股票名称  占净值比例 持股数 持仓市值              季度
0   1  002025   航天电器   3.46  209.92  7947.67  2024年1季度股票投资明细
1   2  600862   中航高科   3.24  380.43  7441.16  2024年1季度股票投资明细
2   3  600941   中国移动   2.86   62.11  6568.75  2024年1季度股票投资明细
3   4  300395    菲利华   2.80  216.80  6417.42  2024年1季度股票投资明细
4   5  300034   钢研高纳   2.69  403.16  6168.33  2024年1季度股票投资明细
5   6  002371   北方华创   2.67   20.07  6134.03  2024年1季度股票投资明细
6   7  002475   立讯精密   2.30  179.77  5287.04  2024年1季度股票投资明细
7   8  600276   恒瑞医药   2.22  111.06  5105.35  2024年1季度股票投资明细
8   9  600522   中天科技   1.99  325.78  4570.69  2024年1季度股票投资明细
9  10  000100  TCL科技   1.82  893.37  4172.03  2024年1季度股票投资明细
```
