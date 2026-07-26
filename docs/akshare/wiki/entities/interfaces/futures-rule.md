---
title: "futures_rule - 期货规则-交易日历表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_rule

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 期货规则-交易日历表
- 描述: 国泰君安期货-交易日历数据表
- 目标地址: https://www.gtjaqh.com/pc/calendar.html
- 限量: 单次返回指定交易日所有合约的交易日历数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 期货规则-交易日历表

接口: futures_rule

目标地址: https://www.gtjaqh.com/pc/calendar.html

描述: 国泰君安期货-交易日历数据表

限量: 单次返回指定交易日所有合约的交易日历数据

输入参数

| 名称   | 类型  | 描述                                 |
|------|-----|------------------------------------|
| date | str | date="20231205"; 需要指定为交易日, 且是近期的日期 |

输出参数

| 名称          | 类型      | 描述      |
|-------------|---------|---------|
| 交易所         | object  | -       |
| 品种          | object  | -       |
| 代码          | object  | -       |
| 交易保证金比例     | float64 | 注意单位: % |
| 涨跌停板幅度      | float64 | 注意单位: % |
| 合约乘数        | int64   | -       |
| 最小变动价位      | float64 | -       |
| 限价单每笔最大下单手数 | int64   | -       |
| 特殊合约参数调整    | object  | -       |
| 调整备注        | object  | -       |

接口示例

```python
import akshare as ak

futures_rule_df = ak.futures_rule(date="20231205")
print(futures_rule_df)
```

数据示例

```
     交易所          品种  ...                                      特殊合约参数调整  调整备注
0    上期所           铜  ...  CU2312合约交易保证金比例为20.0%; CU2401合约交易保证金比例为15.0%   NaN
1    上期所         铜期权  ...    期权卖方交易保证金中涉及标的期货合约的公司交易保证金按照对应的期货合约保证金标准收取   NaN
2    上期所           铝  ...  AL2312合约交易保证金比例为20.0%; AL2401合约交易保证金比例为15.0%   NaN
3    上期所         铝期权  ...    期权卖方交易保证金中涉及标的期货合约的公司交易保证金按照对应的期货合约保证金标准收取   NaN
4    上期所           锌  ...  ZN2312合约交易保证金比例为20.0%; ZN2401合约交易保证金比例为15.0%   NaN
..   ...         ...  ...                                           ...   ...
117  中金所  中证1000股指期权  ...                       保证金调整系数为14%，最低保障系数为0.50   NaN
118  中金所       2年期国债  ...                          TS2312合约交易保证金比例为1.3%   NaN
119  中金所       5年期国债  ...                          TF2312合约交易保证金比例为2.5%   NaN
120  中金所      30年期国债  ...                          TL2312合约交易保证金比例为6.5%   NaN
121  中金所      10年期国债  ...                           T2312合约交易保证金比例为3.5%   NaN
[122 rows x 10 columns]
```
