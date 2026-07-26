---
title: "variety_niuxiong_top - 多头排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_niuxiong_top

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 牛熊线排行数据 > 多头排行
- 描述: 牛熊线排行数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

### 多头排行

#### 接口名称

variety_niuxiong_top

#### 接口描述

牛熊线排行数据接口

#### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

#### 返回参数

| 参数名    | 类型     | 说明   |
|:-------|:-------|------|
| symbol | string | 品种编码 |
| code   | string | 合约代号 |
| value  | float  | 牛熊线  |

#### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_niuxiong_long_top_df = pro.variety_niuxiong_top(fields="long", date="2018-08-08")
print(variety_niuxiong_long_top_df)
```

#### 返回示例

```
     code symbol  value
0  au1812     AU     45
1  rm1901     RM     30
2  sm1901     SM     28
3   v1901      V     27
4   t1812      T     23
5   j1901      J     23
6  sm1809     SM     23
7  ta1903     TA     23
8  ta1905     TA     21
9  sf1901     SF     20
```
