---
title: "index_sugar_msweet - 中国食糖指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_sugar_msweet

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 中国食糖指数
- 描述: 沐甜科技数据中心-中国食糖指数
- 目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 中国食糖指数

接口: index_sugar_msweet

目标地址: http://www.msweet.com.cn/mtkj/sjzx13/index.html

描述: 沐甜科技数据中心-中国食糖指数

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 综合价格 | float64 | -   |
| 原糖价格 | float64 | -   |
| 现货价格 | float64 | -   |

接口示例

```python
import akshare as ak

index_sugar_msweet_df = ak.index_sugar_msweet()
print(index_sugar_msweet_df)
```

数据示例

```
        日期    综合价格   原糖价格    现货价格
0     2005-10-03  3927.0  15.51     NaN
1     2005-10-04  3932.0  11.41     NaN
2     2005-10-10  3950.0  11.62  3550.0
3     2005-10-11  3986.0  11.79  3640.0
4     2005-10-12  4020.0  11.67  3641.0
          ...     ...    ...     ...
4234  2023-06-08  7247.0  25.22  6966.0
4235  2023-06-09  7262.0  24.94  7021.0
4236  2023-06-12  7281.0  25.00  7051.0
4237  2023-06-13  7300.0  24.70  7058.0
4238  2023-06-14  7311.0  25.25  7036.0
[4239 rows x 4 columns]
```
