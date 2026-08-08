---
title: "index_realtime_fund_sw - 基金指数实时行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_realtime_fund_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 基金指数实时行情
- 描述: 申万宏源研究-申万指数-指数发布-基金指数-实时行情
- 目标地址: https://www.swsresearch.com/institute_sw/allIndex/releasedIndex
- 限量: 该接口返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金指数实时行情

接口: index_realtime_fund_sw

目标地址: https://www.swsresearch.com/institute_sw/allIndex/releasedIndex

描述: 申万宏源研究-申万指数-指数发布-基金指数-实时行情

限量: 该接口返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                        |
|--------|-----|-----------------------------------------------------------|
| symbol | str | symbol="基础一级"; choice of {"基础一级", "基础二级", "基础三级", "特色指数"} |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 指数代码 | object  | -       |
| 指数名称 | object  | -       |
| 昨收盘  | float64 | -       |
| 日涨跌幅 | float64 | 注意单位: % |
| 年涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_realtime_fund_sw_df = ak.index_realtime_fund_sw(symbol="基础一级")
print(index_realtime_fund_sw_df)
```

数据示例

```
     指数代码          指数名称      昨收盘  日涨跌幅  年涨跌幅
0  807100    申万宏源权益基金指数   770.47 -0.39 -1.40
1  807200    申万宏源债券基金指数  1043.30  0.04  1.24
2  807300    申万宏源混合基金指数   947.76 -0.04  0.70
3  807400    申万宏源货币基金指数  1031.48  0.01  0.50
4  807500    申万宏源另类基金指数  1119.82  0.09  4.45
5  807600    申万宏源组合基金指数   874.51  0.46 -0.98
6  807700  申万宏源QDII基金指数  1063.01  0.03  1.78
```
