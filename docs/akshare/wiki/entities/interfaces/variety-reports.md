---
title: "variety_reports - 商品相关研报数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/commodity.md]
confidence: high
---
# variety_reports

- 分类: [[qhkc-commodity|商品]]
- 主题路径: 商品 > 商品相关研报数据
- 描述: 商品相关研报数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/commodity.html

## 相关

- [[qhkc-commodity|商品]]
- [[_meta/topic-map]]

## 源文摘录

## 商品相关研报数据

### 接口名称

variety_reports

### 接口描述

商品相关研报数据接口

### 请求参数

| 参数名        | 说明   | 举例         |
|:-----------|:-----|------------|
| csymbolode | 品种编码 | RB         |
| date       | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名   | 类型       | 说明    |
|:------|:---------|-------|
| title | string   | 研报标题  |
| pub   | string   | 研报发布人 |
| time  | datetime | 发布时间  |
| url   | string   | 研报地址  |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_reports_df = pro.variety_reports(csymbolode="RB", date="2018-08-08")
print(variety_reports_df)
```

### 返回示例

```
    pub  ...                                                url
0  中信期货  ...  https://report.qhkch.com/47/黑色建材日报/reportd471f...
1  格林大华  ...  https://report.qhkch.com/274/工业品/reportd836d83...
2  格林大华  ...  https://report.qhkch.com/274/深度报告/reportd003e4...
3  华泰期货  ...  https://report.qhkch.com/127/金属/report11f7a4db...
4  华泰期货  ...  https://report.qhkch.com/127/黑色建材/reportdd6bdd...
5  银河期货  ...  https://report.qhkch.com/416/黑色链/reportb05ee81...
6  兴证期货  ...  https://report.qhkch.com/101/工业品日报/report26db3...
```
