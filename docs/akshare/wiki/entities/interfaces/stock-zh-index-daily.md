---
title: "stock_zh_index_daily - 历史行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_daily

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 历史行情数据 > 历史行情数据-新浪
- 描述: 股票指数的历史数据按日频率更新
- 目标地址: https://finance.sina.com.cn/realstock/company/sz399552/nc.shtml(示例)
- 限量: 单次返回指定 symbol 的所有历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 历史行情数据-新浪

接口: stock_zh_index_daily

目标地址: https://finance.sina.com.cn/realstock/company/sz399552/nc.shtml(示例)

描述: 股票指数的历史数据按日频率更新

限量: 单次返回指定 symbol 的所有历史行情数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="sz399552" |

输出参数-历史行情数据

| 名称     | 类型      | 描述                    |
|--------|---------|-----------------------|
| date   | object  | 新浪的数据开始时间, 不是该指数的上市时间 |
| open   | float64 | -                     |
| high   | float64 | -                     |
| low    | float64 | -                     |
| close  | float64 | -                     |
| volume | int64   | -                     |

接口示例-历史行情数据

```python
import akshare as ak

stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
print(stock_zh_index_daily_df)
```

数据示例-历史行情数据

```
            date      open      high       low     close       volume
0     2005-01-04   996.682   996.682   984.795   986.927    232376203
1     2005-01-05   986.570  1008.855   985.677  1003.633    348610113
2     2005-01-06  1003.490  1003.490   990.792   994.595    293390559
3     2005-01-07   993.434  1009.000   990.446   997.606    339162698
4     2005-01-10   996.928  1006.457   993.123  1006.337    294940533
          ...       ...       ...       ...       ...          ...
4566  2023-10-23  5400.543  5400.794  5269.828  5290.334  10308312600
4567  2023-10-24  5311.669  5363.195  5290.505  5352.012  11474572900
4568  2023-10-25  5386.425  5423.014  5375.999  5375.999  11492124400
4569  2023-10-26  5351.163  5404.992  5337.493  5398.934  10248504400
4570  2023-10-27  5387.274  5514.308  5380.941  5492.027  11254280400
[4571 rows x 6 columns]
```
