---
title: "spot_quotations_sge - 实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_quotations_sge

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 上海黄金交易所 > 实时行情数据
- 描述: 上海黄金交易所-数据资讯-行情走势-实时数据
- 目标地址: https://www.sge.com.cn/
- 限量: 单次返回指定 symbol 的所有行情数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据

接口: spot_quotations_sge

目标地址: https://www.sge.com.cn/

描述: 上海黄金交易所-数据资讯-行情走势-实时数据

限量: 单次返回指定 symbol 的所有行情数据

输入参数

| 名称     | 类型  | 描述                                                      |
|--------|-----|---------------------------------------------------------|
| symbol | str | symbol="Au99.99"; 可以通过 ak.spot_symbol_table_sge() 获取品种表 |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 品种   | object  | -  |
| 时间   | object  | -  |
| 现价   | float64 | -  |
| 更新时间 | object  | -  |

接口示例

```python
import akshare as ak

spot_quotations_sge_df = ak.spot_quotations_sge(symbol="Au99.99")
print(spot_quotations_sge_df)
```

数据示例

```
     品种        时间     现价                  更新时间
0    Au99.99  00:00:00  755.0  2025年04月14日 22:28:55
1    Au99.99  00:01:00  755.0  2025年04月14日 22:28:55
2    Au99.99  00:02:00  755.0  2025年04月14日 22:28:55
3    Au99.99  00:03:00  755.0  2025年04月14日 22:28:55
4    Au99.99  00:04:00  755.0  2025年04月14日 22:28:55
..       ...       ...    ...                   ...
686  Au99.99  22:24:00  760.0  2025年04月14日 22:28:55
687  Au99.99  22:25:00  760.0  2025年04月14日 22:28:55
688  Au99.99  22:26:00  760.0  2025年04月14日 22:28:55
689  Au99.99  22:27:00  760.0  2025年04月14日 22:28:55
690  Au99.99  22:28:00  760.0  2025年04月14日 22:28:55
[691 rows x 4 columns]
```
