---
title: "AKShare 公募基金数据"
created: 2026-07-26
updated: 2026-07-26
type: concept
tags: [akshare, data-dictionary, category, fund]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# AKShare 公募基金数据

来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html
原始快照: [fund/fund_public.md](../../raw/data-dictionary/fund/fund_public.md)

该分类从 AKShare 数据字典中抽取出 76 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。

## 接口

- [[fund-announcement-dividend-em|fund_announcement_dividend_em]] - 东方财富网站-天天基金网-基金档案-基金公告-分红配送
- [[fund-announcement-personnel-em|fund_announcement_personnel_em]] - 东方财富网站-天天基金网-基金档案-基金公告-人事调整
- [[fund-announcement-report-em|fund_announcement_report_em]] - 东方财富网站-天天基金网-基金档案-基金公告-定期报告
- [[fund-aum-em|fund_aum_em]] - 天天基金网-基金数据-基金规模
- [[fund-aum-hist-em|fund_aum_hist_em]] - 天天基金网-基金数据-基金公司历年管理规模排行列表
- [[fund-aum-trend-em|fund_aum_trend_em]] - 天天基金网-基金数据-市场全部基金规模走势
- [[fund-balance-position-lg|fund_balance_position_lg]] - 乐咕乐股-基金仓位-平衡混合型基金仓位
- [[fund-cf-em|fund_cf_em]] - 天天基金网-基金数据-分红送配-基金拆分
- [[fund-etf-category-sina|fund_etf_category_sina]] - 新浪财经-基金列表及行情数据
- [[fund-etf-category-ths|fund_etf_category_ths]] - 同花顺理财-基金数据-每日净值-实时行情
- [[fund-etf-dividend-sina|fund_etf_dividend_sina]] - 新浪财经-基金-ETF 基金-累计分红
- [[fund-etf-fund-daily-em|fund_etf_fund_daily_em]] - 东方财富网站-天天基金网-基金数据-场内交易基金-实时数据, 此接口数据每个交易日 **16:00～23:00**
- [[fund-etf-fund-info-em|fund_etf_fund_info_em]] - 东方财富网站-天天基金网-基金数据-场内交易基金-历史净值数据
- [[fund-etf-hist-em|fund_etf_hist_em]] - 东方财富-ETF 行情; 历史数据按日频率更新, 当日收盘价请在收盘后获取
- [[fund-etf-hist-min-em|fund_etf_hist_min_em]] - 东方财富-ETF 分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置
- [[fund-etf-hist-sina|fund_etf_hist_sina]] - 新浪财经-基金行情的日频率行情数据
- [[fund-etf-scale-sse|fund_etf_scale_sse]] - 上海证券交易所-产品-基金产品-ETF产品-ETF产品列表-基金规模
- [[fund-etf-scale-szse|fund_etf_scale_szse]] - 深圳证券交易所-基金产品-基金列表-ETF基金份额
- [[fund-etf-spot-em|fund_etf_spot_em]] - 东方财富-ETF 实时行情
- [[fund-etf-spot-ths|fund_etf_spot_ths]] - 同花顺理财-基金数据-每日净值-ETF-实时行情
- [[fund-exchange-rank-em|fund_exchange_rank_em]] - 东方财富网-数据中心-场内交易基金排行榜
- [[fund-fee-em|fund_fee_em]] - 天天基金-基金档案-购买信息
- [[fund-fh-em|fund_fh_em]] - 天天基金网-基金数据-分红送配-基金分红
- [[fund-fh-rank-em|fund_fh_rank_em]] - 天天基金网-基金数据-分红送配-基金分红排行
- [[fund-financial-fund-daily-em|fund_financial_fund_daily_em]] - 东方财富网-天天基金网-基金数据-理财型基金-实时数据, 此接口数据每个交易日 **16:00～23:00** 更新
- [[fund-financial-fund-info-em|fund_financial_fund_info_em]] - 东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细
- [[fund-graded-fund-daily-em|fund_graded_fund_daily_em]] - 东方财富网-天天基金网-基金数据-分级基金-实时数据, 此接口数据每个交易日 **16:00～23:00**
- [[fund-graded-fund-info-em|fund_graded_fund_info_em]] - 东方财富网站-天天基金网-基金数据-分级基金-历史数据
- [[fund-hk-fund-hist-em|fund_hk_fund_hist_em]] - 东方财富网站-天天基金网-基金数据-香港基金-历史净值明细
- [[fund-hk-rank-em|fund_hk_rank_em]] - 东方财富网-数据中心-基金排行-香港基金排行
- [[fund-hold-structure-em|fund_hold_structure_em]] - 天天基金网-基金数据-规模份额-持有人结构
- [[fund-individual-achievement-xq|fund_individual_achievement_xq]] - 雪球基金-基金详情-基金业绩-详情
- [[fund-individual-analysis-xq|fund_individual_analysis_xq]] - 雪球基金-基金详情-数据分析
- [[fund-individual-basic-info-xq|fund_individual_basic_info_xq]] - 雪球基金-基金详情
- [[fund-individual-detail-hold-xq|fund_individual_detail_hold_xq]] - 雪球基金-基金详情-基金持仓-详情
- [[fund-individual-detail-info-xq|fund_individual_detail_info_xq]] - 雪球基金-基金详情-基金交易规则
- [[fund-individual-profit-probability-xq|fund_individual_profit_probability_xq]] - 雪球基金-基金详情-盈利概率；历史任意时点买入，持有满X时间，盈利概率，以及平均收益
- [[fund-info-index-em|fund_info_index_em]] - 东方财富网-天天基金网-基金数据-基金基本信息-指数型
- [[fund-info-ths|fund_info_ths]] - 同花顺-基金数据-基金基本信息
- [[fund-lcx-rank-em|fund_lcx_rank_em]] - 东方财富网-数据中心-理财基金排行, 每个交易日17点后更新, 货币基金的单位净值均为 1.0000 元，最新一年期定存利率: 1.50%
- [[fund-linghuo-position-lg|fund_linghuo_position_lg]] - 乐咕乐股-基金仓位-灵活配置型基金仓位
- [[fund-lof-hist-em|fund_lof_hist_em]] - 东方财富-LOF 行情; 历史数据按日频率更新, 当日收盘价请在收盘后获取
- [[fund-lof-hist-min-em|fund_lof_hist_min_em]] - 东方财富-LOF 分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置
- [[fund-lof-spot-em|fund_lof_spot_em]] - 东方财富-LOF 实时行情
- [[fund-manager-em|fund_manager_em]] - 天天基金网-基金数据-基金经理大全
- [[fund-money-fund-daily-em|fund_money_fund_daily_em]] - 东方财富网-天天基金网-基金数据-货币型基金收益, 此接口数据每个交易日 **16:00～23:00**
- [[fund-money-fund-info-em|fund_money_fund_info_em]] - 东方财富网-天天基金网-基金数据-货币型基金-历史净值
- [[fund-money-rank-em|fund_money_rank_em]] - 东方财富网-数据中心-货币型基金排行
- [[fund-name-em|fund_name_em]] - 东方财富网-天天基金网-基金数据-所有基金的基本信息数据
- [[fund-new-found-em|fund_new_found_em]] - 天天基金网-基金数据-新发基金-新成立基金
- [[fund-new-found-ths|fund_new_found_ths]] - 天天基金网-基金数据-新发基金-新成立基金
- [[fund-open-fund-daily-em|fund_open_fund_daily_em]] - 东方财富网-天天基金网-基金数据, 此接口在每个交易日 **16:00-23:00** 更新当日的最新开放式基金净值数据
- [[fund-open-fund-info-em|fund_open_fund_info_em]] - 东方财富网-天天基金网-基金数据-具体基金信息
- [[fund-open-fund-rank-em|fund_open_fund_rank_em]] - 东方财富网-数据中心-开放式基金排行
- [[fund-overview-em|fund_overview_em]] - 天天基金-基金档案-基本概况
- [[fund-portfolio-bond-hold-em|fund_portfolio_bond_hold_em]] - 天天基金网-基金档案-投资组合-债券持仓
- [[fund-portfolio-change-em|fund_portfolio_change_em]] - 天天基金网-基金档案-投资组合-重大变动
- [[fund-portfolio-hold-em|fund_portfolio_hold_em]] - 天天基金网-基金档案-投资组合-基金持仓
- [[fund-portfolio-industry-allocation-em|fund_portfolio_industry_allocation_em]] - 天天基金网-基金档案-投资组合-行业配置
- [[fund-purchase-em|fund_purchase_em]] - 东方财富网站-天天基金网-基金数据-基金申购状态
- [[fund-rating-all|fund_rating_all]] - 天天基金网-基金评级-基金评级总汇
- [[fund-rating-ja|fund_rating_ja]] - 天天基金网-基金评级-济安金信评级
- [[fund-rating-sh|fund_rating_sh]] - 天天基金网-基金评级-上海证券评级
- [[fund-rating-zs|fund_rating_zs]] - 天天基金网-基金评级-招商证券评级
- [[fund-report-asset-allocation-cninfo|fund_report_asset_allocation_cninfo]] - 巨潮资讯-数据中心-专题统计-基金报表-基金资产配置
- [[fund-report-industry-allocation-cninfo|fund_report_industry_allocation_cninfo]] - 巨潮资讯-数据中心-专题统计-基金报表-基金行业配置
- [[fund-report-stock-cninfo|fund_report_stock_cninfo]] - 巨潮资讯-数据中心-专题统计-基金报表-基金重仓股
- [[fund-scale-change-em|fund_scale_change_em]] - 天天基金网-基金数据-规模份额-规模变动
- [[fund-scale-close-sina|fund_scale_close_sina]] - 基金数据中心-基金规模-封闭式基金
- [[fund-scale-daily-szse|fund_scale_daily_szse]] - 深圳证券交易所-基金产品-基金规模-日频数据
- [[fund-scale-open-sina|fund_scale_open_sina]] - 基金数据中心-基金规模-开放式基金
- [[fund-scale-structured-sina|fund_scale_structured_sina]] - 基金数据中心-基金规模-分级子基金
- [[fund-stock-position-lg|fund_stock_position_lg]] - 乐咕乐股-基金仓位-股票型基金仓位
- [[fund-value-estimation-em|fund_value_estimation_em]] - 东方财富网-数据中心-净值估算
- [[reits-hist-em|reits_hist_em]] - 东方财富网-行情中心-REITs-沪深 REITs-历史行情
- [[reits-realtime-em|reits_realtime_em]] - 东方财富网-行情中心-REITs-沪深 REITs-实时行情

## 相关

- [[index]]
- [[_meta/topic-map]]
