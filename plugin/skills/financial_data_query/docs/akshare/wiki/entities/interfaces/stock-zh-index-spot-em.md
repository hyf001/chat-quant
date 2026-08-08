---
title: "stock_zh_index_spot_em - 实时行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_spot_em

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 实时行情数据-东财
- 描述: 东方财富网-行情中心-沪深京指数
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#index_sz
- 限量: 单次返回所有指数的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据-东财

接口: stock_zh_index_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#index_sz

描述: 东方财富网-行情中心-沪深京指数

限量: 单次返回所有指数的实时行情数据

输入参数

| 名称     | 类型  | 描述                                                                         |
|--------|-----|----------------------------------------------------------------------------|
| symbol | str | symbol="上证系列指数"；choice of {"沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"} |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 序号  | int64   | -       |
| 代码  | object  | -       |
| 名称  | object  | -       |
| 最新价 | float64 | -       |
| 涨跌额 | float64 | -       |
| 涨跌幅 | float64 | 注意单位: % |
| 成交量 | float64 | -       |
| 成交额 | float64 | -       |
| 振幅  | float64 | 注意单位: % |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 今开  | float64 | -       |
| 昨收  | float64 | -       |
| 量比  | float64 | -       |

接口示例

```python
import akshare as ak

stock_zh_index_spot_em_df = ak.stock_zh_index_spot_em(symbol="上证系列指数")
print(stock_zh_index_spot_em_df)
```

数据示例

```
      序号  代码     名称    最新价   涨跌幅   涨跌额  ... 振幅  最高  最低 今开 昨收  量比
0      1  000116  信用100   183.69  0.01  0.02  ...  0.0 NaN NaN NaN   183.67 NaN
1      2  000101   5年信用   233.04  0.01  0.02  ...  0.0 NaN NaN NaN   233.02 NaN
2      3  000022   沪公司债   234.63  0.01  0.02  ...  0.0 NaN NaN NaN   234.61 NaN
3      4  000061  沪企债30   169.79  0.01  0.01  ...  0.0 NaN NaN NaN   169.78 NaN
4      5  000012   国债指数   206.03  0.00  0.01  ...  0.0 NaN NaN NaN   206.02 NaN
..   ...     ...    ...      ...   ...   ...  ...  ...  ..  ..  ..      ...  ..
174  175  000005   商业指数  2351.11  0.00  0.00  ...  0.0 NaN NaN NaN  2351.11 NaN
175  176  000004   工业指数  2703.99  0.00  0.00  ...  0.0 NaN NaN NaN  2703.99 NaN
176  177  000003   Ｂ股指数   234.19  0.00  0.00  ...  0.0 NaN NaN NaN   234.19 NaN
177  178  000002   Ａ股指数  3111.03  0.00  0.00  ...  0.0 NaN NaN NaN  3111.03 NaN
178  179  000001   上证指数  2967.25  0.00  0.00  ...  0.0 NaN NaN NaN  2967.25 NaN
[179 rows x 14 columns]
```
