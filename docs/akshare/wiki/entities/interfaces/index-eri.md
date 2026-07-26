---
title: "index_eri - 排污权指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_eri

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 排污权指数
- 描述: 浙江省排污权交易指数的数据
- 目标地址: https://zs.zjpwq.net/
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 排污权指数

接口: index_eri

目标地址: https://zs.zjpwq.net/

描述: 浙江省排污权交易指数的数据

输入参数

| 名称     | 类型  | 描述                                  |
|--------|-----|-------------------------------------|
| symbol | str | symbol="月度"; choice of {"月度", "季度"} |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 日期   | object  |         |
| 交易指数 | float64 |         |
| 成交量  | float64 | 注意单位: 吨 |
| 成交额  | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

index_eri_df = ak.index_eri(symbol="月度")
print(index_eri_df)
```

数据示例

```
       日期        交易指数     成交量         成交额
0    2015-01-01  666.723178  1034.4964  1.947994e+07
1    2015-02-01  331.931459  1432.3328  4.688527e+07
2    2015-03-01  280.808046   368.7993  1.286788e+07
3    2015-04-01  306.577138   847.2793  2.034412e+07
4    2015-05-01  175.653651   914.9349  1.267447e+07
..          ...         ...        ...           ...
97   2023-02-01  496.845377   302.1130  1.710103e+07
98   2023-03-01  422.643848   706.8660  3.102841e+07
99   2023-04-01  209.456300  4374.7260  5.408741e+07
100  2023-05-01  330.866173   622.0553  1.696480e+07
101  2023-06-01  351.518957   836.3700  1.942974e+07
[102 rows x 4 columns]
```
