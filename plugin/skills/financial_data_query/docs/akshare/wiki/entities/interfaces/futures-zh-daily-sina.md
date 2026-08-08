---
title: "futures_zh_daily_sina - 内盘-历史行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_zh_daily_sina

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-历史行情数据-新浪
- 描述: 新浪财经-期货-日频数据
- 目标地址: https://finance.sina.com.cn/futures/quotes/V2105.shtml
- 限量: 单次返回指定 symbol 的所有日频数据; 期货连续合约为 品种代码+0，比如螺纹钢连续合约为 RB0;
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-历史行情数据-新浪

接口: futures_zh_daily_sina

目标地址: https://finance.sina.com.cn/futures/quotes/V2105.shtml

描述: 新浪财经-期货-日频数据

限量: 单次返回指定 symbol 的所有日频数据; 期货连续合约为 品种代码+0，比如螺纹钢连续合约为 RB0;

输入参数

| 名称     | 类型  | 描述                                                                    |
|--------|-----|-----------------------------------------------------------------------|
| symbol | str | symbol="RB0"; 具体合约可以通过 ak.match_main_contract(symbol="shfe") 获取或者访问网页 |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| date   | object  | -   |
| open   | float64 | 开盘价 |
| high   | float64 | 最高价 |
| low    | float64 | 最低价 |
| close  | float64 | 收盘价 |
| volume | int64   | 成交量 |
| hold   | int64   | 持仓量 |
| settle | float64 | 结算价 |

接口示例-连续

```python
import akshare as ak

futures_zh_daily_sina_df = ak.futures_zh_daily_sina(symbol="RB0")
print(futures_zh_daily_sina_df)
```

数据示例-连续

```
            date    open    high     low   close   volume     hold  settle
0     2009-03-27  3550.0  3663.0  3513.0  3561.0   354590    45548     0.0
1     2009-03-30  3550.0  3580.0  3528.0  3544.0   145168    48380     0.0
2     2009-03-31  3538.0  3566.0  3531.0  3549.0    70592    44714     0.0
3     2009-04-01  3560.0  3561.0  3543.0  3547.0    28100    42076     0.0
4     2009-04-02  3545.0  3548.0  3456.0  3473.0   235446    68888     0.0
          ...     ...     ...     ...     ...      ...      ...     ...
3644  2024-03-28  3470.0  3504.0  3441.0  3481.0  2312398  1433991  3473.0
3645  2024-03-29  3475.0  3486.0  3405.0  3412.0  2015960  1299182  3448.0
3646  2024-04-01  3400.0  3456.0  3368.0  3456.0  1622273  1141786  3405.0
3647  2024-04-02  3459.0  3493.0  3431.0  3463.0  1217107  1026768  3463.0
3648  2024-04-03  3500.0  3540.0  3462.0  3463.0  1620584  1674662  3509.0
[3649 rows x 8 columns]
```

接口示例-合约

```python
import akshare as ak

futures_zh_daily_sina_df = ak.futures_zh_daily_sina(symbol="RB2410")
print(futures_zh_daily_sina_df)
```

数据示例-合约

```
           date    open    high     low   close   volume     hold  settle
0    2023-10-17  3600.0  3650.0  3600.0  3631.0     1140      893  3631.0
1    2023-10-18  3636.0  3636.0  3593.0  3602.0     1050     1642  3615.0
2    2023-10-19  3612.0  3633.0  3590.0  3623.0      818     2070  3608.0
3    2023-10-20  3630.0  3638.0  3580.0  3588.0     1554     3088  3606.0
4    2023-10-23  3580.0  3595.0  3555.0  3568.0     2058     4175  3570.0
..          ...     ...     ...     ...     ...      ...      ...     ...
110  2024-03-28  3487.0  3535.0  3461.0  3509.0   799059  1302305  3493.0
111  2024-03-29  3505.0  3507.0  3443.0  3450.0   837570  1488697  3475.0
112  2024-04-01  3439.0  3497.0  3408.0  3492.0  1404806  1569587  3445.0
113  2024-04-02  3498.0  3546.0  3482.0  3506.0  1694801  1651838  3512.0
114  2024-04-03  3500.0  3540.0  3462.0  3463.0  1620584  1674662  3509.0
[115 rows x 8 columns]
```
