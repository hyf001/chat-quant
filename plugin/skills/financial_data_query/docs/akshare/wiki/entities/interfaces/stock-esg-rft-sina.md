---
title: "stock_esg_rft_sina - 路孚特"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_esg_rft_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > ESG 评级 > 路孚特
- 描述: 新浪财经-ESG评级中心-ESG评级-路孚特
- 目标地址: https://finance.sina.com.cn/esg/grade.shtml
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 路孚特

接口: stock_esg_rft_sina

目标地址: https://finance.sina.com.cn/esg/grade.shtml

描述: 新浪财经-ESG评级中心-ESG评级-路孚特

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述 |
|----------|---------|----|
| 股票代码     | object  | -  |
| ESG评分    | object  | -  |
| ESG评分日期  | object  | -  |
| 环境总评     | float64 | -  |
| 环境总评日期   | float64 | -  |
| 社会责任总评   | float64 | -  |
| 社会责任总评日期 | object  | -  |
| 治理总评     | object  | -  |
| 治理总评日期   | object  | -  |
| 争议总评     | object  | -  |
| 争议总评日期   | object  | -  |
| 行业       | object  | -  |
| 交易所      | object  | -  |

接口示例

```python
import akshare as ak

stock_esg_rft_sina_df = ak.stock_esg_rft_sina()
print(stock_esg_rft_sina_df)
```

数据示例

```
           股票代码     ESG评分     ESG评分日期  ...      争议总评日期          行业   交易所
0          MNTX   10.9(D)  2024-03-23  ...  2023-08-26  卡车-建筑-农用机械  纳斯达克
1     600958.SH  52.3(B-)  2024-03-23  ...  2023-08-26         证券Ⅱ   上交所
2     000799.SZ  27.4(C-)  2024-03-23  ...  2023-08-26         白酒Ⅱ   深交所
3     600745.SH  52.5(B-)  2024-03-23  ...  2023-09-09        消费电子   上交所
4         DISCA   59.9(B)  2024-03-23  ...  2024-03-16     有线-卫星电视  纳斯达克
         ...       ...         ...  ...         ...         ...   ...
5418    BILI.US   35.3(C)  2024-03-23  ...  2024-03-23        ????  纳斯达克
5419    TCOM.US  29.0(C-)  2024-03-23  ...  2023-12-16        ????  纳斯达克
5420     HCM.US  52.4(B-)  2024-03-23  ...  2023-08-26     ???????  纳斯达克
5421    XPEV.US   60.4(B)  2024-03-23  ...  2023-08-26          ??   纽交所
5422      LI.US   35.7(C)  2024-03-23  ...  2023-09-23          ??  纳斯达克
[5423 rows x 13 columns]
```
