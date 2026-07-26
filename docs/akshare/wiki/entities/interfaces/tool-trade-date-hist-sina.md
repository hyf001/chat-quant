---
title: "tool_trade_date_hist_sina - 交易日历"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, tool, parameters, returns, example]
sources: [raw/data-dictionary/tool/tool.md]
confidence: high
---
# tool_trade_date_hist_sina

- 分类: [[tool-tool|AKShare 工具箱]]
- 主题路径: AKShare 工具箱 > 交易日历
- 描述: 新浪财经-股票交易日历数据
- 目标地址: https://finance.sina.com.cn
- 限量: 单次返回从 1990-12-19 到 2024-12-31 之间的股票交易日历数据, 这里补充 1992-05-04 进入交易日
- 来源页面: https://akshare.akfamily.xyz/data/tool/tool.html

## 相关

- [[tool-tool|AKShare 工具箱]]
- [[_meta/topic-map]]

## 源文摘录

### 交易日历

接口: tool_trade_date_hist_sina

目标地址: https://finance.sina.com.cn

描述: 新浪财经-股票交易日历数据

限量: 单次返回从 1990-12-19 到 2024-12-31 之间的股票交易日历数据, 这里补充 1992-05-04 进入交易日

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型     | 描述                                                        |
|------------|--------|-----------------------------------------------------------|
| trade_date | object | 从 1990-12-19 至 2024-12-31 的股票交易日数据; 这里补充 1992-05-04 进入交易日 |

接口示例

```python
import akshare as ak

tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
print(tool_trade_date_hist_sina_df)
```

数据示例

```
      trade_date
0     1990-12-19
1     1990-12-20
2     1990-12-21
3     1990-12-24
4     1990-12-25
...          ...
8550  2025-12-25
8551  2025-12-26
8552  2025-12-29
8553  2025-12-30
8554  2025-12-31
[8555 rows x 1 columns]
```
