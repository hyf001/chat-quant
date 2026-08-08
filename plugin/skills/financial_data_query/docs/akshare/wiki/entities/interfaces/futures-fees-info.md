---
title: "futures_fees_info - 期货交易费用参照表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_fees_info

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 期货交易费用参照表
- 描述: openctp 期货交易费用参照表
- 目标地址: http://openctp.cn/fees.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 期货交易费用参照表

接口: futures_fees_info

目标地址: http://openctp.cn/fees.html

描述: openctp 期货交易费用参照表

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称          | 类型      | 描述 |
|-------------|---------|----|
| 交易所         | object  | -  |
| 合约代码        | object  | -  |
| 合约名称        | object  | -  |
| 品种代码        | object  | -  |
| 品种名称        | object  | -  |
| 合约乘数        | int64   | -  |
| 最小跳动        | float64 | -  |
| 开仓费率（按金额）   | float64 | -  |
| 开仓费用（按手）    | float64 | -  |
| 平仓费率（按金额）   | float64 | -  |
| 平仓费用（按手）    | float64 | -  |
| 平今费率（按金额）   | float64 | -  |
| 平今费用（按手）    | float64 | -  |
| 做多保证金率（按金额） | float64 | -  |
| 做多保证金（按手）   | int64   | -  |
| 做空保证金率（按金额） | float64 | -  |
| 做空保证金（按手）   | int64   | -  |
| 上日结算价       | float64 | -  |
| 上日收盘价       | float64 | -  |
| 最新价         | float64 | -  |
| 成交量         | int64   | -  |
| 持仓量         | int64   | -  |
| 1手开仓费用      | float64 | -  |
| 1手平仓费用      | float64 | -  |
| 1手平今费用      | float64 | -  |
| 做多1手保证金     | float64 | -  |
| 做空1手保证金     | float64 | -  |
| 1Tick平仓盈亏   | float64 | -  |
| 2Tick平仓盈亏   | float64 | -  |
| 1Tick平仓收益率  | object  | -  |
| 2Tick平仓收益率  | object  | -  |
| 1Tick平今盈亏   | float64 | -  |
| 2Tick平今盈亏   | float64 | -  |
| 1Tick平今收益率  | object  | -  |
| 2Tick平今收益率  | object  | -  |
| 更新时间        | object  | -  |

接口示例

```python
import akshare as ak

futures_fees_info_df = ak.futures_fees_info()
print(futures_fees_info_df)
```

数据示例

```
      交易所    合约代码    合约名称  ... 1Tick平今收益率 2Tick平今收益率                 更新时间
0    CZCE   AP410   苹果10月  ...    -0.147%    -0.049%  2024-07-05 15:12:27
1    CZCE   AP411   苹果11月  ...    -0.153%    -0.051%  2024-07-05 15:12:27
2    CZCE   AP412   苹果12月  ...     -0.15%     -0.05%  2024-07-05 15:12:27
3    CZCE   AP501    苹果1月  ...    -0.148%     -0.05%  2024-07-05 15:12:27
4    CZCE   AP503    苹果3月  ...    -0.148%    -0.049%  2024-07-05 15:12:27
..    ...     ...     ...  ...        ...        ...                  ...
764  SHFE  zn2502  zn2502  ...     0.138%     0.295%  2024-07-05 15:12:27
765  SHFE  zn2503  zn2503  ...     0.138%     0.295%  2024-07-05 15:12:27
766  SHFE  zn2504  zn2504  ...     0.138%     0.295%  2024-07-05 15:12:27
767  SHFE  zn2505  zn2505  ...     0.138%     0.296%  2024-07-05 15:12:27
768  SHFE  zn2506  zn2506  ...     0.138%     0.295%  2024-07-05 15:12:27
[769 rows x 36 columns]
```
