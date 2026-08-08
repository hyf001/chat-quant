---
title: "spot_golden_benchmark_sge - 上海金基准价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_golden_benchmark_sge

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 上海黄金交易所 > 上海金基准价
- 描述: 上海黄金交易所-数据资讯-上海金基准价-历史数据
- 目标地址: https://www.sge.com.cn/sjzx/jzj
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上海金基准价

接口: spot_golden_benchmark_sge

目标地址: https://www.sge.com.cn/sjzx/jzj

描述: 上海黄金交易所-数据资讯-上海金基准价-历史数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 交易时间 | object  | -   |
| 晚盘价  | float64 | -   |
| 早盘价  | float64 | -   |

接口示例

```python
import akshare as ak

spot_golden_benchmark_sge_df = ak.spot_golden_benchmark_sge()
print(spot_golden_benchmark_sge_df)
```

数据示例

```
     交易时间     晚盘价     早盘价
0     2016-04-18  257.29  256.92
1     2016-04-19  259.97  261.15
2     2016-04-20  261.82  260.39
3     2016-04-21  260.41  261.32
4     2016-04-24  258.80  258.42
          ...     ...     ...
1801  2023-09-10  467.92  468.49
1802  2023-09-11  468.62  468.20
1803  2023-09-12  470.00  469.14
1804  2023-09-13  474.58  474.68
1805  2023-09-14  470.43  479.08
[1806 rows x 3 columns]
```
