---
title: "fund_etf_spot_em - ETF基金实时行情-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_spot_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金行情 > ETF基金实时行情-东财
- 描述: 东方财富-ETF 实时行情
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#fund_etf
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### ETF基金实时行情-东财

接口: fund_etf_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#fund_etf

描述: 东方财富-ETF 实时行情

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 代码         | object  | -       |
| 名称         | object  | -       |
| 最新价        | float64 | -       |
| IOPV实时估值   | float64 | -       |
| 基金折价率      | float64 | 注意单位: % |
| 涨跌额        | float64 | -       |
| 涨跌幅        | float64 | 注意单位: % |
| 成交量        | float64 | -       |
| 成交额        | float64 | -       |
| 开盘价        | float64 | -       |
| 最高价        | float64 | -       |
| 最低价        | float64 | -       |
| 昨收         | float64 | -       |
| 换手率        | float64 | -       |
| 量比         | float64 | -       |
| 委比         | float64 | -       |
| 外盘         | float64 | -       |
| 内盘         | float64 | -       |
| 主力净流入-净额   | float64 | -       |
| 主力净流入-净占比  | float64 | -       |
| 超大单净流入-净额  | float64 | -       |
| 超大单净流入-净占比 | float64 | -       |
| 大单净流入-净额   | float64 | -       |
| 大单净流入-净占比  | float64 | -       |
| 中单净流入-净额   | float64 | -       |
| 中单净流入-净占比  | float64 | -       |
| 小单净流入-净额   | float64 | -       |
| 小单净流入-净占比  | float64 | -       |
| 现手         | float64 | -       |
| 买一         | float64 | -       |
| 卖一         | float64 | -       |
| 最新份额       | float64 | -       |
| 流通市值       | int64   | -       |
| 总市值        | int64   | -       |
| 数据日期       | object  | -       |
| 更新时间       | object  | -       |

接口示例

```python
import akshare as ak

fund_etf_spot_em_df = ak.fund_etf_spot_em()
print(fund_etf_spot_em_df)
```

数据示例

```
          代码    名称  ...       数据日期                  更新时间
0     520890  港股通红利低波ETF  ... 2024-12-26 2024-12-26 16:11:57+08:00
1     159331     红利港股ETF  ... 2024-12-26 2024-12-26 15:34:48+08:00
2     159333   港股央企红利ETF  ... 2024-12-26 2024-12-26 15:34:45+08:00
3     159583     通信设备ETF  ... 2024-12-26 2024-12-26 15:35:03+08:00
4     515880       通信ETF  ... 2024-12-26 2024-12-26 16:11:33+08:00
...      ...         ...  ...        ...                       ...
1005  561170     绿电50ETF  ... 2024-12-26 2024-12-26 16:11:52+08:00
1006  562550       绿电ETF  ... 2024-12-26 2024-12-26 16:11:39+08:00
1007  159301     公用事业ETF  ... 2024-12-26 2024-12-26 15:34:36+08:00
1008  159611       电力ETF  ... 2024-12-26 2024-12-26 15:34:12+08:00
1009  560580     电力ETF南方  ... 2024-12-26 2024-12-26 16:11:52+08:00
[1010 rows x 37 columns]
```
