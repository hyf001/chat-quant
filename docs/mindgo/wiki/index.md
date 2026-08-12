# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-08-11 | Total pages: 22

## Entities

- [[supermind-mindgo]] - SuperMind / MindGo 在本仓库中被视为一个复合数据源：它既有在线策略与研究环境里的 mindgo-api-docs，也有可浏览的数据平台字段字典 mindgo-data-dictionary，还可以通过 mindgo-jupyter-python-execution 在授权远程 Jupyter kernel 中执行 Python 取数脚本。

## Concepts

- [[mindgo-fundamental-table-api]] - 财务和表数据主要通过 get_fundamentals(query_object, date=None, statDate=None, latest=False) 查询。API 文档说明函数签名、参数和返回值；字段、表名和样例应对照 mindgo-stock-data-dictionary 中的上市公司财务数据。
- [[mindgo-strategy-framework-api]] - 策略框架 API 定义回测/模拟交易代码的生命周期、回调函数、交易函数、context 对象和重要枚举。它是 mindgo-api-docs 的基础层，行情和财务 API 通常在这些回调中被调用。
- [[mindgo-stock-data-dictionary]] - 股票类数据是数据平台最大部分，覆盖 A 股基本信息、交易日历、行情、快照、资金、财务报表、公司资料、行业、概念、分析师一致预期和另类数据。函数层参考 mindgo-market-data-api、mindgo-security-reference-api 和 mindgo-fundamental-table-api。
- [[mindgo-funds-bonds-index-forex-dictionary]] - 本页汇总基金、可转债、指数、外汇的数据平台条目。行情字段通常对应 mindgo-market-data-api；基本信息与成分股相关函数见 mindgo-security-reference-api。
- [[mindgo-futures-options-data-dictionary]] - 本页汇总期货、期权与 T+D 合约的数据平台条目。行情函数优先看 mindgo-market-data-api，证券/合约信息看 mindgo-security-reference-api。
- [[mindgo-data-dictionary]] - 数据平台字典来自 https://quant.10jqka.com.cn/view/dataplatform 及 101 个 detail/{id} 详情页。每个详情页通常包含：字段说明、使用代码、参数说明、使用样例、数据样例。原始解析结果见 raw/articles/mindgo-dataplatform-detail-docs.json.md。
- [[mindgo-data-source-overview]] - MindGo 数据源由三层材料组成：
- [[mindgo-utility-file-api]] - 工具函数位于 help/4 的“工具函数”部分，覆盖代码格式转换、文件读写、路径查询、复制/删除、消息推送、自选板块和文件加密。
- [[mindgo-iwencai-api]] - 问财接口把自然语言选股接入 MindGo，但 query_iwencai 和 get_iwencai 的服务侧重点不同。
- [[mindgo-market-data-api]] - 行情资金接口集中在 API 文档“行情资金数据接口”，并和数据平台中的日频/分钟/快照字段表互相对应。
- [[mindgo-factor-risk-alt-dictionary]] - 本页汇总风险模型、因子数据、i问财接口和 iFinD 数据接口。因子函数可结合 mindgo-security-reference-api 的 get_sfactor_data；问财使用方式见 mindgo-iwencai-api。
- [[mindgo-security-reference-api]] - 证券信息接口回答“有哪些标的、属于什么分类、在哪些交易日、属于什么行业/概念”。它和 mindgo-data-dictionary 中的基本信息、行业、概念、指数成分股、因子数据表对应。
- [[mindgo-intraday-realtime-bars]] - A 股 1 分钟分时取数可以抽象为一段远程 Jupyter Python 脚本：在 MindGo kernel 中执行 get_price(STOCK_LIST, START_TIME, END_TIME, "1m", FIELDS, True, None, 0, is_panel=1)，再把返回的 Panel/dict/DataFrame 结构转成 JSON rows。
- [[mindgo-api-docs]] - help/4 的 API 文档覆盖策略框架、行情资金、证券信息、表数据、问财、组合优化和工具函数。本次解析得到 171 个标题和 288 个代码块。
- [[mindgo-indexmap-arsenal-api]] - 获取indexmap指标数据方法.py 展示了另一条数据入口：在 MindGo 环境中调用 get_arsenal_api('cbas-babel-frondend-pod')，再 POST 到 /babel/api/query_index。
- [[mindgo-security-model]] - MindGo 数据源的主要动态风险来自远程 Jupyter Python 执行，而不是只读文档本身。mindgo-jupyter-python-execution 中的代码以远程 Jupyter 用户身份运行，理论上可读远程文件、访问环境变量、发网络请求，甚至在账号暴露交易 API 时执行交易相关操作。
- [[mindgo-jupyter-python-execution]] - 这页只保留从 portable Jupyter 案例中抽象出的取数方法：在授权的远程 MindGo / SuperMind Jupyter kernel 中执行 Python 代码，用 MindGo 内置函数获取数据，再把结果标准化输出。

## Comparisons

- [[mindgo-access-methods-comparison]] - | 方式 | 主要用途 | 优点 | 局限 | 首选页面 |

## Queries

- [[mindgo-data-source-quickstart]] - 当用户问“MindGo 怎么取某类数据”时，按下面顺序决策：

## Meta Summaries

- [[api-function-outline]] - 本页是 mindgo-api-docs 的标题索引，帮助快速定位 API 区域。
- [[source-inventory]] - | Source | Wiki raw file | Notes |

