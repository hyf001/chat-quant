---
title: "stock_esg_rate_sina - ESG 评级数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_esg_rate_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > ESG 评级 > ESG 评级数据
- 描述: 新浪财经-ESG评级中心-ESG评级-ESG评级数据
- 目标地址: https://finance.sina.com.cn/esg/grade.shtml
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### ESG 评级数据

接口: stock_esg_rate_sina

目标地址: https://finance.sina.com.cn/esg/grade.shtml

描述: 新浪财经-ESG评级中心-ESG评级-ESG评级数据

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| 成分股代码 | object | -  |
| 评级机构  | object | -  |
| 评级    | object | -  |
| 评级季度  | object | -  |
| 标识    | object | -  |
| 交易市场  | object | -  |

接口示例

```python
import akshare as ak

stock_esg_rate_sina_df = ak.stock_esg_rate_sina()
print(stock_esg_rate_sina_df)
```

数据示例

```
    成分股代码              评级机构     评级    评级季度             标识 交易市场
0      SZ000001             中财绿金院     A-  2022Q4            NaN   cn
1      SZ000001              商道融绿     B+  2022Q4            NaN   cn
2      SZ000001                盟浪      A  2022Q2            NaN   cn
3      SZ000001               中诚信    AA-  2023Q3            NaN   cn
4      SZ000001  晨星Sustainalytics  24.96  2022Q4  Comprehensive   cn
         ...               ...    ...     ...            ...  ...
46888   HK02361                盟浪      -  2022Q2            NaN   hk
46889   HK02361               中诚信     BB  2023Q3            NaN   hk
46890   HK02361  晨星Sustainalytics      -  2022Q4                  hk
46891   HK02361                妙盈      -  2022Q2            NaN   hk
46892   HK02361             华测CTI      -  2022Q1            NaN   hk
[46893 rows x 6 columns]
```
