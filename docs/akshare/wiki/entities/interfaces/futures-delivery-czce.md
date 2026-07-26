---
title: "futures_delivery_czce - 交割统计-郑商所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_delivery_czce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 交割统计-郑商所
- 描述: 郑州商品交易所-交割统计
- 目标地址: http://www.czce.com.cn/cn/jysj/ydjgcx/H770316index_1.htm
- 限量: 单次返回指定交易月份的交割统计数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 交割统计-郑商所

接口: futures_delivery_czce

目标地址: http://www.czce.com.cn/cn/jysj/ydjgcx/H770316index_1.htm

描述: 郑州商品交易所-交割统计

限量: 单次返回指定交易月份的交割统计数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20210112"; 交易日 |

输出参数

| 名称   | 类型     | 描述             |
|------|--------|----------------|
| 品种   | object | -              |
| 交割数量 | int64  | 按单边统计          |
| 交割额  | int64  | 注意单位: 元; 按单边统计 |

接口示例

```python
import akshare as ak

futures_delivery_monthly_czce_df = ak.futures_delivery_czce(date="20210112")
print(futures_delivery_monthly_czce_df)
```

数据示例

```
      品种  交割数量        交割额
0     鲜苹果   138    8221920
1      棉花  1416  106332600
2    干制红枣    76    3697150
3      棉纱     4     418600
4  精对苯二甲酸   216    3974400
5     动力煤   200   15276000
6      合计  2050  137920670
```
