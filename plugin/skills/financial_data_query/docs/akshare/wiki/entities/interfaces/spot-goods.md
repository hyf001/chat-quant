---
title: "spot_goods - 商品现货价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# spot_goods

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 商品现货价格指数
- 描述: 新浪财经-商品现货价格指数
- 目标地址: http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 商品现货价格指数

接口: spot_goods

目标地址: http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0

描述: 新浪财经-商品现货价格指数

输入参数

| 名称     | 类型  | 描述                                      |
|--------|-----|-----------------------------------------|
| symbol | str | symbol="波罗的海干散货指数"; 指数目录请参考 **现货指数一览表** |

现货指数一览表

| 名称        | 时间段     |
|-----------|---------|
| 波罗的海干散货指数 | 2007-至今 |
| 钢坯价格指数    | 2005-至今 |
| 澳大利亚粉矿价格  | 2020-至今 |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 日期  | object  |     |
| 指数  | float64 |     |
| 涨跌额 | float64 |     |
| 涨跌幅 | float64 |     |

接口示例

```python
import akshare as ak

spot_goods_df = ak.spot_goods(symbol="波罗的海干散货指数")
print(spot_goods_df)
```

数据示例

```
         日期      指数    涨跌额   涨跌幅
0     2006-06-23  2808.0   83.0  0.0305
1     2006-06-30  2964.0  156.0  0.0556
2     2006-07-07  2870.0  -94.0 -0.0317
3     2006-07-14  2968.0   98.0  0.0341
4     2006-07-21  3191.0  223.0  0.0751
...          ...     ...    ...     ...
3673  2024-12-18  1028.0  -25.0 -2.3700
3674  2024-12-19   976.0  -52.0 -5.0600
3675  2024-12-20   990.0   14.0  1.4300
3676  2024-12-23   994.0    4.0  0.4000
3677  2024-12-24   997.0    3.0  0.3000
[3678 rows x 4 columns]
```
