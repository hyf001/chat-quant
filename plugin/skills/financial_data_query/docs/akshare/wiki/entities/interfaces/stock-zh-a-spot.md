---
title: "stock_zh_a_spot - 实时行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_spot

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-新浪
- 描述: 新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
- 目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_a
- 限量: 单次返回沪深京 A 股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时行情数据-新浪

接口: stock_zh_a_spot

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_a

描述: 新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔

限量: 单次返回沪深京 A 股上市公司的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 代码  | object  | -       |
| 名称  | object  | -       |
| 最新价 | float64 | -       |
| 涨跌额 | float64 | -       |
| 涨跌幅 | float64 | 注意单位: % |
| 买入  | float64 | -       |
| 卖出  | float64 | -       |
| 昨收  | float64 | -       |
| 今开  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 成交量 | float64 | 注意单位: 股 |
| 成交额 | float64 | 注意单位: 元 |
| 时间戳 | object  | -       |

接口示例

```python
import akshare as ak

stock_zh_a_spot_df = ak.stock_zh_a_spot()
print(stock_zh_a_spot_df)
```

数据示例

```
      代码        名称    最新价   涨跌额  ...  最低  成交量          成交额       时间戳
0     bj430017  星昊医药  15.41  1.15  ...  14.02   8411380.0  127141645.0  15:30:01
1     bj430047  诺思兰德  18.17  0.67  ...  17.45   4167518.0   75391105.0  15:30:01
2     bj430090  同辉信息   4.10  0.31  ...   3.75  22609069.0   90900380.0  15:30:01
3     bj430139  华岭股份  13.66  0.86  ...  12.73   4712891.0   63247000.0  15:30:01
4     bj430198  微创光电   0.00  0.00  ...   0.00         0.0          0.0  15:30:01
        ...   ...    ...   ...  ...    ...         ...          ...       ...
5311  sz301550  斯菱股份  48.53 -1.92  ...  48.50   2589623.0  127379535.0  15:35:30
5312  sz301555  惠柏新材  42.12 -1.40  ...  41.90   3411454.0  146471807.0  15:35:45
5313  sz301558  三态股份  14.33 -0.92  ...  14.32  21311135.0  313639930.0  15:35:00
5314  sz301559  中集环科  19.01 -0.49  ...  19.00   2980100.0   57148056.0  15:35:15
5315  sz301568   思泰克  49.08 -3.00  ...  48.83   9336045.0  469276460.0  15:35:30
[5316 rows x 14 columns]
```
