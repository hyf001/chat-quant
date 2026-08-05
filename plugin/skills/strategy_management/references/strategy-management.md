# 策略管理

## 执行入口

所有命令在当前本地项目目录中执行：

```bash
uv run python -m cli.chatq_strategy <command>
```

不要传 API base URL。连接地址由项目配置读取。

## 上下文

不要传 `--user-id` 或 `--project-id`。`list`、`create` 等项目级命令传 `--project-path "<当前项目路径>"`，CLI 会通过该本地路径解析 project，并在需要时把内部 `project_id` 写入 API payload。

Claude Agent SDK 已由后端设置初始 `cwd = project.local_path`，因此 Agent 知道当前业务项目路径。即使命令为了使用 Python 环境需要在仓库根目录执行，也必须把该业务项目路径传给 `--project-path`，不要让 CLI 用仓库根目录推断项目。

## 列出策略

```bash
uv run python -m cli.chatq_strategy list \
  --project-path "<当前项目路径>"
```

## 创建策略

创建策略时使用源码文件，参数 schema 由源码协议解析。

```bash
uv run python -m cli.chatq_strategy create \
  --project-path "<当前项目路径>" \
  --name "策略名称" \
  --description "策略说明" \
  --source-file ./strategy.py \
  --mode single_symbol \
  --risk-note "历史回测不代表未来收益，不构成投资建议"
```

创建后记录返回的 `strategy_id`。

## 查看策略

```bash
uv run python -m cli.chatq_strategy show "$STRATEGY_ID"
```

## 查看版本

```bash
uv run python -m cli.chatq_strategy versions "$STRATEGY_ID"
```

## 编辑策略

编辑策略可以只改元数据，也可以通过 `--source-file` 创建新版本。

```bash
uv run python -m cli.chatq_strategy modify "$STRATEGY_ID" \
  --name "新版策略名称" \
  --description "新版说明" \
  --tag 单只股票 \
  --tag 阶梯交易 \
  --source-file ./strategy_v2.py \
  --risk-note "新版代码风险提示"
```

带 `--source-file` 时会创建新版本，并成为当前版本。记录返回的版本 ID。

## 切换当前版本

```bash
uv run python -m cli.chatq_strategy switch-version "$STRATEGY_ID" "$VERSION_ID"
```

## 归档策略

```bash
uv run python -m cli.chatq_strategy archive "$STRATEGY_ID"
```

## 删除策略

```bash
uv run python -m cli.chatq_strategy delete "$STRATEGY_ID"
```

删除是策略软删除动作。执行前确认用户意图。

## 策略源码协议

当需要创建或修改源码时，读取 [strategy-protocol.md](strategy-protocol.md)。
