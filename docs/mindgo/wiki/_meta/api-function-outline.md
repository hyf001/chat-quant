---
title: API Function Outline
created: 2026-08-11
updated: 2026-08-11
type: summary
tags: ["mindgo", "api", "catalog"]
sources: ["raw/articles/mindgo-api-docs-help-4.md"]
confidence: high
---
# API Function Outline

本页是 [[mindgo-api-docs]] 的标题索引，帮助快速定位 API 区域。

| Line | Level | Heading |
| ---: | ---: | --- |
| 1 | 1 | API文档 |
| 42 | 2 | 回测引擎专用API |
| 53 | 3 | [重要！！]写在最前面 |
| 61 | 3 | 基本函数 |
| 262 | 3 | 自定义运行函数 |
| 361 | 3 | 设置函数 |
| 1015 | 3 | 数据函数 |
| 1466 | 3 | 交易函数 |
| 2173 | 3 | 枚举常量 |
| 2215 | 3 | 重要对象 |
| 2513 | 3 | 辅助函数 |
| 2624 | 2 | 工具函数 |
| 2625 | 3 | 股票代码格式转换：normalize_symbol |
| 2662 | 3 | 保存文件函数：write_file |
| 2691 | 3 | 读取文件函数：read_file |
| 2730 | 3 | 查询研究环境指定路径下的文件：list_file |
| 2766 | 3 | 复制/剪贴文件或文件夹：copy_file |
| 2794 | 3 | 删除文件或文件夹：remove_file |
| 2820 | 3 | 消息推送函数：notify_push |
| 2875 | 3 | 自选板块：custom_sector |
| 2909 | 3 | 文件加密：compile_pyfile |
| 2926 | 1 | 编译加密py文件 |
| 2938 | 2 | 行情资金数据接口 |
| 2939 | 3 | 行情数据：get_price |
| 3030 | 3 | 开盘竞价成交信息：get_call_auction |
| 3068 | 3 | 期货行情数据：get_price_future |
| 3180 | 3 | 蜡烛图数据：get_candle_stick |
| 3240 | 3 | 获取实时行情快照数据：get_last_tick |
| 3279 | 3 | 获取历史行情快照数据：get_tick |
| 3313 | 3 | 统计涨跌区间个股数量：get_stats |
| 3337 | 3 | 压力支撑位数据：get_resistance_support |
| 3408 | 3 | 获取基金净值数据：get_extras |
| 3477 | 3 | 融资融券数据：get_mtss |
| 3541 | 3 | 获取历史资金数据：get_money_flow_step |
| 3652 | 2 | 证券信息数据接口 |
| 3653 | 3 | 获取单只证券的基本信息：get_security_info |
| 3686 | 3 | 获取所有证券信息：get_all_securities |
| 3761 | 3 | 获取期货期权品种相关信息：get_futures_info |
| 3797 | 3 | 获取主力合约代码：get_futures_dominate |
| 3817 | 3 | 获取指定品种所有可交易的合约：get_future_code |
| 3848 | 3 | 获取可交易的期权合约列表：get_option_code |
| 3876 | 3 | 获取指数成份股：get_index_stocks |
| 3909 | 3 | 获取指数成份股权重：get_index_weight |
| 3948 | 3 | 获取指数列表：get_index_list |
| 3974 | 3 | 获取行业成份股：get_industry_stocks |
| 3999 | 3 | 获取行业分类信息：get_industry_relate |
| 4039 | 3 | 获取股票所属行业数据：get_symbol_industry |
| 4063 | 3 | 获取所有同花顺概念成分股：get_concept_stocks |
| 4090 | 3 | 获取所有同花顺概念信息：get_concept_relate |
| 4123 | 3 | 获取指定时间段交易日：get_trade_days |
| 4156 | 3 | 获取所有交易日：get_all_trade_days |
| 4183 | 3 | 获取因子数据：get_sfactor_data |
| 4228 | 2 | 表数据接口 |
| 4442 | 2 | 问财接口 |
| 4443 | 3 | 问财接口使用前必读 |
| 4455 | 3 | 问财实时数据：query_iwencai (研究环境使用) |
| 4495 | 3 | 问财昨日数据：get_iwencai(回测环境使用) |
| 4551 | 3 | 问财接口是否支持本地接口调用？ |
| 4555 | 3 | 市面ZUI全！一文讲透问财语句深度使用技巧（含50个案例） |
| 4560 | 2 | 组合优化器 |
| 4562 | 3 | 构造组合优化 |
| 4645 | 1 | 从中证500中随机选取50股票，模拟中证500走势，周频调仓 |
| 4646 | 1 | Stratified Sampling 方法优点： |
