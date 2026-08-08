---
title: "index_all_cni - 全部指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_all_cni

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 国证指数 > 全部指数
- 描述: 国证指数-最近交易日的所有指数的代码和基本信息
- 目标地址: http://www.cnindex.com.cn/zh_indices/sese/index.html?act_menu=1&index_type=-1
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全部指数

接口: index_all_cni

目标地址: http://www.cnindex.com.cn/zh_indices/sese/index.html?act_menu=1&index_type=-1

描述: 国证指数-最近交易日的所有指数的代码和基本信息

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述                               |
|--------|---------|----------------------------------|
| 指数代码   | object  | -                                |
| 指数简称   | object  | -                                |
| 样本数    | int64   | -                                |
| 收盘点位   | float64 | -                                |
| 涨跌幅    | float64 | -                                |
| PE滚动   | float64 | -                                |
| 成交量    | float64 | 注意单位: 债券指数成交量单位为亿张，非债券指数成交量单位为万手 |
| 成交额    | float64 | 注意单位: 亿元                         |
| 总市值    | float64 | 注意单位: 亿元                         |
| 自由流通市值 | float64 | 注意单位: 亿元                         |

接口示例

```python
import akshare as ak

index_all_cni_df = ak.index_all_cni()
print(index_all_cni_df)
```

数据示例

```
          指数代码          指数简称  样本数  ...          成交额            总市值        自由流通市值
0       399001          深证成指  500  ...  1551.817177  182200.555052  93688.587978
1       399002          深成指R  500  ...  1551.817177  182200.555052  93688.587978
2       399003          成份Ｂ指   10  ...     0.545615     345.946714    289.787042
3       399004        深证100R  100  ...   725.052558  102390.468955  51849.808034
4       399005         中小100  100  ...   425.914666   52479.098750  26772.330931
        ...           ...  ...  ...          ...            ...           ...
1257  CNB20014  高等级非贴标绿债（全价）    0  ...   109.463922            NaN           NaN
1258  CNB20015   高等级贴标绿债（全价）    0  ...   193.434154            NaN           NaN
1259      CNYR       人民币实际指数    0  ...     0.000000            NaN           NaN
1260      CNYX         人民币指数    0  ...     0.000000            NaN           NaN
1261   RETHKDG    中华房地产信托基金R   30  ...     2.311884    1617.705097    221.909288
[1262 rows x 10 columns]
```
