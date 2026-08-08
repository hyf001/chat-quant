---
title: "long_pool - 龙虎牛熊多头合约池"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/tools.md]
confidence: high
---
# long_pool

- 分类: [[qhkc-tools|工具]]
- 主题路径: 工具 > 龙虎牛熊多头合约池
- 描述: 龙虎牛熊多头合约池接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/tools.html

## 相关

- [[qhkc-tools|工具]]
- [[_meta/topic-map]]

## 源文摘录

## 龙虎牛熊多头合约池

### 接口名称

long_pool

### 接口描述

龙虎牛熊多头合约池接口

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
long_pool_df = pro.long_pool(date="2018-08-08")
print(long_pool_df)
```

### 返回示例

```
      code symbol
0   rb1810     RB
1   rb1901     RB
2    j1809      J
3    j1901      J
4   ap1810     AP
5   ap1901     AP
6   ap1903     AP
7   ap1905     AP
8   cf1809     CF
9   fg1809     FG
10  ma1809     MA
11  rm1901     RM
12  sf1901     SF
13  sm1901     SM
14  sr1809     SR
15  sr1905     SR
16  ta1808     TA
17  ta1903     TA
18  cu1811     CU
19  cu1905     CU
20  al1808     AL
21  zn1808     ZN
22  ni1809     NI
23  au1812     AU
24   b1901      B
25   c1905      C
26  cs1901     CS
27  jd1809     JD
28  jd1901     JD
29   m1809      M
30  pp1809     PP
31  pp1901     PP
32   v1901      V
```
