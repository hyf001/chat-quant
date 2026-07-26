---
title: "stock_zh_index_spot_sina - 实时行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_spot_sina

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 实时行情数据-新浪
- 描述: 新浪财经-中国股票指数数据
- 目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_s
- 限量: 单次返回所有指数的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据-新浪

接口: stock_zh_index_spot_sina

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#hs_s

描述: 新浪财经-中国股票指数数据

限量: 单次返回所有指数的实时行情数据

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
| 昨收  | float64 | -       |
| 今开  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 成交量 | float64 | 注意单位: 手 |
| 成交额 | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

stock_zh_index_spot_sina_df = ak.stock_zh_index_spot_sina()
print(stock_zh_index_spot_sina_df)
```

数据示例

```
     代码      名称      最新价  ...       最低        成交量           成交额
0    sh000001  上证指数  2967.2472  ...  2953.2901   285455945  321018391310
1    sh000002  Ａ股指数  3111.0281  ...  3096.3842   285134140  320788878153
2    sh000003  Ｂ股指数   234.1943  ...   232.4912      297879     160673330
3    sh000004  工业指数  2703.9886  ...  2690.2040   168709808  228294788620
4    sh000005  商业指数  2351.1093  ...  2339.6375    23082870   23470835715
..        ...   ...        ...  ...        ...         ...           ...
552  sz980015  疫苗生科  8560.3130  ...  8533.3370   421452161   12430783309
553  sz980016  公卫健康  6844.2740  ...  6824.8810   572854058   16723915499
554  sz980028  龙头家电  9330.1080  ...  9296.8940   296504548    7181802948
555  sz980030  消费电子  4393.0420  ...  4372.5400  1645434624   24770906620
556  sz980032  新能电池  8862.8690  ...  8791.8960   344385538   13001077515
[557 rows x 11 columns]
```
