---
title: "sw_index_third_cons - 申万三级行业成份"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# sw_index_third_cons

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万三级行业成份
- 描述: 申万三级行业成份
- 目标地址: https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 申万三级行业成份

接口: sw_index_third_cons

目标地址: https://legulegu.com/stockdata/index-composition?industryCode=851921.SI

描述: 申万三级行业成份

输入参数

| 名称     | 类型  | 描述                                                               |
|--------|-----|------------------------------------------------------------------|
| symbol | str | symbol="850111.SI"; 行业代码; 可以通过 ak.sw_index_third_info() 获取所有行业代码 |

输出参数

| 名称               | 类型      | 描述       |
|------------------|---------|----------|
| 序号               | int64   |          |
| 股票代码             | object  |          |
| 股票简称             | object  |          |
| 纳入时间             | object  |          |
| 申万1级             | object  |          |
| 申万2级             | object  |          |
| 申万3级             | object  |          |
| 价格               | float64 |          |
| 市盈率              | float64 |          |
| 市盈率ttm           | float64 |          |
| 市净率              | float64 |          |
| 股息率              | float64 | 注意单位: %  |
| 市值               | float64 | 注意单位: 亿元 |
| 归母净利润同比增长(09-30) | float64 | 注意单位: %  |
| 归母净利润同比增长(06-30) | float64 | 注意单位: %  |
| 营业收入同比增长(09-30)  | float64 | 注意单位: %  |
| 营业收入同比增长(06-30)  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

sw_index_third_cons_df = ak.sw_index_third_cons(symbol="850111.SI")
print(sw_index_third_cons_df)
```

数据示例

```
   序号 股票代码  股票简称  ... 归母净利润同比增长(06-30) 营业收入同比增长(09-30) 营业收入同比增长(06-30)
0   1  600313.SH  农发种业  ...          1433.66           35.62           18.57
1   2  000713.SZ  丰乐种业  ...           -26.10            3.59           -5.45
2   3  000998.SZ  隆平高科  ...          -421.52           55.20            6.98
3   4  300087.SZ  荃银高科  ...           421.95           28.09           42.46
4   5  300189.SZ  神农科技  ...           -39.18          -12.49          -12.68
5   6  600371.SH  万向德农  ...           174.47           11.65            3.10
6   7  600354.SH  敦煌种业  ...           -55.18           -8.59          -13.23
7   8  002041.SZ  登海种业  ...             6.67           10.01            6.12
```
