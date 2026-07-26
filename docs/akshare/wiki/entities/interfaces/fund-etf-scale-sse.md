---
title: "fund_etf_scale_sse - ETF 基金份额-上交所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_scale_sse

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > ETF 基金份额-上交所
- 描述: 上海证券交易所-产品-基金产品-ETF产品-ETF产品列表-基金规模
- 目标地址: https://www.sse.com.cn/assortment/fund/etf/list/scale/
- 限量: 单次返回指定日期的 ETF 基金份额数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### ETF 基金份额-上交所

接口: fund_etf_scale_sse

目标地址: https://www.sse.com.cn/assortment/fund/etf/list/scale/

描述: 上海证券交易所-产品-基金产品-ETF产品-ETF产品列表-基金规模

限量: 单次返回指定日期的 ETF 基金份额数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20250115" |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 序号    | int64   | -  |
| 基金代码  | object  | -  |
| 基金简称  | object  | -  |
| ETF类型 | object  | -  |
| 统计日期  | object  | -  |
| 基金份额  | float64 | -  |

接口示例

```python
import akshare as ak

fund_etf_scale_sse_df = ak.fund_etf_scale_sse(date="20250115")
print(fund_etf_scale_sse_df)
```

数据示例

```
      序号 基金代码  基金简称 ETF类型  统计日期        基金份额
0      1  510010   治理ETF    单市  2025-01-15    20152.44
1      2  510020   超大ETF    单市  2025-01-15     4324.80
2      3  510030   价值ETF    单市  2025-01-15    21122.98
3      4  510040  上证180E    单市  2025-01-15    56448.00
4      5  510050   50ETF    单市  2025-01-15  5533716.68
..   ...     ...     ...   ...         ...         ...
588  589  588880    科创指数    单市  2025-01-15    46836.80
589  590  588890     科创芯    单市  2025-01-15    23381.00
590  591  588900  科创100N    单市  2025-01-15    40678.30
591  592  588930   科创板AI    单市  2025-01-15    16532.90
592  593  588990     科芯片    单市  2025-01-15    14574.54
[593 rows x 6 columns]
```
