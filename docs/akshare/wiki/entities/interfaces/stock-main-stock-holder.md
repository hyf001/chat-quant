---
title: "stock_main_stock_holder - 主要股东"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_main_stock_holder

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 主要股东
- 描述: 新浪财经-股本股东-主要股东
- 目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/600004.phtml
- 限量: 单次获取所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 主要股东

接口: stock_main_stock_holder

目标地址: https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/600004.phtml

描述: 新浪财经-股本股东-主要股东

限量: 单次获取所有历史数据

输入参数

| 名称    | 类型  | 描述                   |
|-------|-----|----------------------|
| stock | str | stock="600004"; 股票代码 |

输出参数

| 名称    | 类型      | 描述         |
|-------|---------|------------|
| 编号    | object  | -          |
| 股东名称  | object  | -          |
| 持股数量  | float64 | 注意单位: 股    |
| 持股比例  | float64 | 注意单位: %    |
| 股本性质  | object  | -          |
| 截至日期  | object  | -          |
| 公告日期  | object  | -          |
| 股东说明  | object  | -          |
| 股东总数  | float64 | -          |
| 平均持股数 | float64 | 备注: 按总股本计算 |

接口示例

```python
import akshare as ak

stock_main_stock_holder_df = ak.stock_main_stock_holder(stock="600004")
print(stock_main_stock_holder_df)
```

数据示例

```
      编号                股东名称          持股数量  ...  股东说明      股东总数     平均持股数
0      1          上海国际集团有限公司  6.331323e+09  ...   NaN  164613.0  178312.0
1      2      中国移动通信集团广东有限公司  5.334893e+09  ...   NaN  164613.0  178312.0
2      3   富德生命人寿保险股份有限公司-传统  2.779437e+09  ...   NaN  164613.0  178312.0
3      4  富德生命人寿保险股份有限公司-资本金  1.763232e+09  ...   NaN  164613.0  178312.0
4      5       上海上国投资产管理有限公司  1.395571e+09  ...   NaN  164613.0  178312.0
...   ..                 ...           ...  ...   ...       ...       ...
1383   6        东方国际（集团）有限公司  5.000000e+07  ...   NaN       NaN       NaN
1384   7            申能股份有限公司  5.000000e+07  ...   NaN       NaN       NaN
1385   8    上海外高桥保税区开发股份有限公司  4.000000e+07  ...   NaN       NaN       NaN
1386   9      上海市城市建设投资开发总公司  3.800000e+07  ...   NaN       NaN       NaN
1387  10          中国华北电力集团公司  3.000000e+07  ...   NaN       NaN       NaN
[1388 rows x 10 columns]
```
