---
title: "crypto_bitcoin_hold_report - 比特币持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, crypto, parameters, returns, example]
sources: [raw/data-dictionary/dc/dc.md]
confidence: high
---
# crypto_bitcoin_hold_report

- 分类: [[dc-dc|AKShare 加密货币数据]]
- 主题路径: AKShare 加密货币数据 > 持仓报告 > 比特币持仓报告
- 描述: 比特币持仓报告
- 目标地址: https://datacenter.jin10.com/dc_report?name=bitcoint
- 限量: 单次返回当前时点的比特币持仓报告数据
- 来源页面: https://akshare.akfamily.xyz/data/dc/dc.html

## 相关

- [[dc-dc|AKShare 加密货币数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 比特币持仓报告

接口: crypto_bitcoin_hold_report

目标地址: https://datacenter.jin10.com/dc_report?name=bitcoint

描述: 比特币持仓报告

限量: 单次返回当前时点的比特币持仓报告数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 代码       | object  | 日期时间-索引 |
| 公司名称-英文  | object  | -       |
| 公司名称-中文  | object  | -       |
| 国家/地区    | object  | -       |
| 市值       | float64 | -       |
| 比特币占市值比重 | float64 | 注意单位: % |
| 持仓成本     | float64 | -       |
| 持仓占比     | float64 | 注意单位: % |
| 持仓量      | float64 | -       |
| 当日持仓市值   | float64 | -       |
| 查询日期     | object  | -       |
| 公告链接     | object  | -       |
| 分类       | object  | -       |
| 倍数       | float64 | -       |

接口示例

```python
import akshare as ak

crypto_bitcoin_hold_report_df = ak.crypto_bitcoin_hold_report()
print(crypto_bitcoin_hold_report_df)
```

数据示例

```
               代码                               公司名称-英文  ...    分类  倍数
0       MSTR:NADQ                         MicroStrategy  ...  上市公司 NaN
1       MARA:NADQ         Marathon Digital Holdings Inc  ...  上市公司 NaN
2       TSLA:NADQ                            Tesla, Inc  ...  上市公司 NaN
3      HUT:NASDAQ                     Hut 8 Mining Corp  ...  上市公司 NaN
4       COIN:NADQ                 Coinbase Global, Inc.  ...  上市公司 NaN
5   BRPHF:OTCMKTS               Galaxy Digital Holdings  ...  上市公司 NaN
6         SQ:NYSE                           Block, Inc.  ...  上市公司 NaN
7       RIOT:NADQ                  Riot Platforms, Inc.  ...  上市公司 NaN
8    BTGGF:TCMKTS                      Bitcoin Group SE  ...  上市公司 NaN
9        VOYG:TSX                   Voyager Digital LTD  ...  上市公司 NaN
10    HIVE:NASDAQ                       Hive Blockchain  ...  上市公司 NaN
11  NEXOF:OTCMKTS                         NEXON Co. Ltd  ...  上市公司 NaN
12   EXOD:OTCMKTS                   Exodus Movement Inc  ...  上市公司 NaN
13        HKD:HKG                                 Meitu  ...  上市公司 NaN
14    PHUN:NASDAQ                        Phunware, Inc.  ...  上市公司 NaN
15       NFT:AQSE                   NFT Investments PLC  ...  上市公司 NaN
16    BITF:NASDAQ                      Bitfarms Limited  ...  上市公司 NaN
17    CLSK:NASDAQ                        CleanSpark Inc  ...  上市公司 NaN
18  DMGGF:OTCMKTS         DMG Blockchain Solutions Inc.  ...  上市公司 NaN
19    BTBT:NASDAQ                     Bit Digital, Inc.  ...  上市公司 NaN
20    CIFR:NASDAQ                         Cipher Mining  ...  上市公司 NaN
21  NPPTF:OTCMKTS                Neptune Digital Assets  ...  上市公司 NaN
22        ABT:DUS      Advanced Bitcoin Technologies AG  ...  上市公司 NaN
23      LQWDF:OTC                     LQwD FinTech Corp  ...  上市公司 NaN
24  BBKCF:OTCMKTS              BIGG Digital Assets Inc.  ...  上市公司 NaN
25  BNXAF:OTCMKTS                    Banxa Holdings Inc  ...  上市公司 NaN
26  HSSHF:OTCMKTS              Digihost Technology Inc.  ...  上市公司 NaN
27   BTCS:OTCMKTS                             BTCS Inc.  ...  上市公司 NaN
28      SATO:TSXV  Canada Computational Unlimited Corp.  ...  上市公司 NaN
29   FRMO:OTCMKTS                            FRMO Corp.  ...  上市公司 NaN
30  ARBKF:OTCMKTS                   Argo Blockchain PLC  ...  上市公司 NaN
31    MILE:NASDAQ                             Metromile  ...  上市公司 NaN
32    MOGO:Nasdaq                        MOGO Financing  ...  上市公司 NaN
33           None                                   USA  ...  政府机构 NaN
34           None                        Ukraine (govt)  ...  政府机构 NaN
35           None                               Mt. Gox  ...  私营企业 NaN
36           None                             Block.one  ...  私营企业 NaN
37           None                   Tether Holdings LTD  ...  私营企业 NaN
38           None                  The Tezos Foundation  ...  私营企业 NaN
39           None            Stone Ridge Holdings Group  ...  私营企业 NaN
40           None                  Massachusetts Mutual  ...  私营企业 NaN
41           None                       Lisk Foundation  ...  私营企业 NaN
42           None                             Seetee AS  ...  私营企业 NaN
43   GBTC:OTCMKTS               Grayscale Bitcoin Trust  ...   ETF NaN
44      XBTE:NADQ             CoinShares / XBT Provider  ...   ETF NaN
45       BTCC:TSX                   Purpose Bitcoin ETF  ...   ETF NaN
46       BTCQ:TSX            3iQ CoinShares Bitcoin ETF  ...   ETF NaN
47     BTCE:XETRA                 ETC Group Bitcoin ETP  ...   ETF NaN
48     QBTCBV:TSX                  3iQ The Bitcoin Fund  ...   ETF NaN
49   BITW:OTCMKTS          Bitwise 10 Crypto Index Fund  ...   ETF NaN
50  OTCQX:OTCMKTS      Grayscale Digital Large Cap Fund  ...   ETF NaN
51       ABTC:SWX                           21Shares AG  ...   ETF NaN
52     VBTC:XETRA            VanEck Vectors Bitcoin ETN  ...   ETF NaN
53       BTCX:TSX                CI Galaxy Bitcoin Fund  ...   ETF NaN
54       OBTC:OTC                  Osprey Bitcoin Trust  ...   ETF NaN
55   BTC0E.AS:OTC               Valour Bitcoin Zero ETP  ...   ETF NaN
56       EBIT:TSX                    Evolve Bitcoin ETF  ...   ETF NaN
57       BITC:TSX               Ninepoint Bitcoin Trust  ...   ETF NaN
58       FTBC:TSE        Fidelity Advantage Bitcoin ETF  ...   ETF NaN
[59 rows x 14 columns]
```
