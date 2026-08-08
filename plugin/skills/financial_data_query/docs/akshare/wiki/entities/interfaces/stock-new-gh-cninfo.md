---
title: "stock_new_gh_cninfo - 新股过会"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_new_gh_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 新股过会
- 描述: 巨潮资讯-数据中心-新股数据-新股过会
- 目标地址: https://webapi.cninfo.com.cn/#/xinguList
- 限量: 单次获取近一年所有新股过会的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 新股过会

接口: stock_new_gh_cninfo

目标地址: https://webapi.cninfo.com.cn/#/xinguList

描述: 巨潮资讯-数据中心-新股数据-新股过会

限量: 单次获取近一年所有新股过会的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| 公司名称  | object | -   |
| 上会日期  | object | -   |
| 审核类型  | object | -   |
| 审议内容  | object | -   |
| 审核结果  | object | -   |
| 审核公告日 | object | -   |

接口示例

```python
import akshare as ak

stock_new_gh_cninfo_df = ak.stock_new_gh_cninfo()
print(stock_new_gh_cninfo_df)
```

数据示例

```
              公司名称        上会日期  审核类型 审议内容 审核结果       审核公告日
0          兰州银行股份有限公司  2021-09-09  首发新股   首发   通过  2021-09-09
1          永安期货股份有限公司  2021-09-09  首发新股   首发   通过  2021-09-09
2        杭州福莱蒽特股份有限公司  2021-09-09  首发新股   首发   通过  2021-09-09
3    新疆派特罗尔能源服务股份有限公司  2021-09-02  首发新股   首发  未通过  2021-09-02
4      浙江盛泰服装集团股份有限公司  2021-08-26  首发新股   首发   通过  2021-08-26
..                ...         ...   ...  ...  ...         ...
125      河南蓝天燃气股份有限公司  2020-09-17  首发新股   首发   通过  2020-09-17
126      北京声迅电子股份有限公司  2020-09-17  首发新股   首发   通过  2020-09-17
127    天津友发钢管集团股份有限公司  2020-09-17  首发新股   首发   通过  2020-09-17
128     联泓新材料科技股份有限公司  2020-09-17  首发新股   首发   通过  2020-09-17
129      中国国际金融股份有限公司  2020-09-17  首发新股   首发   通过  2020-09-17
```
