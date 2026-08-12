---
title: MindGo Jupyter 执行安全模型
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "security", "jupyter"]
sources: ["raw/articles/jupyter-python-execution-pattern.md"]
confidence: high
---

# MindGo Jupyter 执行安全模型

MindGo 数据源的主要动态风险来自远程 Jupyter Python 执行，而不是只读文档本身。[[mindgo-jupyter-python-execution]] 中的代码以远程 Jupyter 用户身份运行，理论上可读远程文件、访问环境变量、发网络请求，甚至在账号暴露交易 API 时执行交易相关操作。

## 规则

- 不要把 Jupyter token、Authorization header、真实 Jupyter URL/token 写入 prompt、日志、截图或配置样例。
- 让用户自己在本地安全位置配置密钥；不要让 Agent 搜索浏览器、shell history 或其他项目里的凭据。
- 远程代码应优先只读取数，并把结果标准化输出。
- 删除/覆盖远程文件、交易相关代码、长时间运行任务都需要明确确认。
- 数据平台和 API 文档属于低风险静态来源；远程 Jupyter 执行属于高风险动态来源。

低风险取数字段查询看 [[mindgo-data-dictionary]]；需要执行的取数看 [[mindgo-jupyter-python-execution]]。
