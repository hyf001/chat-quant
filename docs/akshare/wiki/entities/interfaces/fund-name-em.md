---
title: "fund_name_em - 基金基本信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_name_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金基本信息
- 描述: 东方财富网-天天基金网-基金数据-所有基金的基本信息数据
- 目标地址: http://fund.eastmoney.com/fund.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金基本信息

接口: fund_name_em

目标地址: http://fund.eastmoney.com/fund.html

描述: 东方财富网-天天基金网-基金数据-所有基金的基本信息数据

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 基金代码 | object | -   |
| 拼音缩写 | object | -   |
| 基金简称 | object | -   |
| 基金类型 | object | -   |
| 拼音全称 | object | -   |

接口示例

```python
import akshare as ak

fund_name_em_df = ak.fund_name_em()
print(fund_name_em_df)
```

数据示例

```
       基金代码      拼音缩写  ...  基金类型                              拼音全称
0      000001        HXCZHH  ...   混合型                  HUAXIACHENGZHANGHUNHE
1      000002        HXCZHH  ...   混合型                  HUAXIACHENGZHANGHUNHE
2      000003      ZHKZZZQA  ...   债券型           ZHONGHAIKEZHUANZHAIZHAIQUANA
3      000004      ZHKZZZQC  ...   债券型           ZHONGHAIKEZHUANZHAIZHAIQUANC
4      000005    JSZQXYDQZQ  ...  定开债券   JIASHIZENGQIANGXINYONGDINGQIZHAIQUAN
       ...           ...  ...   ...                                    ...
10223  952035     GTJAJDCHH  ...   混合型             GUOTAIJUNANJUNDECHENGHUNHE
10224  952099    GTJAJDXHHC  ...   混合型              GUOTAIJUNANJUNDEXINHUNHEC
10225  959991  XZJQLLXYSHHA  ...   混合型  XINGZHENGJINQILINLINGXIANYOUSHIHUNHEA
10226  959993  XZJQLLXYSHHC  ...   混合型  XINGZHENGJINQILINLINGXIANYOUSHIHUNHEC
10227  980003   TPYLGYGDCYZ  ...   债券型   TAIPINGYANGLIUGEYUEGUNDONGCHIYOUZHAI
```
