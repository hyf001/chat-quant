---
title: "macro_germany_trade_adjusted - 贸易帐-季调后"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_germany_trade_adjusted

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 德国宏观 > 贸易帐-季调后
- 描述: 东方财富-数据中心-经济数据一览-德国-贸易帐(季调后)
- 目标地址: https://data.eastmoney.com/cjsj/foreign_1_3.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 贸易帐-季调后

接口: macro_germany_trade_adjusted

目标地址: https://data.eastmoney.com/cjsj/foreign_1_3.html

描述: 东方财富-数据中心-经济数据一览-德国-贸易帐(季调后)

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 前值   | float64 | -   |
| 现值   | float64 | -   |
| 发布日期 | object  | -   |

接口示例

```python
import akshare as ak

macro_germany_trade_adjusted_df = ak.macro_germany_trade_adjusted()
print(macro_germany_trade_adjusted_df)
```

数据示例

```
      时间    前值    现值        发布日期
0    2008年01月  15.5  17.2  2008-03-10
1    2008年02月  17.2  16.3  2008-04-10
2    2008年03月  16.3  16.8  2008-05-09
3    2008年04月  16.8  16.8  2008-06-09
4    2008年05月  16.8  15.3  2008-07-09
..        ...   ...   ...         ...
173  2022年06月   3.2   5.7  2022-08-03
174  2022年07月   5.7   3.4  2022-09-02
175  2022年08月   3.4   1.2  2022-10-05
176  2022年09月   1.2   3.7  2022-11-02
177  2022年10月   3.7   NaN  2022-12-02
```
