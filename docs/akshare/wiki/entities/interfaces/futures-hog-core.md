---
title: "futures_hog_core - 核心数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_hog_core

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 生猪信息 > 核心数据
- 描述: 玄田数据-核心数据
- 目标地址: https://zhujia.zhuwang.com.cn
- 限量: 单次返回指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 核心数据

接口: futures_hog_core

目标地址: https://zhujia.zhuwang.com.cn

描述: 玄田数据-核心数据

限量: 单次返回指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                            |
|--------|-----|-----------------------------------------------|
| symbol | str | symbol="外三元"; choice of {"外三元", "内三元", "土杂猪"} |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| date  | object  | -  |
| value | float64 | -  |

接口示例

```python
import akshare as ak

futures_hog_core_df = ak.futures_hog_core(symbol="外三元")
print(futures_hog_core_df)
```

数据示例

```
           date  value
0    2023-03-18  15.42
1    2023-03-19  15.46
2    2023-03-20  15.42
3    2023-03-21  15.44
4    2023-03-22  15.25
..          ...    ...
362  2024-03-14  14.58
363  2024-03-15  14.53
364  2024-03-16  14.54
365  2024-03-17  14.67
366  2024-03-18  14.71
[367 rows x 2 columns]
```
