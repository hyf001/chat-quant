---
title: "stock_ipo_review_em - 新股上会信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_review_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 新股上会信息
- 描述: 东方财富网-数据中心-新股申购-新股上会信息
- 目标地址: https://data.eastmoney.com/xg/gh/default.html
- 限量: 单次获取所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新股上会信息

接口: stock_ipo_review_em

目标地址: https://data.eastmoney.com/xg/gh/default.html

描述: 东方财富网-数据中心-新股申购-新股上会信息

限量: 单次获取所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型     | 描述 |
|---------|--------|----|
| 序号      | int64  | -  |
| 企业名称    | object | -  |
| 股票简称    | object | -  |
| 股票代码    | object | -  |
| 上市板块    | object | -  |
| 上会日期    | object | -  |
| 审核状态    | object | -  |
| 发审委委员   | object | -  |
| 主承销商    | object | -  |
| 发行数量(股) | object | -  |
| 拟融资额(元) | object | -  |
| 公告日期    | object | -  |
| 上市日期    | object | -  |

接口示例

```python
import akshare as ak

stock_ipo_review_em_df = ak.stock_ipo_review_em()
print(stock_ipo_review_em_df)
```

数据示例

```
     序号              企业名称  股票简称  ...       拟融资额(元)        公告日期 上市日期
0        1     北京维通利电气股份有限公司   维通利  ...  1.593741e+09  2025-11-19  NaT
1        2        杭州福恩股份有限公司  福恩股份  ...  1.250000e+09  2025-12-17  NaT
2        3    南昌三瑞智能科技股份有限公司  三瑞智能  ...  7.688829e+08  2025-12-08  NaT
3        4     深圳大普微电子股份有限公司   大普微  ...  1.877852e+09  2025-09-30  NaT
4        5        视涯科技股份有限公司  视涯科技  ...  2.014572e+09  2025-09-30  NaT
...    ...               ...   ...  ...           ...         ...  ...
5056  5057     合肥芯谷微电子股份有限公司   芯谷微  ...  8.500000e+08  2023-05-05  NaT
5057  5058    安翰科技(武汉)股份有限公司  安翰科技  ...  1.200000e+09  2019-03-22  NaT
5058  5059      浙江高信技术股份有限公司  高信技术  ...  7.300000e+08  2023-06-26  NaT
5059  5060    华夏天信智能物联股份有限公司  华夏天信  ...  9.280300e+08  2019-05-31  NaT
5060  5061  广西北部湾陆海新能源股份有限公司  陆海新能  ...  1.600000e+09  2023-09-22  NaT
[5061 rows x 13 columns]
```
