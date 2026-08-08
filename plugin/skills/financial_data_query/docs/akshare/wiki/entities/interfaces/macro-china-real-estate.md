---
title: "macro_china_real_estate - 国房景气指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_real_estate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 国房景气指数
- 描述: 国家统计局-国房景气指数
- 目标地址: http://data.eastmoney.com/cjsj/hyzs_list_EMM00121987.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 国房景气指数

接口: macro_china_real_estate

目标地址: http://data.eastmoney.com/cjsj/hyzs_list_EMM00121987.html

描述: 国家统计局-国房景气指数

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 最新值    | float64 | -   |
| 涨跌幅    | float64 | -   |
| 近3月涨跌幅 | float64 | -   |
| 近6月涨跌幅 | float64 | -   |
| 近1年涨跌幅 | float64 | -   |
| 近2年涨跌幅 | float64 | -   |
| 近3年涨跌幅 | float64 | -   |

接口示例

```python
import akshare as ak

macro_china_real_estate_df = ak.macro_china_real_estate()
print(macro_china_real_estate_df)
```

数据示例

```
     日期     最新值       涨跌幅  ...    近1年涨跌幅    近2年涨跌幅    近3年涨跌幅
0    1998-01-01   98.60       NaN  ...       NaN       NaN       NaN
1    1998-02-01   98.99  0.395538  ...       NaN       NaN       NaN
2    1998-03-01   99.05  0.060612  ...       NaN       NaN       NaN
3    1998-04-01  100.81  1.776880  ...       NaN       NaN       NaN
4    1998-05-01  101.68  0.863010  ...       NaN       NaN       NaN
..          ...     ...       ...  ...       ...       ...       ...
280  2022-03-01   96.66 -0.278552  ... -4.618117 -1.598290 -4.306504
281  2022-04-01   95.89 -0.796607  ... -5.349916 -3.023867 -5.190825
282  2022-05-01   95.60 -0.302430  ... -5.533597 -3.774534 -5.402731
283  2022-06-01   95.40 -0.209205  ... -5.619311 -4.456685 -5.628648
284  2022-07-01   95.26 -0.146751  ... -5.683168 -4.825657 -5.757816
```
