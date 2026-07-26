---
title: "drewry_wci_index - 集装箱指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# drewry_wci_index

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 集装箱指数
- 描述: Drewry 集装箱指数的数据
- 目标地址: https://infogram.com/world-container-index-1h17493095xl4zj
- 限量: 返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 集装箱指数

接口: drewry_wci_index

目标地址: https://infogram.com/world-container-index-1h17493095xl4zj

描述: Drewry 集装箱指数的数据

限量: 返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                                                                                                                                                    |
|--------|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol | str | symbol="composite"; choice of {"composite", "shanghai-rotterdam", "rotterdam-shanghai", "shanghai-los angeles", "los angeles-shanghai", "shanghai-genoa", "new york-rotterdam", "rotterdam-new york"} |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| date | object  |     |
| wci  | float64 |     |

接口示例

```python
import akshare as ak

drewry_wci_index_df = ak.drewry_wci_index(symbol="composite")
print(drewry_wci_index_df)
```

数据示例

```
           date      wci
0    2016-03-10   700.57
1    2016-03-17   674.41
2    2016-03-24   666.27
3    2016-03-31   849.08
4    2016-04-07   868.06
..          ...      ...
437  2024-08-22  5319.00
438  2024-08-29  5181.00
439  2024-09-05  4775.00
440  2024-09-12  4168.00
441  2024-09-19  3970.00
[442 rows x 2 columns]
```
