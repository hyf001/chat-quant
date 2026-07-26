---
title: "variety_niuxiong_top - 空头排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_niuxiong_top

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 牛熊线排行数据 > 空头排行
- 描述: 牛熊线排行数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

### 空头排行

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
variety_niuxiong_short_top_df = pro.variety_niuxiong_top(fields="short", date="2018-08-08")
print(variety_niuxiong_short_top_df)
```

#### 返回示例

```
     code symbol  value
0   a1901      A    -40
1  cu1810     CU    -37
2  zn1810     ZN    -32
3  ru1901     RU    -26
4  ru1905     RU    -23
5   y1905      Y    -22
6  al1811     AL    -21
7   l1901      L    -20
8  hc1810     HC    -16
9   y1901      Y    -14
```
