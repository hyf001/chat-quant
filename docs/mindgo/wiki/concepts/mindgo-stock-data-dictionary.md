---
title: MindGo 股票数据字典
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "data-dictionary", "stock", "catalog"]
sources: ["raw/articles/mindgo-dataplatform-detail-docs.json.md"]
confidence: high
---
# MindGo 股票数据字典

股票类数据是数据平台最大部分，覆盖 A 股基本信息、交易日历、行情、快照、资金、财务报表、公司资料、行业、概念、分析师一致预期和另类数据。函数层参考 [[mindgo-market-data-api]]、[[mindgo-security-reference-api]] 和 [[mindgo-fundamental-table-api]]。

| ID | 名称 | 分类 | 字段数 | 代码块 | 主要调用 |
| --- | --- | --- | ---: | ---: | --- |
| 77 | 分析师一致预期(A股) | 股票 / A股 / 分析师一致预期 | 12 | 2 | run_query(query_object)<br>#获取2023年2月1日的全市场股票分析师一致预期指标 |
| 16 | 历史行情快照(A股) | 股票 / A股 / 高频行情数据(A股) | 29 | 1 | get_tick(securities, start_date, end_date, fields) |
| 20 | 实时行情快照(A股) | 股票 / A股 / 高频行情数据(A股) | 30 | 1 | get_last_tick(securities, fields) |
| 1 | 股票基本信息(A股) | 股票 / A股 / 基本信息(A股) | 7 | 3 | get_all_securities(ty=None,date=None)<br>#获取2023年2月1日处于上市状态的所有A股的基本信息 |
| 5 | 交易日历(A股) | 股票 / A股 / 交易日历(A股) | 0 | 1 | get_all_trade_days() |
| 393 | 新闻评级数据 | 股票 / A股 / 另类数据 | 6 | 2 | run_query(query_object)<br>#获取全市场最近1000条利好新闻 |
| 394 | 举牌事件 | 股票 / A股 / 另类数据 | 7 | 2 | run_query(query(query_object))<br>#获取全市场历史举牌数据 |
| 395 | 实控人变更事件 | 股票 / A股 / 另类数据 | 4 | 2 | run_query(query(query_object))<br>#获取全市场历史实控人变更事件信息 |
| 396 | 定向增发事件 | 股票 / A股 / 另类数据 | 7 | 2 | run_query(query(query_object))<br>#获取全市场最近1000条利好新闻 |
| 397 | 机构调研数据 | 股票 / A股 / 另类数据 | 21 | 2 | run_query(query(query_object))<br>#获取全市场上市公司历史机构调研情况数据 |
| 538 | 龙虎榜 | 股票 / A股 / 另类数据 | 31 | 2 | get_dragon_tiger_league_table(query_object)<br>#获取2025年4月25日龙虎榜细节数据 |
| 64 | 资产负债表 | 股票 / A股 / 上市公司财务数据 | 157 | 3 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2022年报资产负债表中的总资产数据，仅取合并报表 |
| 341 | 利润表 | 股票 / A股 / 上市公司财务数据 | 98 | 0 |  |
| 342 | 现金流量表 | 股票 / A股 / 上市公司财务数据 | 123 | 3 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2022年报现金流量表中的经营活动产生的现金流量净额数据，仅取合并报表 |
| 343 | 业绩快报 | 股票 / A股 / 上市公司财务数据 | 15 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2022年报业绩快报中的归母扣非净利润数据 |
| 344 | 业绩预告 | 股票 / A股 / 上市公司财务数据 | 21 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2022年报业绩预告中的扣非净利润上限与下限 |
| 345 | 估值指标表 | 股票 / A股 / 上市公司财务数据 | 58 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期静态市盈率 |
| 346 | 偿还能力表 | 股票 / A股 / 上市公司财务数据 | 40 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期现金比率 |
| 355 | 运营能力表 | 股票 / A股 / 上市公司财务数据 | 29 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期存货周转率TTM |
| 356 | 盈利能力表 | 股票 / A股 / 上市公司财务数据 | 47 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期ROE(TTM) |
| 357 | 成长能力表 | 股票 / A股 / 上市公司财务数据 | 40 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期净利润增长率(同比) |
| 361 | 利润表(单季度) | 股票 / A股 / 上市公司财务数据 | 88 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期净利润(单季度) |
| 359 | 现金流量表(单季度) | 股票 / A股 / 上市公司财务数据 | 113 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期经营性现金流入(单季度) |
| 360 | 盈利能力表(单季度) | 股票 / A股 / 上市公司财务数据 | 10 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期ROE(单季度) |
| 358 | 成长能力表(单季度) | 股票 / A股 / 上市公司财务数据 | 5 | 2 | get_fundamentals(query_object, date=None, statDate=None, latest=False)<br>#获取全市场2023年2月1日全市场股票最近一期净利润增长率(单季度同比) |
| 81 | 公司更名信息 | 股票 / A股 / 上市公司资料 | 7 | 2 | run_query(query_object)<br>#获取全市场公司更名信息表 |
| 85 | 公司员工数量表 | 股票 / A股 / 上市公司资料 | 8 | 2 | run_query(query_object)<br>#获取全市场公司员工数量表 |
| 89 | 十大股东信息表 | 股票 / A股 / 上市公司资料 | 14 | 2 | run_query(query_object)<br>#获取全市场公司十大股东信息 |
| 93 | 十大流通股东信息表 | 股票 / A股 / 上市公司资料 | 12 | 2 | run_query(query_object)<br>#获取全市场公司十大流通股东信息 |
| 97 | 上市公司所在地 | 股票 / A股 / 上市公司资料 | 5 | 2 | run_query(query_object)<br>#获取全市场公司所在地信息 |
| 101 | 公司股本变动表 | 股票 / A股 / 上市公司资料 | 14 | 2 | run_query(query_object)<br>#获取全市场公司股本变动情况表 |
| 105 | 机构股东持股情况表 | 股票 / A股 / 上市公司资料 | 9 | 2 | run_query(query_object)<br>#获取全市场公司机构股东持股情况表 |
| 109 | 解禁明细表 | 股票 / A股 / 上市公司资料 | 10 | 2 | run_query(query_object)<br>#获取全市场公司限售股解禁情况表 |
| 113 | 配股信息表 | 股票 / A股 / 上市公司资料 | 3 | 2 | run_query(query_object)<br>#获取全市场公司配股情况表 |
| 117 | 分红送股信息 | 股票 / A股 / 上市公司资料 | 19 | 3 | run_query(query_object)<br>#获取同花顺300033.SZ历史分红送股情况及股利支付率 |
| 121 | 融资融券数据 | 股票 / A股 / 市场资金数据 | 7 | 3 | get_mtss(<br># 获取平安银行, 贵州茅台2023年2月1日前3天的融资融券余额数据 |
| 558 | 日频资金流向数据 | 股票 / A股 / 市场资金数据 | 17 | 3 | get_money_flow_step(<br>[IN]: |
| 566 | 半小时资金流向数据 | 股票 / A股 / 市场资金数据 | 17 | 3 | get_money_flow_step(<br>[IN]: |
| 574 | 五分钟资金流向数据 | 股票 / A股 / 市场资金数据 | 17 | 3 | get_money_flow_step(<br>[IN]: |
| 66 | 同花顺概念分类 | 股票 / A股 / 同花顺概念(A股) | 8 | 2 | get_concept_relate(date='now', levels=None, fields=None)<br>#获取2023年2月1日的A股概念信息 |
| 70 | 概念股数据(A股) | 股票 / A股 / 同花顺概念(A股) | 0 | 2 | get_concept_stocks(symbol, date=None)<br>#获取2023年3月31日的ChatGPT概念股 |
| 73 | 个股概念数据 | 股票 / A股 / 同花顺概念(A股) | 3 | 2 | run_query(query_object)<br>#获取同花顺300033.SZ，2023年2月1日所属概念 |
| 8 | 股票日行情数据(A股) | 股票 / A股 / 行情数据(A股) | 16 | 3 | get_price(<br>[IN]: |
| 12 | 股票分钟行情数据(A股) | 股票 / A股 / 行情数据(A股) | 9 | 3 | get_price(<br>[IN]: |
| 435 | 开盘竞价成交信息 | 股票 / A股 / 行情数据(A股) | 2 | 3 | get_call_auction(symbol, dt=None)<br>[IN]: |
| 24 | 行业分类信息 | 股票 / A股 / 行业分类 | 9 | 2 | get_industry_relate(date='now', types='industryid1', fields=None)<br>#获取2023年2月1日的同花顺一级行业分类信息 |
