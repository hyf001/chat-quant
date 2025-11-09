#!/usr/bin/env python3
"""
智能体数据导出脚本

根据智能体类型导出所需的数据资源到本地缓存。

支持的智能体类型:
    - data_analysis: 数据分析智能体（数据表 + BI报表）
    - fin_data_analysis: 金融数据分析智能体（金融指标视图表）

数据来源:
    - 数据表/报表/金融视图表: 通过HTTPS API获取（支持开发/生产环境自动切换）

用法:
    python3 export_agent_data.py [--agent-type TYPE] [OPTIONS]

选项:
    --agent-type TYPE           智能体类型 (必需)
    --business-lines BL1,BL2    业务线过滤 (可选)
    --query KEYWORD            查询关键字 (可选)
    --batch-size SIZE          批处理大小 (可选)
    --dry-run                  预览模式，不写入文件
    --verbose                  详细输出

示例:
    # 导出数据分析智能体的所有数据
    python3 export_agent_data.py --agent-type data_analysis

    # 导出金融数据分析智能体的所有数据
    python3 export_agent_data.py --agent-type fin_data_analysis

    # 仅导出指定领域的金融视图表
    python3 export_agent_data.py --agent-type fin_data_analysis --domains stock,fund

    # 仅导出iwc业务线的数据
    python3 export_agent_data.py --agent-type data_analysis --business-lines iwc

    # 预览模式
    python3 export_agent_data.py --agent-type data_analysis --dry-run

    # 详细输出
    python3 export_agent_data.py --agent-type data_analysis --verbose
"""
import sys
import asyncio
import logging
import argparse
from pathlib import Path
from typing import List, Optional

# 动态查找并添加apps/api目录到sys.path
def find_api_root():
    """向上查找apps/api目录"""
    current = Path(__file__).resolve().parent
    while current.parent != current:  # 防止到达根目录
        # 检查是否是api目录（包含app子目录）
        if (current / "app").exists() and (current / "app").is_dir():
            # 验证这是正确的api目录（包含cache_manager）
            if (current / "app" / "services" / "project" / "cache_manager").exists():
                return current
        current = current.parent
    raise RuntimeError("无法找到apps/api目录，请确保脚本在正确的项目结构中运行")

api_root = find_api_root()
sys.path.insert(0, str(api_root))

# 加载 .env 文件（必需：Python 脚本不会自动读取 .env）
# 必须在导入其他模块之前加载，确保 ConfigManager 和 Settings 能读取到环境变量
from dotenv import load_dotenv
project_root = api_root.parent.parent  # 从 apps/api 向上两级到项目根目录
env_file = project_root / ".env"
load_dotenv(env_file)  # 即使文件不存在也不会报错，load_dotenv 会静默处理

