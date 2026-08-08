---
title: "spot_silver_benchmark_sge - 上海银基准价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_silver_benchmark_sge

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 上海黄金交易所 > 上海银基准价
- 描述: 上海黄金交易所-数据资讯-上海银基准价-历史数据
- 目标地址: https://www.sge.com.cn/sjzx/shyjzj
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上海银基准价

接口: spot_silver_benchmark_sge

目标地址: https://www.sge.com.cn/sjzx/shyjzj

描述: 上海黄金交易所-数据资讯-上海银基准价-历史数据

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

spot_silver_benchmark_sge_df = ak.spot_silver_benchmark_sge()
print(spot_silver_benchmark_sge_df)
```

数据示例

```
      交易时间     晚盘价     早盘价
0    2019-10-13  4286.0  4284.0
1    2019-10-14  4286.0  4301.0
2    2019-10-15  4222.0  4270.0
3    2019-10-16  4261.0  4244.0
4    2019-10-17  4271.0  4271.0
..          ...     ...     ...
953  2023-09-10  5776.0  5773.0
954  2023-09-11  5773.0  5798.0
955  2023-09-12  5783.0  5791.0
956  2023-09-13  5890.0  5881.0
957  2023-09-14  5870.0  5928.0
[958 rows x 3 columns]
```
