---
title: "index_info - 指数信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/index_data.md]
confidence: high
---
# index_info

- 分类: [[qhkc-index-data|指数]]
- 主题路径: 指数 > 指数信息
- 描述: 指数信息接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/index_data.html

## 相关

- [[qhkc-index-data|指数]]
- [[_meta/topic-map]]

## 源文摘录

## 指数信息

### 接口名称

index_info

### 接口描述

指数信息接口

### 请求参数

| 参数名      | 说明   | 举例                                        |
|:---------|:-----|-------------------------------------------|
| index_id | 指数id | index0070c0eb-93ba-2da9-6633-fa70cb90e959 |

### 返回参数

| 参数名           | 类型       | 说明                                   |
|:--------------|:---------|--------------------------------------|
| name          | string   | 指数名称                                 |
| all_brokers   | int      | 是否包含所有席位，0:否，1:是                     |
| created_time  | datetime | 创建时间                                 |
| all_varieties | int      | 是否包含所有品种，0:否，1:所有商品，2:所有股指，3:所有商品和股指 |
| status        | int      | 是否开放，0:不开放，1:开放                      |
| nickname      | string   | 创建人昵称                                |
| varieties     | array    | 包含品种的编码， all_varieties为0时返回          |
| brokers       | array    | 包含席位， all_brokers为0时返回               |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_info_df = pro.index_info(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959")
print(index_info_df)
```

### 返回示例

```
   name  all_brokers  ... nickname  varieties
0  奇货黑链            1  ...     奇货可查         RB
1  奇货黑链            1  ...     奇货可查          I
2  奇货黑链            1  ...     奇货可查         JM
3  奇货黑链            1  ...     奇货可查          J
4  奇货黑链            1  ...     奇货可查         HC
5  奇货黑链            1  ...     奇货可查         SF
6  奇货黑链            1  ...     奇货可查         SM
```
