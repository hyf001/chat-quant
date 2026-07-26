---
title: "stock_hk_index_daily_sina - 历史行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_hk_index_daily_sina

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 港股股票指数 > 历史行情数据-新浪
- 描述: 新浪财经-港股指数-历史行情数据
- 目标地址: https://stock.finance.sina.com.cn/hkstock/quotes/CES100.html
- 限量: 单次返回指定 symbol 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情数据-新浪

接口: stock_hk_index_daily_sina

目标地址: https://stock.finance.sina.com.cn/hkstock/quotes/CES100.html

描述: 新浪财经-港股指数-历史行情数据

限量: 单次返回指定 symbol 的所有数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="CES100" |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| date   | object  | -       |
| open   | object  | -       |
| close  | float64 | -       |
| high   | float64 | -       |
| low    | float64 | 注意单位: % |
| volume | float64 | -       |

接口示例

```python
import akshare as ak

stock_hk_index_daily_sina_df = ak.stock_hk_index_daily_sina(symbol="CES100")
print(stock_hk_index_daily_sina_df)
```

数据示例

```
            date      open      high       low     close      volume
0     2014-12-15  4354.014  4362.220  4331.394  4355.359  1087163017
1     2014-12-16  4334.295  4347.367  4275.529  4280.410  1303011243
2     2014-12-17  4278.770  4280.350  4223.895  4227.100  2002919200
3     2014-12-18  4281.007  4296.184  4264.265  4282.028  1547580777
4     2014-12-19  4347.982  4354.488  4321.534  4331.438  1515374212
          ...       ...       ...       ...       ...         ...
2293  2024-04-08  3645.559  3688.903  3624.238  3654.013  2067842312
2294  2024-04-09  3678.340  3719.132  3677.429  3686.826  1588737425
2295  2024-04-10  3706.046  3752.432  3701.602  3741.842  1947224622
2296  2024-04-11  3678.382  3736.533  3676.288  3725.992  1829890643
2297  2024-04-12  3702.688  3712.628  3647.700  3648.330  2097570788
[2298 rows x 6 columns]
```
