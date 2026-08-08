# 策略管理

## 执行入口

使用 MCP 工具 `mcp__chatq__strategy`，只传一个 CLI-style `command` 字符串。下面所有代码块都是 `command` 字符串本身，不是 Bash 命令，也不是 JSON：

```text
<subcommand> [--flags]
```

不要用 Bash 或本地 HTTP 请求替代 MCP 工具。工具内部已经绑定当前项目上下文，不要传 `--project-path`、`--project-id`、`--user-id` 或 API base URL。

不确定参数时先调用：

```text
--help
strategy create --help
```

## 列出策略

```text
strategy list
```

## 创建策略

创建策略时使用源码文件，参数 schema 由源码协议解析。`--source-file` 可以传当前项目目录下的相对路径。

```text
strategy create --name "策略名称" --description "策略说明" --source-file ./strategy.py --mode single_symbol --risk-note "历史回测不代表未来收益，不构成投资建议"
```

创建后记录返回的 `strategy_id`。

## 查看策略

```text
strategy show --strategy-id str_xxx
```

## 查看版本

```text
strategy versions --strategy-id str_xxx
```

查看回测记录需要使用这里返回的 `stv_xxx` 策略版本 ID；不要把 `str_xxx` 策略 ID 传给 `backtest list`。

## 编辑策略

编辑策略可以只改元数据，也可以通过 `--source-file` 创建新版本。

```text
strategy modify --strategy-id str_xxx --name "新版策略名称" --description "新版说明" --tag "单只股票" --tag "阶梯交易" --source-file ./strategy_v2.py --risk-note "新版代码风险提示"
```

带 `--source-file` 时会创建新版本，并成为当前版本。记录返回的版本 ID。

## 切换当前版本

```text
strategy switch-version --strategy-id str_xxx --strategy-version-id stv_xxx
```

## 归档策略

```text
strategy archive --strategy-id str_xxx
```

## 删除策略

```text
strategy delete --strategy-id str_xxx
```

删除是策略软删除动作。执行前确认用户意图。

## 策略源码协议

当需要创建或修改源码时，读取 [strategy-protocol.md](strategy-protocol.md)。