from app.services.project.cache_manager.config.config_manager import ConfigManager
from app.services.project.cache_manager.config.constants import get_agent_type_config
from app.services.project.cache_manager.exporters.data_table_exporter import DataTableExporter
from app.services.project.cache_manager.exporters.report_exporter import ReportExporter
from app.services.project.cache_manager.exporters.fin_view_exporter import FinViewExporter


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def export_data_analysis(
    config: ConfigManager,
    agent_type: str,
    business_lines: Optional[List[str]] = None,
    dry_run: bool = False,
    verbose: bool = False,
    query: Optional[str] = None,
    batch_size: int = 10
) -> bool:
    """
    导出数据分析智能体的所有项目初始化数据

    包括：
    - 数据表（PHYSICAL）
    - BI报表（REPORT）

    Args:
        config: 配置管理器
        agent_type: 智能体类型
        business_lines: 业务线过滤
        dry_run: 是否预览模式
        verbose: 是否详细输出
        query: 查询关键字
        batch_size: 批处理大小

    Returns:
        是否全部成功
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("开始导出数据分析智能体项目初始化数据")
    logger.info("=" * 80)

    # 删除旧的 agent_type 目录
    if not dry_run:
        import shutil
        agent_output_dir = config.get_output_dir(agent_type)
        if agent_output_dir.exists():
            logger.info(f"\n🗑️  删除旧的导出目录: {agent_output_dir}")
            try:
                shutil.rmtree(agent_output_dir)
                logger.info("✅ 旧目录删除成功")
            except Exception as e:
                logger.error(f"❌ 删除旧目录失败: {str(e)}")
                return False

    all_success = True

    # 1. 导出数据表（PHYSICAL）
    logger.info("\n📊 [1/2] 导出数据表...")
    logger.info("-" * 80)
    try:
        table_exporter = DataTableExporter(config, agent_type)
        success = await table_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            table_type='PHYSICAL',
            query=query,
            batch_size=batch_size
        )
        if not success:
            logger.error("❌ 数据表导出失败")
            all_success = False
        else:
            logger.info("✅ 数据表导出完成")
    except Exception as e:
        logger.error(f"❌ 数据表导出异常: {str(e)}", exc_info=True)
        all_success = False

    # 2. 导出BI报表（REPORT）
    logger.info("\n📈 [2/2] 导出BI报表...")
    logger.info("-" * 80)
    try:
        report_exporter = ReportExporter(config, agent_type)
        success = await report_exporter.export(
            business_lines=business_lines,
            dry_run=dry_run,
            verbose=verbose,
            query=query
        )
        if not success:
            logger.error("❌ BI报表导出失败")
            all_success = False
        else:
            logger.info("✅ BI报表导出完成")
    except Exception as e:
        logger.error(f"❌ BI报表导出异常: {str(e)}", exc_info=True)
        all_success = False

    return all_success


async def export_fin_data_analysis(
    config: ConfigManager,
    agent_type: str,
    domains: Optional[List[str]] = None,
    dry_run: bool = False,
    verbose: bool = False,
    page_size: int = 100
) -> bool:
    """
    导出金融数据分析智能体的项目初始化数据

    包括：
    - 金融指标视图表

    Args:
        config: 配置管理器
        agent_type: 智能体类型
        domains: Domain过滤（使用简称，如：stock, fund）
        dry_run: 是否预览模式
        verbose: 是否详细输出
        page_size: 每页大小

    Returns:
        是否全部成功
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("开始导出金融数据分析智能体项目初始化数据")
    logger.info("=" * 80)

    # 删除旧的 agent_type 目录
    if not dry_run:
        import shutil
        agent_output_dir = config.get_output_dir(agent_type)
        if agent_output_dir.exists():
            logger.info(f"\n🗑️  删除旧的导出目录: {agent_output_dir}")
            try:
                shutil.rmtree(agent_output_dir)
                logger.info("✅ 旧目录删除成功")
            except Exception as e:
                logger.error(f"❌ 删除旧目录失败: {str(e)}")
                return False

    all_success = True

    # 导出金融指标视图表
    logger.info("\n💰 [1/1] 导出金融指标视图表...")
    logger.info("-" * 80)
    try:
        fin_view_exporter = FinViewExporter(config, agent_type)
        success = await fin_view_exporter.export(
            domains=domains,
            dry_run=dry_run,
            verbose=verbose,
            page_size=page_size
        )
        if not success:
            logger.error("❌ 金融指标视图表导出失败")
            all_success = False
        else:
            logger.info("✅ 金融指标视图表导出完成")
    except Exception as e:
        logger.error(f"❌ 金融指标视图表导出异常: {str(e)}", exc_info=True)
        all_success = False

    return all_success


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='导出指定智能体的所有项目初始化数据到本地YAML文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
智能体类型说明:
  data_analysis      - 数据分析智能体（包含：数据表、BI报表）
  fin_data_analysis  - 金融数据分析智能体（包含：金融指标视图表）

