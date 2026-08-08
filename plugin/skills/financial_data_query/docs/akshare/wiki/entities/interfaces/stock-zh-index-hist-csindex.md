---
title: "stock_zh_index_hist_csindex - 中证指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_hist_csindex

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 中证指数
- 描述: 中证指数日频率的数据
- 目标地址: https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374
- 限量: 该接口返回指定 symbol 的 start_date 和 end_date 的指数日频率数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 中证指数

接口: stock_zh_index_hist_csindex

目标地址: https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374

描述: 中证指数日频率的数据

限量: 该接口返回指定 symbol 的 start_date 和 end_date 的指数日频率数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="000928"; 指数代码 |
| start_date | str | start_date="20180526" |
| end_date   | str | end_date="20240604"   |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 日期     | object  | -        |
| 指数代码   | object  | -        |
| 指数中文全称 | object  | -        |
| 指数中文简称 | object  | -        |
| 指数英文全称 | object  | -        |
| 指数英文简称 | object  | -        |
| 开盘     | float64 | -        |
| 最高     | float64 | -        |
| 最低     | float64 | -        |
| 收盘     | float64 | -        |
| 涨跌     | float64 | -        |
| 涨跌幅    | float64 | 注意单位: %  |
| 成交量    | float64 | 注意单位: 万手 |
| 成交金额   | float64 | 注意单位: 亿元 |
| 样本数量   | float64 | -        |
| 滚动市盈率  | float64 | -        |

接口示例

```python
import akshare as ak

stock_zh_index_hist_csindex_df = ak.stock_zh_index_hist_csindex(symbol="000928", start_date="20100101", end_date="20240604")
print(stock_zh_index_hist_csindex_df)
```

数据示例

```
          日期    指数代码  指数中文全称 指数中文简称  ... 成交量   成交金额 样本数量 滚动市盈率
0     2010-01-01  000928  中证能源指数  800能源  ...   189.61   19.89  38.0  11.51
1     2012-08-31  000928  中证能源指数  800能源  ...   189.61   19.89  38.0  11.51
2     2012-09-03  000928  中证能源指数  800能源  ...   256.16   27.91  38.0    NaN
3     2012-09-04  000928  中证能源指数  800能源  ...   259.30   28.01  38.0  11.51
4     2012-09-05  000928  中证能源指数  800能源  ...   230.82   26.39  38.0  11.43
...          ...     ...     ...    ...  ...      ...     ...   ...    ...
2851  2024-05-29  000928  中证能源指数  800能源  ...  1062.61  114.86  24.0  12.70
2852  2024-05-30  000928  中证能源指数  800能源  ...  1209.83  112.27  24.0  12.45
2853  2024-05-31  000928  中证能源指数  800能源  ...   954.20   94.05  24.0  12.37
2854  2024-06-03  000928  中证能源指数  800能源  ...  1294.04  115.08  24.0  12.41
2855  2024-06-04  000928  中证能源指数  800能源  ...  1169.28  127.39  24.0  12.20
[2856 rows x 16 columns]
```
