---
title: "index_min_sw - 申万指数分时行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_min_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 申万指数分时行情
- 描述: 申万宏源研究-指数发布-指数详情-指数分时数据
- 目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801001&name=申万中小
- 限量: 该接口返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 申万指数分时行情

接口: index_min_sw

目标地址: https://www.swsresearch.com//institute_sw/allIndex/releasedIndex/releasedetail?code=801001&name=申万中小

描述: 申万宏源研究-指数发布-指数详情-指数分时数据

限量: 该接口返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                               |
|--------|-----|--------------------------------------------------|
| symbol | str | symbol="801030"; 指数代码                            |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 代码  | object  | -   |
| 名称  | object  | -   |
| 价格  | float64 | -   |
| 日期  | object  | -   |
| 时间  | object  | -   |

接口示例

```python
import akshare as ak

index_min_sw_df = ak.index_min_sw(symbol="801001")
print(index_min_sw_df)
```

数据示例

```
     代码    名称       价格       日期        时间
0    801001  申万50  3076.03  2024-10-23  09:30:00
1    801001  申万50  3074.62  2024-10-23  09:30:10
2    801001  申万50  3072.27  2024-10-23  09:30:20
3    801001  申万50  3070.98  2024-10-23  09:30:30
4    801001  申万50  3068.14  2024-10-23  09:30:40
..      ...   ...      ...         ...       ...
968  801001  申万50  3105.32  2024-10-23  13:41:20
969  801001  申万50  3104.96  2024-10-23  13:41:30
970  801001  申万50  3105.10  2024-10-23  13:41:40
971  801001  申万50  3104.75  2024-10-23  13:41:50
972  801001  申万50  3104.46  2024-10-23  13:42:00
[973 rows x 5 columns]
```
