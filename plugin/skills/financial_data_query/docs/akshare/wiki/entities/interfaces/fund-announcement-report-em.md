---
title: "fund_announcement_report_em - 定期报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_announcement_report_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金公告 > 定期报告
- 描述: 东方财富网站-天天基金网-基金档案-基金公告-定期报告
- 目标地址: https://fundf10.eastmoney.com/jjgg_000001_3.html
- 限量: 返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 定期报告

接口: fund_announcement_report_em

目标地址: https://fundf10.eastmoney.com/jjgg_000001_3.html

描述: 东方财富网站-天天基金网-基金档案-基金公告-定期报告

限量: 返回所有历史数据

输入参数

| 名称     | 类型  | 描述                                 |
|--------|-----|------------------------------------|
| symbol | str | 基金代码，可以通过调用 ak.fund_name_em() 接口获取 |

输出参数

| 名称   | 类型     | 描述                     |
|------|--------|------------------------|
| 基金代码 | object | 基金代码                   |
| 公告标题 | object | -                      |
| 基金名称 | object | 基金名称                   |
| 公告日期 | object | 公告的发布日期                |
| 报告ID | object | 获取报告详情的依据; 拼接后可以获取公告地址 |

接口示例

```python
import akshare as ak

fund_announcement_report_em_df = ak.fund_announcement_report_em(symbol="000001")
print(fund_announcement_report_em_df)
```

数据示例

```
      基金代码                   公告标题    基金名称        公告日期                  报告ID
0   000001         华夏成长：2011年年度报告  华夏成长混合  2012-03-30  AN201203300005099372
1   000001       华夏成长：2012年第一季度报告  华夏成长混合  2012-04-23  AN201205070005160501
2   000001       华夏成长：2012年第二季度报告  华夏成长混合  2012-07-18  AN201207180005363504
3   000001        华夏成长：2012年半年度报告  华夏成长混合  2012-08-28  AN201208280005468375
4   000001      华夏成长：2012年半年度报告摘要  华夏成长混合  2012-08-28  AN201208280005468376
..     ...                    ...     ...         ...                   ...
95  000001  华夏成长证券投资基金2024年第4季度报告  华夏成长混合  2025-01-22  AN202501221642432601
96  000001    华夏成长证券投资基金2024年年度报告  华夏成长混合  2025-03-31  AN202503311649448425
97  000001  华夏成长证券投资基金2025年第1季度报告  华夏成长混合  2025-04-22  AN202504221660344553
98  000001  华夏成长证券投资基金2025年第2季度报告  华夏成长混合  2025-07-21  AN202507211712819893
99  000001    华夏成长证券投资基金2025年中期报告  华夏成长混合  2025-08-30  AN202508301736777385
[100 rows x 5 columns]
```
