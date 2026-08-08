---
title: "money_in_out - 每日商品保证金沉淀变化"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/fund.md]
confidence: high
---
# money_in_out

- 分类: [[qhkc-fund|资金]]
- 主题路径: 资金 > 每日商品保证金沉淀变化
- 描述: 每日商品保证金沉淀变化接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/fund.html

## 相关

- [[qhkc-fund|资金]]
- [[_meta/topic-map]]

## 源文摘录

## 每日商品保证金沉淀变化

### 接口名称

money_in_out

### 接口描述

每日商品保证金沉淀变化接口

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明           |
|:-------|:-------|--------------|
| symbol | string | 品种编码         |
| chge   | float  | 品种沉淀资金变化，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
money_in_out_df = pro.money_in_out(date="2018-08-08")
print(money_in_out_df)
```

### 返回示例

```
           chge symbol
0  -275632312.0      J
1  -243543981.6     ZC
2   -81290136.0      I
3   -45598051.2     JM
4   -31547670.0      P
5   -30567752.5      L
6   -30113737.6     BU
7   -28320467.0     PP
8   -26664664.0     SR
9   -22570900.0     CF
10  -19633982.0     FU
11  -10199960.0     PB
12   -6788380.0     FG
13   -6080775.4     JD
14   -2069555.6     SN
15   -1979271.0     RU
16    -695370.0     CY
17     -87414.0     RI
18     -18258.0     JR
19          0.0     SC
20          0.0     PM
21          0.0     WR
22          0.0     FB
23          0.0     BB
24          0.0     RS
25    2467941.0     AL
26    3289568.0     WH
27    5503300.0     LR
28    8602684.0     OI
29    9535390.0     CS
30   15957968.0     ZN
31   19975040.4     SF
32   21202165.0     AU
33   25174906.8     RM
34   26598818.0      B
35   31817098.0      Y
36   33848526.6     MA
37   34038302.2     SM
38   43679158.6     AP
39   52613008.0      A
40   58577657.6     HC
41   81632070.0     AG
42  105799545.0      V
43  110605243.0      C
44  184962996.0     RB
45  192803778.0      M
46  204487969.0     CU
47  220199220.0     TA
48  293341736.0     NI
```
