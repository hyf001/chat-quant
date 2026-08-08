---
title: "index_official - 公共指数列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/index_data.md]
confidence: high
---
# index_official

- 分类: [[qhkc-index-data|指数]]
- 主题路径: 指数 > 公共指数列表
- 描述: 公共指数列表接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/index_data.html

## 相关

- [[qhkc-index-data|指数]]
- [[_meta/topic-map]]

## 源文摘录

## 公共指数列表

### 接口名称

index_official

### 接口描述

公共指数列表接口

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
index_official_df = pro.index_official()
print(index_official_df)
```

### 返回示例

```
                                           id   name
0   index0070c0eb-93ba-2da9-6633-fa70cb90e959   奇货黑链
1   index0d5e051e-b262-bd7a-0fdc-89e2aab21ebb   奇货商品
2   index1ad9d461-7c43-9dea-9e8f-de20878b3ce1   奇货谷物
3   index35cc6f8a-dbca-0614-d48a-1d6258fad6b9  奇货贵金属
4   index6c063119-f98c-586e-64f2-7a42b5cd7d51   奇货饲料
5   index997af7f7-bd77-19cf-6f99-181a6d592f17  奇货软商品
6   indexa5dc7cfd-560e-86bb-50d7-5b4fb4f29ab5   奇货化工
7   indexa9a72e02-d36a-b4c4-58df-0bc75ad4e16b   奇货有色
8   indexd5e4f6e7-373e-334d-07b4-772ba758a9bd   奇货股指
9   indexe369e025-f33d-e787-c13d-0087e90c7d45  奇货铁合金
10  indexfa921e91-b136-605a-29fe-998d25355eaa   奇货油脂
```
