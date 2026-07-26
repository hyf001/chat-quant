---
title: "short_pool - 龙虎牛熊空头合约池"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/tools.md]
confidence: high
---
# short_pool

- 分类: [[qhkc-tools|工具]]
- 主题路径: 工具 > 龙虎牛熊空头合约池
- 描述: 龙虎牛熊空头合约池
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/tools.html

## 相关

- [[qhkc-tools|工具]]
- [[_meta/topic-map]]

## 源文摘录

## 龙虎牛熊空头合约池

### 接口名称

short_pool

### 接口描述

龙虎牛熊空头合约池

### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名    | 类型     | 说明   |
|:-------|:-------|------|
| symbol | string | 品种编码 |
| code   | string | 合约代号 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
short_pool_df = pro.short_pool(date="2018-08-08")
print(short_pool_df)
```

### 返回示例

```
      code symbol
0    i1901      I
1   hc1810     HC
2   ap1811     AP
3   cf1901     CF
4   oi1809     OI
5   oi1905     OI
6   rm1905     RM
7   sf1809     SF
8   ta1811     TA
9   zc1809     ZC
10  zc1811     ZC
11  zc1901     ZC
12  cu1809     CU
13  cu1810     CU
14  cu1901     CU
15  al1811     AL
16  al1812     AL
17  zn1810     ZN
18  pb1810     PB
19  sn1809     SN
20  ag1812     AG
21  fu1901     FU
22  ru1809     RU
23  ru1811     RU
24  ru1901     RU
25  ru1905     RU
26   a1901      A
27   c1811      C
28  cs1809     CS
29   l1809      L
30   l1901      L
31   m1811      M
32   m1901      M
33   p1809      P
34   p1905      P
35   v1809      V
36   y1809      Y
37   y1901      Y
38   y1905      Y
39  if1808     IF
40  if1809     IF
41  ih1808     IH
```
