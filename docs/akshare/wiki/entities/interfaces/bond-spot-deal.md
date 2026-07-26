---
title: "bond_spot_deal - 现券市场成交行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_spot_deal

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 中国债券市场行情数据 > 现券市场成交行情
- 描述: 中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场成交行情
- 目标地址: https://www.chinamoney.com.cn/chinese/mkdatabond/
- 限量: 单次返回所有即期数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 现券市场成交行情

接口: bond_spot_deal

目标地址: https://www.chinamoney.com.cn/chinese/mkdatabond/

描述: 中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场成交行情

限量: 单次返回所有即期数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 债券简称  | object  | -        |
| 成交净价  | float64 | 注意单位: 元  |
| 最新收益率 | float64 | 注意单位: %  |
| 涨跌    | float64 | 注意单位: BP |
| 加权收益率 | float64 | 注意单位: %  |
| 交易量   | float64 | 注意单位: 亿  |

接口示例

```python
import akshare as ak

bond_spot_deal_df = ak.bond_spot_deal()
print(bond_spot_deal_df)
```

数据示例

```
                       债券简称    成交净价   最新收益率     涨跌   加权收益率  交易量
0                  23附息国债26  103.20  2.3000  -0.80  2.3168  NaN
1                  23附息国债18  101.31  2.3650  -0.80  2.3733  NaN
2                    20人民财险  101.15  4.1810  -0.23  4.1810  NaN
3              23无锡建投MTN003  100.87  2.7369    NaN  2.7369  NaN
4     22国新控股MTN005(能源保供特别债)  100.88  2.5900    NaN  2.5900  NaN
                     ...     ...     ...    ...     ...  ...
1775           22滨江房产MTN001  100.64  3.2700  -0.01  3.2700  NaN
1776            23建设银行CD059   97.44  1.8492   1.00  1.8492  NaN
1777            23华夏银行CD085   97.43  1.8505   1.00  1.8505  NaN
1778            24招商银行CD015   97.84  2.2099    NaN  2.2100  NaN
1779               24贴现国债13   99.88  1.7497  65.65  1.7497  NaN
[1780 rows x 6 columns]
```
