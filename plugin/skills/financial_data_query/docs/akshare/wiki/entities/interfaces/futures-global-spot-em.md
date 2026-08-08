---
title: "futures_global_spot_em - 外盘-实时行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_global_spot_em

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 外盘-实时行情数据-东财
- 描述: 东方财富网-行情中心-期货市场-国际期货-实时行情数据
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#futures_global
- 限量: 单次返回所有期货品种的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 外盘-实时行情数据-东财

接口: futures_global_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#futures_global

描述: 东方财富网-行情中心-期货市场-国际期货-实时行情数据

限量: 单次返回所有期货品种的实时行情数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 序号  | int64   | -       |
| 代码  | object  | -       |
| 名称  | object  | -       |
| 最新价 | float64 | -       |
| 涨跌额 | float64 | -       |
| 涨跌幅 | float64 | 注意单位: % |
| 今开  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 昨结  | float64 | -       |
| 成交量 | int64   | -       |
| 买盘  | int64   | -       |
| 卖盘  | int64   | -       |
| 持仓量 | int64   | -       |

接口示例

```python
import akshare as ak

futures_global_spot_em_df = ak.futures_global_spot_em()
print(futures_global_spot_em_df)
```

数据示例

```
     序号  代码           名称        最新价  ...   成交量  买盘  卖盘    持仓量
0      1   NG00Y          天然气      3.252  ...  15662  8269  7393  305016
1      2   NG25F      天然气2501      3.252  ...  15662  8269  7393  305016
2      3  JRU24Z      日橡胶2412    380.000  ...      3     3     0      69
3      4    LNKT        综合镍03  16100.000  ...      0     0     0       0
4      5  JRU25G      日橡胶2502    376.000  ...     11    11     0     495
..   ...     ...          ...        ...  ...    ...   ...   ...     ...
615  616    M25G      天然气2502    119.310  ...    815   495   320   47830
616  617  MPM25K      棕榈油2505   4570.000  ...    859   621   238   20731
617  618  MPM25X      棕榈油2511   4235.000  ...      3     3     0    3189
618  619   GC25Z  COMEX黄金2512   2756.200  ...     25     8    17    8537
619  620   SB26K     糖11号2605     18.470  ...   2742  1289  1453   29289
[620 rows x 14 columns]
```
