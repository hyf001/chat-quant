---
title: "fund_new_found_ths - 新发基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_new_found_ths

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 新发基金
- 描述: 天天基金网-基金数据-新发基金-新成立基金
- 目标地址: https://fund.eastmoney.com/data/xinfound.html
- 限量: 单次返回所有新发基金数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 新发基金

接口: fund_new_found_em

目标地址: https://fund.eastmoney.com/data/xinfound.html

描述: 天天基金网-基金数据-新发基金-新成立基金

限量: 单次返回所有新发基金数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 基金代码  | object  | -        |
| 基金简称  | object  | -        |
| 发行公司  | object  | -        |
| 基金类型  | object  | -        |
| 集中认购期 | object  | -        |
| 募集份额  | float64 | 注意单位: 亿份 |
| 成立日期  | object  | -        |
| 成立来涨幅 | float64 | 注意单位: %  |
| 基金经理  | object  | -        |
| 申购状态  | object  | -        |
| 优惠费率  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

fund_new_found_em_df = ak.fund_new_found_em()
print(fund_new_found_em_df)
```

数据示例

```
        基金代码                      基金简称    发行公司  ...   基金经理  申购状态  优惠费率
0     019879              万家周期驱动股票发起式A    万家基金  ...     叶勇  开放申购  0.15
1     019873                     长城短债E    长城基金  ...    邹德立   限大额  0.00
2     019872                     长城短债D    长城基金  ...    邹德立   限大额  0.03
3     019880              万家周期驱动股票发起式C    万家基金  ...     叶勇  开放申购  0.00
4     019671  广发中证香港创新药ETF发起式联接(QDII)C    广发基金  ...     刘杰  开放申购  0.00
      ...                       ...     ...  ...    ...   ...   ...
7310  008411                  博时富信纯债债券    博时基金  ...     陈黎   限大额  0.08
7311  008135                  华宸未来价值先锋  华宸未来基金  ...    张翼翔  开放申购  0.15
7312  007729     招商普盛全球配置(QDII-FOF)人民币    招商基金  ...    范刚强  开放申购  0.15
7313  008055            汇添富中债7-10年国开债C   汇添富基金  ...  何旻,李伟  开放申购  0.00
7314  008054            汇添富中债7-10年国开债A   汇添富基金  ...  何旻,李伟  开放申购  0.05
[7315 rows x 11 columns]
```

接口: fund_new_found_ths

目标地址: https://fund.10jqka.com.cn/datacenter/xfjj/

描述: 同花顺-基金数据-新发基金

限量: 单次返回所有新发基金数据

输入参数

| 名称     | 类型  | 描述                                                                                  |
|--------|-----|-------------------------------------------------------------------------------------|
| symbol | str | choice of {"全部", "发行中", "将发行"} "全部": 全部新发基金; "发行中": 发行中的基金; "将发行": 将发行的基金; 默认为 "全部" |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 基金代码  | object  | -        |
| 基金名称  | object  | -        |
| 投资类型  | object  | -        |
| 募集起始日 | object  | -        |
| 募集终止日 | object  | -        |
| 管理人   | object  | -        |
| 基金经理  | object  | -        |
| 认购费率  | float64 | 注意单位: %  |
| 最低认购  | float64 | -        |
| 基金类型  | object  | -        |
| 投资风格  | object  | -        |

接口示例

```python
import akshare as ak

fund_new_found_ths_df = ak.fund_new_found_ths(symbol="全部")
print(fund_new_found_ths_df)
```

数据示例

```
       基金代码       基金名称 投资类型       募集起始日  ... 认购费率 最低认购   基金类型  投资风格
0    020073          财通中证A500指数A  股票型  2026-02-13  ...  0.3  NaN  开放式基金   平衡型
1    020074          财通中证A500指数C  股票型  2026-02-13  ...  0.0  NaN  开放式基金   平衡型
2    022471  兴全安养稳健养老一年持有混合(FOF)  基金型  2026-02-26  ...  0.5  1.0  开放式基金  None
3    023679       格林上证科创板综合指数增强A  股票型  2026-03-04  ...  0.3  1.0  开放式基金   成长型
4    023680       格林上证科创板综合指数增强C  股票型  2026-03-04  ...  0.0  1.0  开放式基金   成长型
..      ...                  ...  ...         ...  ...  ...  ...    ...   ...
218  520790        兴业中证港股通互联网ETF  股票型  2026-03-02  ...  0.3  NaN    ETF   成长型
219  560210           景顺长城农牧渔ETF  股票型  2026-02-24  ...  0.3  NaN    ETF   平衡型
220  560400      华泰柏瑞中证全指证券公司ETF  股票型  2026-02-26  ...  0.3  NaN    ETF   平衡型
221  560410          鹏华中证电池主题ETF  股票型  2026-03-19  ...  0.3  NaN    ETF   平衡型
222  589250       浦银安盛科创板芯片设计ETF  股票型  2026-03-02  ...  0.3  NaN    ETF   平衡型
[223 rows x 11 columns]
```
