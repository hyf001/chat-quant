---
title: "futures_to_spot_czce - 期转现-郑商所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_to_spot_czce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 期转现-郑商所
- 描述: 郑州商品交易所-期转现统计数据
- 目标地址: http://www.czce.com.cn/cn/jysj/qzxtj/H770311index_1.htm
- 限量: 单次返回指定交易日的期转现统计数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 期转现-郑商所

接口: futures_to_spot_czce

目标地址: http://www.czce.com.cn/cn/jysj/qzxtj/H770311index_1.htm

描述: 郑州商品交易所-期转现统计数据

限量: 单次返回指定交易日的期转现统计数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20210112"; 交易日 |

输出参数

| 名称   | 类型     | 描述       |
|------|--------|----------|
| 合约代码 | object | -        |
| 合约数量 | int64  | 注意: 单边计算 |

接口示例

```python
import akshare as ak

futures_to_spot_czce_df = ak.futures_to_spot_czce(date="20231228")
print(futures_to_spot_czce_df)
```

数据示例

```
    合约代码  合约数量
0  CF401   496
1  CJ401    10
```
