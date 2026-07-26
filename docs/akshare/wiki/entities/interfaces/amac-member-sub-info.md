---
title: "amac_member_sub_info - 证券公司私募基金子公司管理人信息公示"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_member_sub_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 私募基金管理人公示 > 证券公司私募基金子公司管理人信息公示
- 描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html?primaryInvestType=private
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 证券公司私募基金子公司管理人信息公示

接口: amac_member_sub_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html?primaryInvestType=private

描述: 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示

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
| 公司类型     | object | -  |

接口示例

```python
import akshare as ak

amac_member_sub_info_df = ak.amac_member_sub_info()
print(amac_member_sub_info_df)
```

数据示例

```
          机构（会员）名称 会员代表  会员类型          会员编号        入会时间            公司类型
0         天相投资顾问有限公司  林义相  联席会员  LX1800000144  2012-06-06            其他机构
1         国泰基金管理有限公司  周向勇  普通会员  PT0100000001  2012-06-06        公募基金管理公司
2       南方基金管理股份有限公司  杨小松  普通会员  PT0100000002  2012-06-06        公募基金管理公司
3         华夏基金管理有限公司  李一梅  普通会员  PT0100000003  2012-06-06        公募基金管理公司
4         华安基金管理有限公司  张霄岭  普通会员  PT0100000004  2012-06-06        公募基金管理公司
              ...  ...   ...           ...         ...             ...
4858  南通乐洵私募基金管理有限公司  胡爱文  观察会员  GC1900033127  2024-03-25     私募证券投资基金管理人
4859  上海瀛赐私募基金管理有限公司   黄振  观察会员  GC1900033128  2024-03-25     私募证券投资基金管理人
4860  合肥高新资本创业投资有限公司  吴玉麟  观察会员  GC1900033129  2024-03-25  私募股权、创业投资基金管理人
4861    上海涌见资产管理有限公司   张阳  观察会员  GC1900033130  2024-03-25     私募证券投资基金管理人
4862    深圳布谷资本管理有限公司  林三秀  观察会员  GC1900033131  2024-03-25     私募证券投资基金管理人
[4863 rows x 6 columns]
```
