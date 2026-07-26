---
title: "amac_member_info - 会员机构综合查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_member_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 会员信息 > 会员机构综合查询
- 描述: 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 会员机构综合查询

接口: amac_member_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html

描述: 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称       | 类型     | 描述 |
|----------|--------|----|
| 机构（会员）名称 | object | -  |
| 会员代表     | object | -  |
| 会员类型     | object | -  |
| 会员编号     | object | -  |
| 入会时间     | object | -  |
| 机构类型     | object | -  |
| 是否星标     | object | -  |

接口示例

```python
import akshare as ak

amac_member_info_df = ak.amac_member_info()
print(amac_member_info_df)
```

数据示例

```
          机构（会员）名称 会员代表  会员类型          会员编号        入会时间            机构类型 是否星标
0         天相投资顾问有限公司  林义相  联席会员  LX1800000144  2012-06-06            其他机构    N
1         国泰基金管理有限公司  周向勇  普通会员  PT0100000001  2012-06-06        公募基金管理公司    Y
2       南方基金管理股份有限公司  杨小松  普通会员  PT0100000002  2012-06-06        公募基金管理公司    Y
3         华夏基金管理有限公司  李一梅  普通会员  PT0100000003  2012-06-06        公募基金管理公司    Y
4         华安基金管理有限公司  张霄岭  普通会员  PT0100000004  2012-06-06        公募基金管理公司    Y
              ...  ...   ...           ...         ...             ...  ...
4858  南通乐洵私募基金管理有限公司  胡爱文  观察会员  GC1900033127  2024-03-25     私募证券投资基金管理人    N
4859  上海瀛赐私募基金管理有限公司   黄振  观察会员  GC1900033128  2024-03-25     私募证券投资基金管理人    N
4860  合肥高新资本创业投资有限公司  吴玉麟  观察会员  GC1900033129  2024-03-25  私募股权、创业投资基金管理人    N
4861    上海涌见资产管理有限公司   张阳  观察会员  GC1900033130  2024-03-25     私募证券投资基金管理人    N
4862    深圳布谷资本管理有限公司  林三秀  观察会员  GC1900033131  2024-03-25     私募证券投资基金管理人    N
[4863 rows x 7 columns]
```
