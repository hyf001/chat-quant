# SQL 工具测试说明

本目录包含了 SQL 校验工具和建表工具的测试脚本。

## 工具说明

### 1. SQL 校验工具 (validate_sql)
- **文件**: `app/services/tools/sql_validator.py`
- **功能**: 验证 SQL 语句的语法正确性
- **参数**:
  - `sql`: SQL 语句 (必需)
  - `engine`: 数据库引擎，支持 presto, hive, starrocks (可选，默认 hive)

### 2. 建表工具 (create_table)
- **文件**: `app/services/tools/sql_executor.py` (已整合到 sql_tools_server)
- **功能**: 通过 EasyFetch API 创建 Hive 或 StarRocks 表
- **参数**:
  - `catalog_type`: 数据源类型，hive 或 starrocks (必需)
  - `sql`: 建表 SQL 语句 (必需)

## 测试脚本

### ✅ 推荐: 直接调用测试 (test_sdk_simple.py)

这是最简单、最快速的测试方式,直接调用工具的 `handler` 方法。

**运行方式**:
```bash
cd /d/learn_project/Claudable/apps/api
.venv/Scripts/python.exe examples/test_sdk_simple.py
```

**特点**:
- ✅ 运行速度快
- ✅ 不需要额外配置
- ✅ 适合单元测试和 CI 环境
- ✅ 测试结果清晰

**测试内容**:
- 工具元数据验证 (名称、描述、Schema)
- SQL 语法验证 (有效/无效 SQL)
- 参数验证 (空值、不支持的类型等)

### ⚠️ ClaudeSDKClient 测试 (test_with_client.py)

使用完整的 ClaudeSDKClient 进行集成测试。

**限制**:
- 需要设置 `CLAUDE_CODE_GIT_BASH_PATH` 环境变量
- 需要完整的 Claude Code CLI 环境
- 在 Windows 下需要 git-bash
- ClaudeSDKClient 不直接支持传入 SDK MCP Server 实例
- 需要通过配置文件或环境设置注册 MCP 服务器

**说明**:
由于 ClaudeSDKClient 的架构限制,它主要用于完整的 Claude Code 会话环境,
不适合作为单元测试工具。建议使用直接调用方式进行测试。

## 测试结果

### SQL 校验工具测试结果

```
工具名称: validate_sql
工具描述: 验证SQL语句的语法正确性
输入 Schema: {'sql': <class 'str'>, 'engine': <class 'str'>}

✅ 有效 SQL (Hive/Presto/StarRocks): 通过
✅ 复杂 JOIN 查询: 通过
✅ 语法错误检测: 正确检测并提供详细错误信息
✅ 参数验证 (空 SQL/不支持引擎): 通过
```

### 建表工具测试结果

```
工具名称: create_table
工具描述: 创建Hive或StarRocks表
输入 Schema: {'catalog_type': <class 'str'>, 'sql': <class 'str'>}

✅ 参数验证 - 空 catalog_type: 正确拒绝
✅ 参数验证 - 不支持的类型: 正确拒绝
✅ 参数验证 - 空 SQL: 正确拒绝
✅ 参数验证 - 非 CREATE 语句: 正确拒绝
```

## 在实际项目中使用

### 方式1: 直接调用 (推荐用于编程调用)

```python
from app.services.tools.sql_validator import validate_sql_tool
from app.services.tools.sql_executor import create_table_tool

# SQL 校验
result = await validate_sql_tool.handler({
    "sql": "SELECT * FROM users WHERE id = 1",
    "engine": "hive"
})
print(result["content"][0]["text"])

# 建表 (已整合到 sql_executor.py)
result = await create_table_tool.handler({
    "catalog_type": "hive",
    "sql": "CREATE TABLE ..."
})
print(result["content"][0]["text"])
```

### 方式2: 在 Claude Code 中使用

这两个工具已经通过 MCP Server 注册,可以在 Claude Code 会话中自动使用:

1. 在项目的 Claude Code 会话中,Claude 可以自动调用这些工具
2. 工具已在 `app/services/tools/__init__.py` 中导出
3. MCP 服务器:
   - `sql_validator_server` - 包含 validate_sql 工具
   - `sql_tools_server` - 包含 download_sql_result, preview_sql_result, count_sql_result, create_table 工具

## 环境配置

### 开发环境
```bash
export THS_TIER=dev
# BI域名会自动配置为: https://phonestat.hexin.cn/sdmp/easyfetch
```

### 生产环境
```bash
export THS_TIER=prod
# 会使用容器内部地址
```

## 工具特性

1. ✅ 使用 `@tool` 装饰器创建
2. ✅ 返回统一的 MCP 格式
3. ✅ 清晰的状态标签 (`[OK]`, `[FAIL]`, `[INFO]`, `[TIP]`, `[DEBUG]`)
4. ✅ 无 emoji 符号
5. ✅ 完整的错误处理和提示
6. ✅ 详细的错误信息和修复建议

## 故障排除

### 问题: ClaudeSDKClient 超时
**原因**: ClaudeSDKClient 需要完整的 CLI 环境,不适合简单的单元测试  
**解决**: 使用直接调用测试方式 (test_sdk_simple.py)

### 问题: 编码错误 (UnicodeEncodeError)
**原因**: Windows 控制台编码问题  
**解决**: 测试脚本已避免使用 emoji 和特殊字符

### 问题: MCP 配置文件未找到
**原因**: ClaudeSDKClient 无法直接接受 SDK MCP Server 实例  
**解决**: 使用直接调用方式,或在完整的 Claude Code 环境中使用
