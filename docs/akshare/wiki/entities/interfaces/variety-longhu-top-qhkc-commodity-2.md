---
title: "variety_longhu_top - 空头排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_longhu_top

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 龙虎比排行数据 > 空头排行
- 描述: 龙虎比排行数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

### 空头排行

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
variety_longhu_short_top_df = pro.variety_longhu_top(fields="short", date="2018-08-08")
print(variety_longhu_short_top_df)
```

#### 返回示例

```
     code symbol      value
0  oi1905     OI -39.089038
1  ru1905     RU -27.660905
2   y1905      Y -25.509936
3  al1812     AL -24.926301
4   m1905      M -24.878081
5  cu1901     CU -23.127945
6   a1901      A -21.994445
7   y1901      Y -21.953714
8   c1901      C -21.143036
9  rm1905     RM -19.026835
```
