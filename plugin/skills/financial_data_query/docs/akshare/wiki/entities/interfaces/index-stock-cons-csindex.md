---
title: "index_stock_cons_csindex - 中证指数成份股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_stock_cons_csindex

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 中国股票指数成份 > 中证指数成份股
- 描述: 中证指数网站-成份股目录，可以通过 ak.index_csindex_all() 获取所有指数
- 目标地址: http://www.csindex.com.cn/zh-CN/indices/index-detail/000300
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中证指数成份股

接口: index_stock_cons_csindex

目标地址: http://www.csindex.com.cn/zh-CN/indices/index-detail/000300

描述: 中证指数网站-成份股目录，可以通过 ak.index_csindex_all() 获取所有指数

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="000300"; 指数代码 |

输出参数

| 名称      | 类型     | 描述  |
|---------|--------|-----|
| 日期      | object | -   |
| 指数代码    | object | -   |
| 指数名称    | object | -   |
| 指数英文名称  | object | -   |
| 成分券代码   | object | -   |
| 成分券名称   | object | -   |
| 成分券英文名称 | object | -   |
| 交易所     | object | -   |
| 交易所英文名称 | object | -   |

示例代码

```python
import akshare as ak

index_stock_cons_csindex_df = ak.index_stock_cons_csindex(symbol="000300")
print(index_stock_cons_csindex_df)
```

数据示例

```
             日期    指数代码  ...      交易所                  交易所英文名称
0    2024-01-04  000300  ...  深圳证券交易所  Shenzhen Stock Exchange
1    2024-01-04  000300  ...  深圳证券交易所  Shenzhen Stock Exchange
2    2024-01-04  000300  ...  深圳证券交易所  Shenzhen Stock Exchange
3    2024-01-04  000300  ...  深圳证券交易所  Shenzhen Stock Exchange
4    2024-01-04  000300  ...  深圳证券交易所  Shenzhen Stock Exchange
..          ...     ...  ...      ...                      ...
295  2024-01-04  000300  ...  上海证券交易所  Shanghai Stock Exchange
296  2024-01-04  000300  ...  上海证券交易所  Shanghai Stock Exchange
297  2024-01-04  000300  ...  上海证券交易所  Shanghai Stock Exchange
298  2024-01-04  000300  ...  上海证券交易所  Shanghai Stock Exchange
299  2024-01-04  000300  ...  上海证券交易所  Shanghai Stock Exchange
[300 rows x 9 columns]
```
