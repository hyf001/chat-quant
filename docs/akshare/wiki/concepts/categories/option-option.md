---
title: "AKShare 期权数据"
created: 2026-07-26
updated: 2026-07-26
type: concept
tags: [akshare, data-dictionary, category, option]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# AKShare 期权数据

来源页面: https://akshare.akfamily.xyz/data/option/option.html
原始快照: [option/option.md](../../raw/data-dictionary/option/option.md)

该分类从 AKShare 数据字典中抽取出 42 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。

## 接口

- [[option-cffex-hs300-daily-sina|option_cffex_hs300_daily_sina]] - 中金所-沪深300指数-指定合约-日频行情
- [[option-cffex-hs300-list-sina|option_cffex_hs300_list_sina]] - 中金所-沪深300指数-所有合约, 返回的第一个合约为主力合约
- [[option-cffex-hs300-spot-sina|option_cffex_hs300_spot_sina]] - 新浪财经-中金所-沪深300指数-指定合约-实时行情
- [[option-cffex-sz50-daily-sina|option_cffex_sz50_daily_sina]] - 中金所-上证50指数-指定合约-日频行情
- [[option-cffex-sz50-list-sina|option_cffex_sz50_list_sina]] - 中金所-上证50指数-所有合约, 返回的第一个合约为主力合约
- [[option-cffex-sz50-spot-sina|option_cffex_sz50_spot_sina]] - 新浪财经-中金所-上证50指数-指定合约-实时行情
- [[option-cffex-zz1000-daily-sina|option_cffex_zz1000_daily_sina]] - 中金所-中证1000指数-指定合约-日频行情
- [[option-cffex-zz1000-list-sina|option_cffex_zz1000_list_sina]] - 中金所-中证1000指数-所有合约, 返回的第一个合约为主力合约
- [[option-cffex-zz1000-spot-sina|option_cffex_zz1000_spot_sina]] - 新浪财经-中金所-中证1000指数-指定合约-实时行情
- [[option-comm-info|option_comm_info]] - 九期网-商品期权手续费数据
- [[option-commodity-contract-sina|option_commodity_contract_sina]] - 新浪财经-商品期权当前在交易的合约
- [[option-commodity-contract-table-sina|option_commodity_contract_table_sina]] - 新浪财经-商品期权的 T 型报价表
- [[option-commodity-hist-sina|option_commodity_hist_sina]] - 新浪财经-商品期权的历史行情数据-日频率
- [[option-contract-info-ctp|option_contract_info_ctp]] - openctp 期权合约信息
- [[option-current-day-sse|option_current_day_sse]] - 上海证券交易所-产品-股票期权-信息披露-当日合约
- [[option-current-day-szse|option_current_day_szse]] - 深圳证券交易所-期权子网-行情数据-当日合约
- [[option-current-em|option_current_em]] - 东方财富网-行情中心-期权市场
- [[option-czce-hist|option_czce_hist]] - 郑州商品交易所的商品期权历史行情数据
- [[option-daily-stats-sse|option_daily_stats_sse]] - 上海证券交易所-产品-股票期权-每日统计
- [[option-daily-stats-szse|option_daily_stats_szse]] - 深圳证券交易所-市场数据-期权数据-日度概况
- [[option-finance-board|option_finance_board]] - 上海证券交易所、深圳证券交易所、中国金融期货交易所的金融期权行情数据
- [[option-finance-minute-sina|option_finance_minute_sina]] - 新浪财经-金融期权-股票期权分时行情数据
- [[option-hist-czce|option_hist_czce]] - 郑州商品交易所-商品期权数据
- [[option-hist-dce|option_hist_dce]] - 大连商品交易所-商品期权数据
- [[option-hist-gfex|option_hist_gfex]] - 广州期货交易所-商品期权数据
- [[option-hist-shfe|option_hist_shfe]] - 上海期货交易所-商品期权数据
- [[option-lhb-em|option_lhb_em]] - 东方财富网-数据中心-期货期权-期权龙虎榜单-金融期权
- [[option-margin|option_margin]] - 唯爱期货-期权保证金
- [[option-minute-em|option_minute_em]] - 东方财富网-行情中心-期权市场-分时行情
- [[option-premium-analysis-em|option_premium_analysis_em]] - 东方财富网-数据中心-特色数据-期权折溢价
- [[option-risk-analysis-em|option_risk_analysis_em]] - 东方财富网-数据中心-特色数据-期权风险分析
- [[option-risk-indicator-sse|option_risk_indicator_sse]] - 上海证券交易所-产品-股票期权-期权风险指标数据
- [[option-sse-codes-sina|option_sse_codes_sina]] - 新浪期权-看涨看跌合约合约的代码
- [[option-sse-daily-sina|option_sse_daily_sina]] - 期权行情日数据
- [[option-sse-expire-day-sina|option_sse_expire_day_sina]] - 获取指定到期月份指定品种的剩余到期时间
- [[option-sse-greeks-sina|option_sse_greeks_sina]] - 新浪财经-期权希腊字母信息表
- [[option-sse-list-sina|option_sse_list_sina]] - 获取期权-上交所-50ETF-合约到期月份列表
- [[option-sse-minute-sina|option_sse_minute_sina]] - 期权行情分钟数据, 只能返还当天的分钟数据
- [[option-sse-spot-price-sina|option_sse_spot_price_sina]] - 期权实时数据
- [[option-sse-underlying-spot-price-sina|option_sse_underlying_spot_price_sina]] - 获取期权标的物的实时数据
- [[option-value-analysis-em|option_value_analysis_em]] - 东方财富网-数据中心-特色数据-期权价值分析
- [[option-vol-gfex|option_vol_gfex]] - 广州期货交易所-商品期权数据-隐含波动参考值

## 相关

- [[index]]
- [[_meta/topic-map]]