示例:
  # 导出数据分析智能体的项目初始化数据
  %(prog)s --agent-type data_analysis

  # 导出金融数据分析智能体的所有视图表
  %(prog)s --agent-type fin_data_analysis

  # 导出金融数据分析智能体的指定领域视图表
  %(prog)s --agent-type fin_data_analysis --domains stock,fund

  # 预览模式
  %(prog)s --agent-type data_analysis --dry-run
        """
    )
    parser.add_argument(
        '--agent-type',
        required=True,
        choices=['data_analysis', 'fin_data_analysis'],
        help='智能体类型'
    )
    parser.add_argument(
        '--business-lines',
        help='业务线过滤，多个用逗号分隔（如：iwc,cot）。仅适用于data_analysis'
    )
    parser.add_argument(
        '--domains',
        help='Domain过滤，多个用逗号分隔（如：stock,fund,macro）。仅适用于fin_data_analysis'
    )
    parser.add_argument(
        '--query',
        help='查询关键字。仅适用于data_analysis智能体类型'
    )
    parser.add_argument(
        '--page-size',
        type=int,
        help='每页大小。仅适用于fin_data_analysis（默认100）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际写入文件'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='详细输出'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        help='批处理大小（data_analysis默认10，data_develop默认50）'
    )

    args = parser.parse_args()

    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # 验证智能体类型
        agent_type_config = get_agent_type_config(args.agent_type)

        logger.info(f"\n{'=' * 80}")
        logger.info(f"智能体类型: {args.agent_type}")
        logger.info(f"描述: {agent_type_config['description']}")
        logger.info(f"包含数据类型: {', '.join(agent_type_config['data_types'])}")
        logger.info(f"{'=' * 80}\n")

        # 解析业务线过滤
        business_lines = None
        if args.business_lines:
            business_lines = [bl.strip() for bl in args.business_lines.split(',')]
            logger.info(f"业务线过滤: {', '.join(business_lines)}\n")

        # 初始化配置管理器
        config = ConfigManager()

        # 验证配置
        is_valid, error_msg = config.validate_config()
        if not is_valid:
            logger.error(f"配置验证失败: {error_msg}")
            sys.exit(1)

        # 根据智能体类型执行不同的导出逻辑
        success = False

        if args.agent_type == 'data_analysis':
            # 确定批处理大小
            batch_size = args.batch_size if args.batch_size is not None else 10

            # domains参数对data_analysis无效
            if args.domains:
                logger.warning("⚠️  --domains 参数对 data_analysis 智能体类型无效，将被忽略")

            success = await export_data_analysis(
                config=config,
                agent_type=args.agent_type,
                business_lines=business_lines,
                dry_run=args.dry_run,
                verbose=args.verbose,
                query=args.query,
                batch_size=batch_size
            )
        elif args.agent_type == 'fin_data_analysis':
            # business-lines和query参数对fin_data_analysis无效
            if args.business_lines:
                logger.warning("⚠️  --business-lines 参数对 fin_data_analysis 智能体类型无效，将被忽略")
            if args.query:
                logger.warning("⚠️  --query 参数对 fin_data_analysis 智能体类型无效，将被忽略")

            # 解析domains过滤
            domains = None
            if args.domains:
                domains = [d.strip() for d in args.domains.split(',')]
                logger.info(f"Domain过滤: {', '.join(domains)}\n")

            # 确定每页大小
            page_size = args.page_size if args.page_size is not None else 100

            # 验证 FIN_VIEW_BASE_URL 环境变量
            import os
            fin_view_base_url = os.getenv('FIN_VIEW_BASE_URL')
            if not fin_view_base_url:
                logger.error("❌ 环境变量 FIN_VIEW_BASE_URL 未配置，请在.env文件中配置")
                logger.error("示例：FIN_VIEW_BASE_URL=https://indexmap.myhexin.com/bfe")
                sys.exit(1)
            logger.info(f"FIN_VIEW_BASE_URL: {fin_view_base_url}\n")

            success = await export_fin_data_analysis(
                config=config,
                agent_type=args.agent_type,
                domains=domains,
                dry_run=args.dry_run,
                verbose=args.verbose,
                page_size=page_size
            )

        # 输出最终结果
        logger.info("\n" + "=" * 80)
        if success:
            logger.info("✅ 智能体项目初始化数据导出任务全部完成")
            logger.info("=" * 80)
            sys.exit(0)
        else:
            logger.error("❌ 部分导出任务失败，请检查上述错误信息")
            logger.info("=" * 80)
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\n用户中断导出")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n导出过程发生异常: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
