---
title: "index_hist_sw - 申万指数历史行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_hist_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 申万指数历史行情
- 描述: 申万宏源研究-指数发布-指数详情-指数历史数据
- 目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801002&name=申万中小
- 限量: 该接口返回指定 symbol 和 period 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 申万指数历史行情

接口: index_hist_sw

目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801002&name=申万中小

描述: 申万宏源研究-指数发布-指数详情-指数历史数据

限量: 该接口返回指定 symbol 和 period 的数据

输入参数

| 名称     | 类型  | 描述                                               |
|--------|-----|--------------------------------------------------|
| symbol | str | symbol="801030"; 指数代码                            |
| period | str | period="day"; choice of {"day", "week", "month"} |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 代码  | object  | -   |
| 日期  | object  | -   |
| 收盘  | float64 | -   |
| 开盘  | float64 | -   |
| 最高  | float64 | -   |
| 最低  | float64 | -   |
| 成交量 | float64 | -   |
| 成交额 | float64 | -   |

接口示例

```python
import akshare as ak

index_hist_sw_df = ak.index_hist_sw(symbol="801193", period="day")
print(index_hist_sw_df)
```

数据示例

```
        代码     日期       收盘  ...     最低        成交量          成交额
0     801193  1999-12-30  1000.00  ...  1000.00    0.007658     0.084756
1     801193  2000-01-04  1035.54  ...  1000.64    0.017623     0.199261
2     801193  2000-01-05  1050.67  ...  1023.45    0.033997     0.391641
3     801193  2000-01-06  1096.88  ...  1031.74    0.057862     0.681682
4     801193  2000-01-07  1127.42  ...  1091.98    0.110529     1.353346
...      ...         ...      ...  ...      ...         ...          ...
4081  801193  2024-10-16  6271.85  ...  6103.77   81.423515   849.555269
4082  801193  2024-10-17  6224.13  ...  6166.22   74.126046   793.383788
4083  801193  2024-10-18  6667.02  ...  6152.42  138.155039  1648.638901
4084  801193  2024-10-21  6532.56  ...  6441.85  103.932491  1157.084810
4085  801193  2024-10-22  6591.44  ...  6472.62   78.312127   848.761688
[4086 rows x 8 columns]
```
