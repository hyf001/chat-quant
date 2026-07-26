---
title: "index_weights - 指数权重数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/index_data.md]
confidence: high
---
# index_weights

- 分类: [[qhkc-index-data|指数]]
- 主题路径: 指数 > 指数权重数据
- 描述: 指数权重数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/index_data.html

## 相关

- [[qhkc-index-data|指数]]
- [[_meta/topic-map]]

## 源文摘录

## 指数权重数据

### 接口名称

index_weights

### 接口描述

指数权重数据接口

### 请求参数

| 参数名      | 说明   | 举例                                        |
|:---------|:-----|-------------------------------------------|
| index_id | 指数id | index0070c0eb-93ba-2da9-6633-fa70cb90e959 |
| date     | 查询日期 | 2018-08-08                                |

### 返回参数

| 参数名     | 类型     | 说明      |
|:--------|:-------|---------|
| variety | string | 品种编码    |
| weight  | float  | 权重值，百分数 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_weights_df = pro.index_weights(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_weights_df)
```

### 返回示例

```
  variety     weight
0      RB  37.714204
1       I  18.168484
2      JM   5.879807
3       J  26.265556
4      HC   7.369110
5      SF   2.431867
6      SM   2.170973
```
