---
title: "fund_scale_daily_szse - 基金规模日频-深交所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_scale_daily_szse

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > 基金规模日频-深交所
- 描述: 深圳证券交易所-基金产品-基金规模-日频数据
- 目标地址: http://www.szse.cn/market/fund/volume/etf/index.html
- 限量: 单次返回指定日期区间和基金类别的基金规模数据; 日期范围不能超过 6 个月, 否则返回带表头的空 DataFrame
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金规模日频-深交所

接口: fund_scale_daily_szse

目标地址: http://www.szse.cn/market/fund/volume/etf/index.html

描述: 深圳证券交易所-基金产品-基金规模-日频数据

限量: 单次返回指定日期区间和基金类别的基金规模数据; 日期范围不能超过 6 个月, 否则返回带表头的空 DataFrame

输入参数

| 名称         | 类型  | 描述                                                         |
|------------|-----|------------------------------------------------------------|
| start_date | str | 开始日期, 格式为 "YYYYMMDD"                                       |
| end_date   | str | 结束日期, 格式为 "YYYYMMDD"                                       |
| symbol     | str | 基金类别, choice of {"ETF", "LOF", "REITS"}; REITS 映射为 "不动产基金" |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
| 基金代码 | object  | -  |
| 基金简称 | object  | -  |
| 基金份额 | float64 | -  |

接口示例

```python
import akshare as ak

fund_scale_daily_szse_df = ak.fund_scale_daily_szse(start_date="20260401", end_date="20260402", symbol="ETF")
print(fund_scale_daily_szse_df)
```

数据示例

```
             日期    基金代码          基金简称          基金份额
0    2026-04-02  159001    保证金ETF博时  1.802765e+07
1    2026-04-02  159003     招商快线ETF  1.994149e+06
2    2026-04-02  159005    添富快钱ETF  7.813720e+05
3    2026-04-02  159100     纳指ETF鹏华  3.865469e+08
4    2026-04-02  159101  港股通科技ETF工银  3.902311e+09
..          ...     ...           ...           ...
1253 2026-04-01  159994     通信ETF银华  2.117003e+09
1254 2026-04-01  159995     芯片ETF华夏  1.406836e+10
1255 2026-04-01  159996     家电ETF国泰  8.325548e+08
1256 2026-04-01  159997     电子ETF天弘  7.343066e+08
1257 2026-04-01  159998    创业板ETF南方  2.209055e+09
[1258 rows x 4 columns]
```
