---
title: "index_stock_cons_weight_csindex - 中证指数成份股权重"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_stock_cons_weight_csindex

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 中国股票指数成份 > 中证指数成份股权重
- 描述: 中证指数网站-成份股权重
- 目标地址: http://www.csindex.com.cn/zh-CN/indices/index-detail/000300
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中证指数成份股权重

接口: index_stock_cons_weight_csindex

目标地址: http://www.csindex.com.cn/zh-CN/indices/index-detail/000300

描述: 中证指数网站-成份股权重

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="000300"; 指数代码 |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 日期      | object  | -       |
| 指数代码    | object  | -       |
| 指数名称    | object  | -       |
| 指数英文名称  | object  | -       |
| 成分券代码   | object  | -       |
| 成分券名称   | object  | -       |
| 成分券英文名称 | object  | -       |
| 交易所     | object  | -       |
| 交易所英文名称 | object  | -       |
| 权重      | float64 | 注意单位: % |

示例代码

```python
import akshare as ak

index_stock_cons_weight_csindex_df = ak.index_stock_cons_weight_csindex(symbol="000300")
print(index_stock_cons_weight_csindex_df)
```

数据示例

```
     日期    指数代码   指数名称  ...     交易所                交易所英文名称     权重
0    2023-12-29  000300  沪深300  ...  深圳证券交易所  Shenzhen Stock Exchange  0.524
1    2023-12-29  000300  沪深300  ...  深圳证券交易所  Shenzhen Stock Exchange  0.410
2    2023-12-29  000300  沪深300  ...  深圳证券交易所  Shenzhen Stock Exchange  0.486
3    2023-12-29  000300  沪深300  ...  深圳证券交易所  Shenzhen Stock Exchange  0.088
4    2023-12-29  000300  沪深300  ...  深圳证券交易所  Shenzhen Stock Exchange  0.465
..          ...     ...    ...  ...      ...                      ...    ...
295  2023-12-29  000300  沪深300  ...  上海证券交易所  Shanghai Stock Exchange  0.074
296  2023-12-29  000300  沪深300  ...  上海证券交易所  Shanghai Stock Exchange  0.136
297  2023-12-29  000300  沪深300  ...  上海证券交易所  Shanghai Stock Exchange  0.063
298  2023-12-29  000300  沪深300  ...  上海证券交易所  Shanghai Stock Exchange  0.178
299  2023-12-29  000300  沪深300  ...  上海证券交易所  Shanghai Stock Exchange  0.602
[300 rows x 10 columns]
```
