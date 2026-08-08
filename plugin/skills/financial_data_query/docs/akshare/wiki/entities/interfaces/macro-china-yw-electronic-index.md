---
title: "macro_china_yw_electronic_index - 义乌小商品指数-电子元器件"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_yw_electronic_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 义乌小商品指数-电子元器件
- 描述: 义乌小商品指数-电子元器件数据, 数据区间从 20060911-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00055551.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 义乌小商品指数-电子元器件

接口: macro_china_yw_electronic_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00055551.html

描述: 义乌小商品指数-电子元器件数据, 数据区间从 20060911-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 日期     | object  | -       |
| 最新值    | int64   | -       |
| 涨跌幅    | float64 | 注意单位: % |
| 近3月涨跌幅 | float64 | 注意单位: % |
| 近6月涨跌幅 | float64 | 注意单位: % |
| 近1年涨跌幅 | float64 | 注意单位: % |
| 近2年涨跌幅 | float64 | 注意单位: % |
| 近3年涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_yw_electronic_index_df = ak.macro_china_yw_electronic_index()
print(macro_china_yw_electronic_index_df)
```

数据示例

```
        日期     最新值   涨跌幅    近3月涨跌幅 近6月涨跌幅 近1年涨跌幅  近2年涨跌幅 近3年涨跌幅
0    2006-09-11  101.34       NaN       NaN     NaN     NaN       NaN     NaN
1    2006-09-18  102.94  1.578844       NaN     NaN     NaN       NaN     NaN
2    2006-09-25  103.34  0.388576       NaN     NaN     NaN       NaN     NaN
3    2006-10-02  103.21 -0.125798       NaN     NaN     NaN       NaN     NaN
4    2006-10-09  103.06 -0.145335       NaN     NaN     NaN       NaN     NaN
..          ...     ...       ...       ...     ...     ...       ...     ...
755  2022-03-07  100.18 -0.169407  0.089919    0.18    0.18 -0.802060    0.18
756  2022-03-14  100.09 -0.089838  0.039980    0.09    0.09 -0.407960    0.09
757  2022-03-21  106.11  6.014587  0.463927    6.11    6.11  5.845387    6.11
758  2022-03-28  103.06 -2.874376  0.243167    3.06    3.06  2.936476    3.06
759  2022-04-04  101.53 -1.484572  0.118332    1.53    1.53  1.469119    1.53
```
