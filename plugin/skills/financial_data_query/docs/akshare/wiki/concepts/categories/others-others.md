---
title: "AKShare 另类数据"
created: 2026-07-26
updated: 2026-07-26
type: concept
tags: [akshare, data-dictionary, category, others]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# AKShare 另类数据

来源页面: https://akshare.akfamily.xyz/data/others/others.html
原始快照: [others/others.md](../../raw/data-dictionary/others/others.md)

该分类从 AKShare 数据字典中抽取出 35 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。

## 接口

- [[air-city-table|air_city_table]] - 所有能获取空气质量数据的城市表
- [[air-quality-hebei|air_quality_hebei]] - 河北省实时空气质量数据
- [[air-quality-hist|air_quality_hist]] - 指定城市和数据频率下并且在指定时间段内的空气质量数据
- [[air-quality-rank|air_quality_rank]] - 获取指定 date 时间点上所有城市(168个)的空气质量数据
- [[air-quality-watch-point|air_quality_watch_point]] - 获取每个城市的所有空气质量监测点的数据
- [[business-value-artist|business_value_artist]] - 艺恩-艺人-艺人商业价值
- [[car-market-cate-cpca|car_market_cate_cpca]] - 乘联会-统计数据-车型大类
- [[car-market-country-cpca|car_market_country_cpca]] - 乘联会-统计数据-国别细分市场
- [[car-market-fuel-cpca|car_market_fuel_cpca]] - 乘联会-统计数据-车型大类
- [[car-market-man-rank-cpca|car_market_man_rank_cpca]] - 乘联会-统计数据-厂商排名
- [[car-market-segment-cpca|car_market_segment_cpca]] - 乘联会-统计数据-级别细分市场
- [[car-market-total-cpca|car_market_total_cpca]] - 乘联会-统计数据-总体市场
- [[car-sale-rank-gasgoo|car_sale_rank_gasgoo]] - 盖世汽车资讯的汽车销量排行榜数据
- [[forbes-rank|forbes_rank]] - 福布斯中国-榜单数据, 一共 87 个指标的数据可以获取
- [[fortune-rank|fortune_rank]] - 指定年份财富世界 500 强公司排行榜
- [[game-hot-rank-taptap|game_hot_rank_taptap]] - 按照榜单类型查询 TapTap 平台游戏排行榜数据
- [[hurun-rank|hurun_rank]] - 胡润百富榜单；富豪榜系列，创业系列，500强系列，特色系列
- [[index-bloomberg-billionaires|index_bloomberg_billionaires]] - 彭博亿万富豪指数, 全球前 500 名; 该接口需要使用代理访问
- [[index-bloomberg-billionaires-hist|index_bloomberg_billionaires_hist]] - 按照年份查询彭博亿万富豪指数; 该接口需要使用代理访问
- [[movie-boxoffice-cinema-daily|movie_boxoffice_cinema_daily]] - 指定日期的每日各影院的票房数据
- [[movie-boxoffice-cinema-weekly|movie_boxoffice_cinema_weekly]] - 指定日期的完整周各影院的票房数据
- [[movie-boxoffice-daily|movie_boxoffice_daily]] - 指定日期的电影票房数据, 每日 10:30, 12:30更新日票房，16:30 同时补充前 7 日票房
- [[movie-boxoffice-monthly|movie_boxoffice_monthly]] - 获取指定日期所在月份的票房数据, 每月5号更新上月票房，并补充之前两个月票房
- [[movie-boxoffice-realtime|movie_boxoffice_realtime]] - 当前时刻的实时电影票房数据, 每 5 分钟更新一次数据, 实时票房包含今天未开映场次已售出的票房
- [[movie-boxoffice-weekly|movie_boxoffice_weekly]] - 指定日期所在完整周的票房数据, 影片周票房数据初始更新周期为每周二，下周二补充数据
- [[movie-boxoffice-yearly|movie_boxoffice_yearly]] - 指定日期所在年度的票房数据
- [[movie-boxoffice-yearly-first-week|movie_boxoffice_yearly_first_week]] - 指定日期所在年度的年度首周票房数据
- [[news-cctv|news_cctv]] - 新闻联播文字稿, 数据区间从 20160330-至今
- [[online-value-artist|online_value_artist]] - 艺恩-艺人-艺人流量价值
- [[stock-js-weibo-report|stock_js_weibo_report]] - 微博舆情报告中近期受关注的股票
- [[sunrise-daily|sunrise_daily]] - 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问
- [[sunrise-monthly|sunrise_monthly]] - 中国各大城市-日出和日落时间, 数据区间从 19990101-至今, 推荐使用代理访问
- [[video-tv|video_tv]] - 艺恩-视频放映-电视剧集
- [[video-variety-show|video_variety_show]] - 艺恩-视频放映-综艺节目
- [[xincaifu-rank|xincaifu_rank]] - 新财富 500 富豪榜, 从 2003 年至今

## 相关

- [[index]]
- [[_meta/topic-map]]
