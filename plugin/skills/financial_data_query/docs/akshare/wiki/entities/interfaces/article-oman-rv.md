---
title: "article_oman_rv - Oxford-Man"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, article, parameters, returns, example]
sources: [raw/data-dictionary/article/article.md]
confidence: high
---
# article_oman_rv

- 分类: [[article-article|AKShare 波动率数据]]
- 主题路径: AKShare 波动率数据 > 已实现波动率数据 > Oxford-Man
- 描述: 获取 Oxford-Man 已实现波动率数据
- 目标地址: https://realized.oxford-man.ox.ac.uk/data/visualization
- 限量: 单次返回某个指数具体指标的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/article/article.html

## 相关

- [[article-article|AKShare 波动率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### Oxford-Man

接口: article_oman_rv

目标地址: https://realized.oxford-man.ox.ac.uk/data/visualization

描述: 获取 Oxford-Man 已实现波动率数据

限量: 单次返回某个指数具体指标的所有历史数据

输入参数

| 名称     | 类型  | 描述                                        |
|--------|-----|-------------------------------------------|
| symbol | str | symbol="FTSE", 具体指数请查看如下 **已实现波动率指数一览表**  |
| index  | str | index="rk_th2", 具体指标请查看如下 **已实现波动率指标一览表** |

已实现波动率指数一览表

| Symbol    | Name                                      | Earliest Available | Latest Available  |
|-----------|-------------------------------------------|--------------------|-------------------|
| .AEX      | AEX index                                 | January 03, 2000   | November 28, 2019 |
| .AORD     | All Ordinaries                            | January 04, 2000   | November 28, 2019 |
| .BFX      | Bell 20 Index                             | January 03, 2000   | November 28, 2019 |
| .BSESN    | S&P BSE Sensex                            | January 03, 2000   | November 28, 2019 |
| .BVLG     | PSI All-Share Index                       | October 15, 2012   | November 28, 2019 |
| .BVSP     | BVSP BOVESPA Index                        | January 03, 2000   | November 28, 2019 |
| .DJI      | Dow Jones Industrial Average              | January 03, 2000   | November 27, 2019 |
| .FCHI     | CAC 40                                    | January 03, 2000   | November 28, 2019 |
| .FTMIB    | FTSE MIB                                  | June 01, 2009      | November 28, 2019 |
| .FTSE     | FTSE 100                                  | January 04, 2000   | November 28, 2019 |
| .GDAXI    | DAX                                       | January 03, 2000   | November 28, 2019 |
| .GSPTSE   | S&P/TSX Composite index                   | May 02, 2002       | November 28, 2019 |
| .HSI      | HANG SENG Index                           | January 03, 2000   | November 28, 2019 |
| .IBEX     | IBEX 35 Index                             | January 03, 2000   | November 28, 2019 |
| .IXIC     | Nasdaq 100                                | January 03, 2000   | November 27, 2019 |
| .KS11     | Korea Composite Stock Price Index (KOSPI) | January 04, 2000   | November 28, 2019 |
| .KSE      | Karachi SE 100 Index                      | January 03, 2000   | November 28, 2019 |
| .MXX      | IPC Mexico                                | January 03, 2000   | November 28, 2019 |
| .N225     | Nikkei 225                                | February 02, 2000  | November 28, 2019 |
| .NSEI     | NIFTY 50                                  | January 03, 2000   | November 28, 2019 |
| .OMXC20   | OMX Copenhagen 20 Index                   | October 03, 2005   | November 28, 2019 |
| .OMXHPI   | OMX Helsinki All Share Index              | October 03, 2005   | November 28, 2019 |
| .OMXSPI   | OMX Stockholm All Share Index             | October 03, 2005   | November 28, 2019 |
| .OSEAX    | Oslo Exchange All-share Index             | September 03, 2001 | November 28, 2019 |
| .RUT      | Russel 2000                               | January 03, 2000   | November 27, 2019 |
| .SMSI     | Madrid General Index                      | July 04, 2005      | November 28, 2019 |
| .SPX      | S&P 500 Index                             | January 03, 2000   | November 27, 2019 |
| .SSEC     | Shanghai Composite Index                  | January 04, 2000   | November 28, 2019 |
| .SSMI     | Swiss Stock Market Index                  | January 04, 2000   | November 28, 2019 |
| .STI      | Straits Times Index                       | January 03, 2000   | November 28, 2019 |
| .STOXX50E | EURO STOXX 50                             | January 03, 2000   | November 28, 2019 |

已实现波动率指标一览表

| Code          | Description                                   |
|---------------|-----------------------------------------------|
| bv            | Bipower Variation (5-min)                     |
| bv_ss         | Bipower Variation (5-min Sub-sampled)         |
| close_price   | Closing (Last) Price                          |
| close_time    | Closing Time                                  |
| medrv         | Median Realized Variance (5-min)              |
| nobs          | Number of Observations                        |
| open_price    | Opening (First) Price                         |
| open_time     | Opening Time                                  |
| open_to_close | Open to Close Return                          |
| rk_parzen     | Realized Kernel Variance (Non-Flat Parzen)    |
| rk_th2        | Realized Kernel Variance (Tukey-Hanning(2))   |
| rk_twoscale   | Realized Kernel Variance (Two-Scale/Bartlett) |
| rsv           | Realized Semi-variance (5-min)                |
| rsv_ss        | Realized Semi-variance (5-min Sub-sampled)    |
| rv10          | Realized Variance (10-min)                    |
| rv10_ss       | Realized Variance (10-min Sub-sampled)        |
| rv5           | Realized Variance (5-min)                     |
| rv5_ss        | Realized Variance (5-min Sub-sampled)         |

输出参数

Oxford-Man-已实现波动率数据

| 名称    | 类型                | 描述 |
|-------|-------------------|----|
| index | datetime.datetime | 日期 |
| data  | float             | 数据 |

接口示例

```python
import akshare as ak

article_oman_rv_df = ak.article_oman_rv(symbol="FTSE", index="rk_th2")
print(article_oman_rv_df)
```

数据示例
```
2000-01-04    22.95
2000-01-05    19.37
2000-01-06    18.22
2000-01-07    19.34
2000-01-10    15.67
              ...
2019-11-04     6.71
2019-11-05     5.90
2019-11-06     6.43
2019-11-07     5.81
2019-11-08     6.75
```
