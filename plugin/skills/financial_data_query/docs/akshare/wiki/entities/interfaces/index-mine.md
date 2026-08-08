---
title: "index_mine - 个人指数列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/index_data.md]
confidence: high
---
# index_mine

- 分类: [[qhkc-index-data|指数]]
- 主题路径: 指数 > 个人指数列表
- 描述: 个人指数列表接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/index_data.html

## 相关

- [[qhkc-index-data|指数]]
- [[_meta/topic-map]]

## 源文摘录

## 个人指数列表

### 接口名称

index_mine

### 接口描述

个人指数列表接口

### 请求参数

| 参数名 | 说明 | 举例 |
|:----|:---|----|
| -   | -  | -  |

### 返回参数

| 参数名  | 类型     | 说明   |
|:-----|:-------|------|
| id   | string | 指数id |
| name | string | 指数名  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_mine_df = pro.index_mine()
print(index_mine_df)
```

### 返回示例

```
                                           id    name
0   index027927d6-bba5-c432-9bf6-dfcaa75df2a8    油脂头部
1   index03cb6802-24a2-3f9b-813e-936f694fb2b2   新纪元反指
2   index04d11eef-ee50-9fef-e839-a64ad95c44eb     镍尾部
3   index153ca7e5-326d-2505-012f-c2eed754ef29     硬化工
4   index195e23d6-02ae-09e3-169c-f2331bc1d2a8    永兴黑色
5   index2a51db56-0424-75b6-35df-3c62fbcf92c9    螺纹亏损
6   index31e43117-e5e3-bb6f-24d6-8eff003d43dc    螺纹盈利
7   index33b671b8-3ac6-d41b-cb4c-554c44cf990f     软化工
8   index3491c65f-40bf-a739-84e3-5b935634ddcc    永安化工
9   index3cfbcf57-d3b5-cf0c-b4ba-c5db990f86ea    化工头部
10  index43cf357a-db28-c55b-03ac-21e2e4cc5aff    黑色头部
11  index4d44eb91-a7e6-eaf1-ba6e-f7f4e5255adb    油脂尾部
12  index54b33270-465a-c803-923a-f6a9ac7fa15e    东海道通
13  index5d9eb2bf-0aee-551b-58f8-5fac7cdda989     能化工
14  index5f6135ac-2283-4cab-05f0-f33d16444ee0    兴证化工
15  index6a66773f-d6b8-7138-4638-ff1d577252cf    永兴化工
16  index72db2cb8-32ba-50e6-c8b5-5d9e7700fb89  香蕉test
17  index763e0c86-ad90-d9b0-2997-fb298c79bff6   永兴海焦炭
18  index7f763d50-48d2-3a5c-9e30-0152ec31a84a   永兴瑞螺纹
19  index842902a2-4da0-0e8a-e060-3467c041dc20    黑色尾部
20  index91e9a576-ea5e-ffda-d295-35539c74ee60     镍头部
21  index92a6e980-de2b-e4b3-2c0d-0d217b4f870f   贵金属尾部
22  indexa36f1dd5-bc02-56dc-7a28-25ad7a3e4e10  永兴海PTA
23  indexabdbd00f-532a-46af-205f-fa96fa1eb048  兴证海通焦炭
24  indexac99bb42-2850-55ee-b0cd-91214a671288   动力煤盈利
25  indexc421b8f9-731a-a23e-9f3d-2832c3d43fc1    永安黑色
26  indexd10d46e8-ff5d-6199-129f-5e0408626aa5    化工头部
27  indexd4480270-06d1-f50b-5ec1-797afb236890    化工尾部
28  indexe0ef3f87-1e2f-fb76-96ec-3da230dc5d18  ma_top
29  indexef445153-4ed8-485d-a593-5a72fb9fa3e7    混沌黑色
30  indexf42a9e96-6747-5d56-b757-7b0c37a1b350   贵金属头部
```
