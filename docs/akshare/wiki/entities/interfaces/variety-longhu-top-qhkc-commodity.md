---
title: "variety_longhu_top - 多头排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_longhu_top

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 龙虎比排行数据 > 多头排行
- 描述: 龙虎比排行数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

### 多头排行

#### 接口名称

variety_longhu_top

#### 接口描述

龙虎比排行数据接口

#### 请求参数

| 参数名  | 说明   | 举例         |
|:-----|:-----|------------|
| date | 查询日期 | 2018-08-08 |

#### 返回参数

| 参数名    | 类型     | 说明     |
|:-------|:-------|--------|
| symbol | string | 品种编码   |
| code   | string | 具体合约代号 |
| value  | float  | 龙虎比    |

#### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_longhu_long_top_df = pro.variety_longhu_top(fields="long", date="2018-08-08")
print(variety_longhu_long_top_df)
```

#### 返回示例

```
     code symbol      value
0  cu1905     CU  56.976958
1  au1812     AU  41.579291
2  sm1901     SM  10.242171
3   v1901      V   9.424667
4  sf1901     SF   9.115990
5   j1901      J   7.243534
6  rb1901     RB   6.526060
7  hc1901     HC   4.098336
8  cu1811     CU   3.650439
9  al1810     AL   3.589835
```
