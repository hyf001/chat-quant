---
title: "AKShare 期货数据"
created: 2026-07-26
updated: 2026-07-26
type: concept
tags: [akshare, data-dictionary, category, futures]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# AKShare 期货数据

来源页面: https://akshare.akfamily.xyz/data/futures/futures.html
原始快照: [futures/futures.md](../../raw/data-dictionary/futures/futures.md)

该分类从 AKShare 数据字典中抽取出 54 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。

## 接口

- [[futures-comex-inventory|futures_comex_inventory]] - 东方财富网-数据中心-期货期权-COMEX 库存数据
- [[futures-comm-info|futures_comm_info]] - 九期网-期货手续费数据
- [[futures-comm-js|futures_comm_js]] - 金十财经-期货手续费数据
- [[futures-contract-detail|futures_contract_detail]] - 新浪财经-期货-期货合约详情数据
- [[futures-contract-detail-em|futures_contract_detail_em]] - 东方财富-期货-期货合约详情数据
- [[futures-contract-info-cffex|futures_contract_info_cffex]] - 中国金融期货交易所-数据-交易参数
- [[futures-contract-info-czce|futures_contract_info_czce]] - 郑州商品交易所-交易数据-参考数据
- [[futures-contract-info-dce|futures_contract_info_dce]] - 大连商品交易所-数据中心-业务数据-交易参数-合约信息
- [[futures-contract-info-gfex|futures_contract_info_gfex]] - 广州期货交易所-业务/服务-合约信息
- [[futures-contract-info-ine|futures_contract_info_ine]] - 上海国际能源交易中心-业务指南-交易参数汇总(期货)
- [[futures-contract-info-shfe|futures_contract_info_shfe]] - 上海期货交易所-交易所服务-业务数据-交易参数汇总查询
- [[futures-dce-position-rank|futures_dce_position_rank]] - 大连商品交易所指定交易日的具体合约的持仓排名
- [[futures-delivery-czce|futures_delivery_czce]] - 郑州商品交易所-交割统计
- [[futures-delivery-dce|futures_delivery_dce]] - 大连商品交易所-交割统计
- [[futures-delivery-match-czce|futures_delivery_match_czce]] - 郑州商品交易所-交割配对
- [[futures-delivery-match-dce|futures_delivery_match_dce]] - 大连商品交易所-交割配对
- [[futures-delivery-shfe|futures_delivery_shfe]] - 上海期货交易所-交割统计
- [[futures-fees-info|futures_fees_info]] - openctp 期货交易费用参照表
- [[futures-foreign-commodity-realtime|futures_foreign_commodity_realtime]] - 新浪财经-外盘商品期货数据
- [[futures-foreign-detail|futures_foreign_detail]] - 新浪财经-期货外盘期货合约详情
- [[futures-foreign-hist|futures_foreign_hist]] - 新浪财经-期货外盘历史行情数据
- [[futures-gfex-position-rank|futures_gfex_position_rank]] - 广州期货交易所-日成交持仓排名
- [[futures-gfex-warehouse-receipt|futures_gfex_warehouse_receipt]] - 广州期货交易所-行情数据-仓单日报
- [[futures-global-hist-em|futures_global_hist_em]] - 东方财富网-行情中心-期货市场-国际期货-历史行情数据
- [[futures-global-spot-em|futures_global_spot_em]] - 东方财富网-行情中心-期货市场-国际期货-实时行情数据
- [[futures-hist-em|futures_hist_em]] - 东方财富网-期货行情-行情数据；其中 weekly, monthly 获取的成交额和持仓量未经验证
- [[futures-hog-core|futures_hog_core]] - 玄田数据-核心数据
- [[futures-hog-cost|futures_hog_cost]] - 玄田数据-成本维度
- [[futures-hog-supply|futures_hog_supply]] - 玄田数据-供应维度
- [[futures-hold-pos-sina|futures_hold_pos_sina]] - 新浪财经-期货-成交持仓
- [[futures-hq-subscribe-exchange-symbol|futures_hq_subscribe_exchange_symbol]] - 新浪财经-外盘商品期货品种代码表数据
- [[futures-index-ccidx|futures_index_ccidx]] - 中证商品指数
- [[futures-inventory-99|futures_inventory_99]] - 99 期货网-大宗商品库存数据
- [[futures-inventory-em|futures_inventory_em]] - 东方财富网-期货数据-库存数据; 近 60 个交易日的期货库存日频率数据
- [[futures-main-sina|futures_main_sina]] - 新浪财经-期货-主力连续合约历史数据
- [[futures-news-shmet|futures_news_shmet]] - 上海金属网-快讯
- [[futures-rule|futures_rule]] - 国泰君安期货-交易日历数据表
- [[futures-settle|futures_settle]] - 提供各交易所的结算参数数据，包括保证金、手续费、涨跌停板等参数
- [[futures-settlement-price-sgx|futures_settlement_price_sgx]] - 新加坡交易所-衍生品-历史数据-历史结算价格; 数据于下个工作日新加坡时间下午 2 点起提供
- [[futures-shfe-warehouse-receipt|futures_shfe_warehouse_receipt]] - 提供上海期货交易所指定交割仓库期货仓单日报
- [[futures-spot-stock|futures_spot_stock]] - 东方财富网-数据中心-现货与股票
- [[futures-spot-sys|futures_spot_sys]] - 生意社-商品与期货-现期图
- [[futures-stock-shfe-js|futures_stock_shfe_js]] - 金十财经-上海期货交易所指定交割仓库库存周报
- [[futures-to-spot-czce|futures_to_spot_czce]] - 郑州商品交易所-期转现统计数据
- [[futures-to-spot-dce|futures_to_spot_dce]] - 大连商品交易所-期转现统计数据
- [[futures-to-spot-shfe|futures_to_spot_shfe]] - 上海期货交易所-期转现数据
- [[futures-warehouse-receipt-czce|futures_warehouse_receipt_czce]] - 郑州商品交易所-交易数据-仓单日报
- [[futures-warehouse-receipt-dce|futures_warehouse_receipt_dce]] - 大连商品交易所-行情数据-统计数据-日统计-仓单日报
- [[futures-zh-daily-sina|futures_zh_daily_sina]] - 新浪财经-期货-日频数据
- [[futures-zh-minute-sina|futures_zh_minute_sina]] - 新浪财经-期货-分时数据
- [[futures-zh-realtime|futures_zh_realtime]] - 新浪财经-期货实时行情数据
- [[futures-zh-spot|futures_zh_spot]] - 新浪财经-期货页面的实时行情数据
- [[get-futures-daily|get_futures_daily]] - 提供各交易所各品种的网站的历史行情数据, 其中 20040625, 20070604, 20081226, 20090119 原网页数据缺失
- [[index-hog-spot-price|index_hog_spot_price]] - 行情宝-生猪市场价格指数

## 相关

- [[index]]
- [[_meta/topic-map]]
