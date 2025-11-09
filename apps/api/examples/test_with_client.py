"""
使用 ClaudeSDKClient 测试 SQL 校验和建表工具
按照官方样例格式编写
建表工具现在已整合到 sql_tools_server 中
"""
import asyncio
import sys
import os
from pathlib import Path

# 设置 git-bash 路径
os.environ["CLAUDE_CODE_GIT_BASH_PATH"] = r"D:\soft\Git\bin\bash.exe"

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 确保使用开发环境
os.environ["THS_TIER"] = "dev"

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from app.services.tools.sql_validator import sql_validator_server
from app.services.tools.sql_executor import sql_tools_server


async def test_sql_validator():
    """测试 SQL 校验工具"""
    print("\n" + "=" * 80)
    print("测试 1: SQL 校验工具 (validate_sql)")
    print("=" * 80)

    # 配置客户端 - 使用字典格式注册 MCP 服务器
    options = ClaudeAgentOptions(
        mcp_servers={"sql-validator": sql_validator_server},
        allowed_tools=[
            "mcp__sql-validator__validate_sql",  # MCP 工具名称格式
        ],
        model="claude-sonnet-4-5-20250929",
        permission_mode="bypassPermissions"
    )

    print("\n测试场景: 验证一个简单的 SQL 查询")
    print("-" * 80)

    try:
        async with ClaudeSDKClient(options=options) as client:
            # 发送请求
            await client.query("请使用 validate_sql 工具验证这个 SQL: SELECT user_id, COUNT(*) as cnt FROM orders WHERE status = 'completed' GROUP BY user_id，引擎使用 hive")

            # 接收响应
            print("\nClaude 的响应:")
            print("-" * 80)

            async for msg in client.receive_response():
                print(msg)

        print("\n[OK] SQL 校验工具测试成功!")
        return True

    except Exception as e:
        print(f"\n[FAIL] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_table_creator():
    """测试建表工具 (现在在 sql_tools_server 中)"""
    print("\n\n" + "=" * 80)
    print("测试 2: 建表工具 (create_table) - 从 sql_tools_server")
    print("=" * 80)

    # 配置客户端 - 使用 sql_tools_server
    options = ClaudeAgentOptions(
        mcp_servers={"sql-tools": sql_tools_server},
        allowed_tools=[
            "mcp__sql-tools__create_table",  # MCP 工具名称格式
        ],
        model="claude-sonnet-4-5-20250929",
        permission_mode="bypassPermissions"
    )

    print("\n测试场景: 测试参数验证 - 使用不支持的数据源类型")
    print("-" * 80)

    try:
        async with ClaudeSDKClient(options=options) as client:
            # 发送请求
            await client.query("请使用 create_table 工具，参数为: catalog_type='mysql', sql='CREATE TABLE test (id INT)'")

            # 接收响应
            print("\nClaude 的响应:")
            print("-" * 80)

            async for msg in client.receive_response():
                print(msg)

        print("\n[OK] 建表工具测试成功!")
        return True

    except Exception as e:
        print(f"\n[FAIL] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_both_tools():
    """测试同时使用 SQL 校验和建表工具"""
    print("\n\n" + "=" * 80)
    print("测试 3: 同时使用 SQL 校验和建表工具")
    print("=" * 80)

    # 配置客户端 - 注册两个 MCP 服务器
    options = ClaudeAgentOptions(
        mcp_servers={
            "sql-validator": sql_validator_server,
            "sql-tools": sql_tools_server
        },
        allowed_tools=[
            "mcp__sql-validator__validate_sql",
            "mcp__sql-tools__create_table",
        ],
        model="claude-sonnet-4-5-20250929",
        permission_mode="bypassPermissions"
    )

    print("\n测试场景: 先验证 SQL,然后说明如何使用建表工具")
    print("-" * 80)

    try:
        async with ClaudeSDKClient(options=options) as client:
            # 发送请求
            await client.query("""
我需要完成两个任务:
1. 首先使用 validate_sql 工具验证这个 SQL 的语法: CREATE TABLE db_test.users (id INT, name STRING)，引擎使用 hive
2. 如果验证通过，请告诉我可以使用 create_table 工具来创建表（但不要实际调用）
""")

            # 接收响应
            print("\nClaude 的响应:")
            print("-" * 80)

            async for msg in client.receive_response():
                print(msg)

        print("\n[OK] 组合工具测试成功!")
        return True

    except Exception as e:
        print(f"\n[FAIL] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """运行所有测试"""
    print("=" * 80)
    print("Claude SDK 工具测试 - 建表工具已整合到 sql_tools_server")
    print("=" * 80)
    print(f"\nGit Bash 路径: {os.environ.get('CLAUDE_CODE_GIT_BASH_PATH')}")
    print(f"环境: {os.environ.get('THS_TIER')}")

    print("\n说明:")
    print("- sql_validator_server: 包含 validate_sql 工具")
    print("- sql_tools_server: 包含 download_sql_result, preview_sql_result, count_sql_result, create_table 工具")

    results = []

    try:
        # 测试 1: SQL 校验工具
        result1 = await test_sql_validator()
        results.append(("SQL 校验工具", result1))

        # 测试 2: 建表工具
        result2 = await test_table_creator()
        results.append(("建表工具", result2))

        # 测试 3: 组合使用
        result3 = await test_both_tools()
        results.append(("组合工具", result3))

        # 输出总结
        print("\n\n" + "=" * 80)
        print("测试总结")
        print("=" * 80)

        for name, success in results:
            status = "[OK] 通过" if success else "[FAIL] 失败"
            print(f"{name}: {status}")

        all_passed = all(r[1] for r in results)
        if all_passed:
            print("\n[SUCCESS] 所有测试通过!")
            sys.exit(0)
        else:
            print("\n[WARN] 部分测试失败")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n[INFO] 用户中断测试")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n[ERROR] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
