---
title: "index_global_hist_em - 全球指数-历史行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_global_hist_em

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 全球指数 > 全球指数-历史行情数据-东财
- 描述: 东方财富网-行情中心-全球指数-历史行情数据
- 目标地址: https://quote.eastmoney.com/gb/zsUDI.html
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全球指数-历史行情数据-东财

接口: index_global_hist_em

目标地址: https://quote.eastmoney.com/gb/zsUDI.html

描述: 东方财富网-行情中心-全球指数-历史行情数据

输入参数

| 名称     | 类型  | 描述                                               |
|--------|-----|--------------------------------------------------|
| symbol | str | symbol="美元指数"; 可以通过 ak.index_global_spot_em() 获取 |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | -       |
| 代码  | object  | -       |
| 名称  | object  | -       |
| 今开  | float64 | -       |
| 最新价 | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 振幅  | float64 | 主要单位: % |

接口示例

```python
import akshare as ak

index_global_hist_em_df = ak.index_global_hist_em(symbol="美元指数")
print(index_global_hist_em_df)
```

数据示例

```
          日期   代码    名称     今开     最新价   最高     最低    振幅
0      1986-01-09  UDI  美元指数  124.18  123.21  124.71  122.91  0.00
1      1986-01-10  UDI  美元指数  123.98  124.16  124.27  123.46  0.66
2      1986-01-13  UDI  美元指数  124.82  124.47  125.21  124.23  0.79
3      1986-01-14  UDI  美元指数  124.75  124.67  124.91  124.38  0.43
4      1986-01-15  UDI  美元指数  124.64  124.30  124.64  124.07  0.46
...           ...  ...   ...     ...     ...     ...     ...   ...
10027  2025-03-03  UDI  美元指数  107.38  106.54  107.41  106.42  0.92
10028  2025-03-04  UDI  美元指数  106.55  105.55  106.66  105.52  1.07
10029  2025-03-05  UDI  美元指数  105.56  104.32  105.78  104.26  1.44
10030  2025-03-06  UDI  美元指数  104.34  104.20  104.39  103.74  0.62
10031  2025-03-07  UDI  美元指数  104.23  103.63  104.25  103.55  0.67
[10032 rows x 8 columns]
```
