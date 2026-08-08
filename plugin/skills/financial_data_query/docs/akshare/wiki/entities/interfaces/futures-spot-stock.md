---
title: "futures_spot_stock - 现货与股票"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_spot_stock

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 现货与股票
- 描述: 东方财富网-数据中心-现货与股票
- 目标地址: https://data.eastmoney.com/ifdata/xhgp.html
- 限量: 单次返回指定 indicator 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 现货与股票

接口: futures_spot_stock

目标地址: https://data.eastmoney.com/ifdata/xhgp.html

描述: 东方财富网-数据中心-现货与股票

限量: 单次返回指定 indicator 的所有数据

输入参数

| 名称     | 类型  | 描述                                                                      |
|--------|-----|-------------------------------------------------------------------------|
| symbol | str | symbol="能源"; choice of {'能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副'} |

输出参数

| 名称     | 类型      | 描述        |
|--------|---------|-----------|
| 商品名称   | object  | -         |
| 近5月    | float64 | 注意: 具体的日期 |
| 近4月    | float64 | 注意: 具体的日期 |
| 近3月    | float64 | 注意: 具体的日期 |
| 近2月    | float64 | 注意: 具体的日期 |
| 近1月    | float64 | 注意: 具体的日期 |
| 最新价    | float64 | -         |
| 近半年涨跌幅 | float64 | 注意单位: %   |
| 生产商    | object  | 注意: 字符串组成 |
| 下游用户   | object  | 注意: 字符串组成 |

接口示例

```python
import akshare as ak

futures_spot_stock_df = ak.futures_spot_stock(symbol="能源")
print(futures_spot_stock_df)
```

数据示例

```
  商品名称  ...                                               下游用户
0   甲醇  ...                                                  -
1  燃料油  ...                                                  -
2  炼焦煤  ...                              美锦能源, 长春燃气, 山西焦化, 宝泰隆
3   沥青  ...                                                  -
4  液化气  ...                                                  -
5  动力煤  ...                                                  -
6   焦炭  ...  沙钢股份, 中信特钢, 抚顺特钢, 三钢闽光, 首钢股份, 华菱钢铁, 鞍钢股份, 包钢股份...
[7 rows x 10 columns]
```
