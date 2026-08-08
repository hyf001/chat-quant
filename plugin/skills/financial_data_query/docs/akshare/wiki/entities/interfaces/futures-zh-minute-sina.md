---
title: "futures_zh_minute_sina - 内盘-分时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_zh_minute_sina

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-分时行情数据
- 描述: 新浪财经-期货-分时数据
- 目标地址: http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
- 限量: 单次返回指定 symbol 和 period 的分时数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-分时行情数据

接口: futures_zh_minute_sina

目标地址: http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3

描述: 新浪财经-期货-分时数据

限量: 单次返回指定 symbol 和 period 的分时数据

输入参数

| 名称     | 类型  | 描述                                                                                              |
|--------|-----|-------------------------------------------------------------------------------------------------|
| symbol | str | symbol="IF2008"; 具体合约(期货品种符号需要大写), 可以通过调用 ak.match_main_contract(symbol="cffex") 接口获取, 或者访问网页获取 |
| period | str | period="1"; choice of {"1": "1分钟", "5": "5分钟", "15": "15分钟", "30": "30分钟", "60": "60分钟"}        |

输出参数

| 名称       | 类型      | 描述  |
|----------|---------|-----|
| datetime | object  | -   |
| open     | float64 | -   |
| high     | float64 | -   |
| low      | float64 | -   |
| close    | float64 | -   |
| volume   | int64   | -   |
| hold     | int64   | 持仓量 |

接口示例

```python
import akshare as ak

futures_zh_minute_sina_df = ak.futures_zh_minute_sina(symbol="RB0", period="1")
print(futures_zh_minute_sina_df)
```

数据示例

```
                 datetime    open    high     low   close  volume     hold
0     2025-01-14 21:13:00  3278.0  3280.0  3278.0  3279.0    3485  1739947
1     2025-01-14 21:14:00  3279.0  3279.0  3277.0  3278.0    5880  1741617
2     2025-01-14 21:15:00  3278.0  3278.0  3276.0  3276.0    4947  1740980
3     2025-01-14 21:16:00  3276.0  3277.0  3276.0  3277.0    3766  1741117
4     2025-01-14 21:17:00  3277.0  3278.0  3276.0  3278.0    3606  1741199
...                   ...     ...     ...     ...     ...     ...      ...
1018  2025-01-17 14:56:00  3373.0  3373.0  3371.0  3372.0    4021  1816948
1019  2025-01-17 14:57:00  3371.0  3374.0  3371.0  3374.0    8199  1816486
1020  2025-01-17 14:58:00  3373.0  3374.0  3372.0  3373.0    7900  1816404
1021  2025-01-17 14:59:00  3373.0  3374.0  3371.0  3372.0   13951  1813334
1022  2025-01-17 15:00:00  3371.0  3373.0  3371.0  3372.0   13335  1809583
[1023 rows x 7 columns]
```
