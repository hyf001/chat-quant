---
title: "futures_settle - 内盘-结算参数数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_settle

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-结算参数数据
- 描述: 提供各交易所的结算参数数据，包括保证金、手续费、涨跌停板等参数
- 目标地址: 各交易所网站
- 限量: 单次返回指定日期指定交易所的结算参数数据；暂不支持 DCE
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-结算参数数据

接口: futures_settle

目标地址: 各交易所网站

描述: 提供各交易所的结算参数数据，包括保证金、手续费、涨跌停板等参数

限量: 单次返回指定日期指定交易所的结算参数数据；暂不支持 DCE

输入参数

| 名称     | 类型  | 描述                                                                 |
|--------|-----|--------------------------------------------------------------------|
| date   | str | date="20250117"; 结算参数日期，默认为当前交易日                                   |
| market | str | market="CFFEX"; choice of {"CFFEX", "INE", "CZCE", "SHFE", "GFEX"} |

输出参数

| 名称                       | 类型      | 描述       |
|--------------------------|---------|----------|
| date                     | str     | 结算日期     |
| symbol                   | str     | 合约代码     |
| variety                  | str     | 品种代码     |
| settle_price             | float64 | 结算价      |
| long_margin_ratio        | object  | 多头保证金率   |
| short_margin_ratio       | object  | 空头保证金率   |
| spec_long_margin_ratio   | float64 | 投机多头保证金率 |
| spec_short_margin_ratio  | float64 | 投机空头保证金率 |
| hedge_long_margin_ratio  | float64 | 套保多头保证金率 |
| hedge_short_margin_ratio | float64 | 套保空头保证金率 |
| trade_fee_ratio          | float64 | 交易手续费率   |
| close_today_fee_ratio    | float64 | 平今手续费率   |
| delivery_fee_ratio       | object  | 交割手续费率   |
| is_single_market         | object  | 是否单边市    |
| single_market_days       | object  | 连续单边市天数  |
| limit_ratio              | object  | 涨跌停板幅度   |
| position_limit           | object  | 持仓限额     |
| trade_limit              | object  | 交易限额     |
| rise_limit_rate          | object  | 涨停板比例    |
| fall_limit_rate          | object  | 跌停板比例    |

接口示例

```python
import akshare as ak

futures_settle_df = ak.futures_settle(date="20260119", market="INE")
print(futures_settle_df)
```

数据示例

```
        date  symbol variety  ...  trade_limit rise_limit_rate fall_limit_rate
0   20260119  sc2602      sc  ...         None            None            None
1   20260119  sc2603      sc  ...         None            None            None
2   20260119  sc2604      sc  ...         None            None            None
3   20260119  sc2605      sc  ...         None            None            None
4   20260119  sc2606      sc  ...         None            None            None
..       ...     ...     ...  ...          ...             ...             ...
57  20260119  ec2604      ec  ...         None            None            None
58  20260119  ec2606      ec  ...         None            None            None
59  20260119  ec2608      ec  ...         None            None            None
60  20260119  ec2610      ec  ...         None            None            None
61  20260119  ec2612      ec  ...         None            None            None
[62 rows x 20 columns]
```
