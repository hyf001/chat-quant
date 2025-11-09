#!/usr/bin/env python3
"""
报表导出脚本

用法:
    python3 export_reports.py [--agent-type TYPE] [--business-lines BL1,BL2] [--query KEYWORD] [--dry-run] [--verbose]

示例:
    # 导出data_analysis智能体类型的所有报表
    python3 export_reports.py --agent-type data_analysis

    # 仅导出cot业务线的报表
    python3 export_reports.py --agent-type data_analysis --business-lines cot

    # 根据关键字导出报表（如：A股开户入口）
    python3 export_reports.py --agent-type data_analysis --query "A股开户入口"

    # 预览模式（不实际写入文件）
    python3 export_reports.py --agent-type data_analysis --dry-run

    # 详细输出
    python3 export_reports.py --agent-type data_analysis --verbose
"""
import sys
import asyncio
import logging
import argparse
from pathlib import Path

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

sys.path.insert(0, str(find_api_root()))

from app.services.project.cache_manager.config.config_manager import ConfigManager
from app.services.project.cache_manager.exporters.report_exporter import ReportExporter
from app.services.project.cache_manager.config.constants import get_agent_type_config


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='导出MCP报表到本地YAML文件')
    parser.add_argument(
        '--agent-type',
        default='data_analysis',
        help='智能体类型（默认：data_analysis）'
    )
    parser.add_argument(
        '--business-lines',
        help='业务线过滤，多个用逗号分隔（如：cot,iwc）'
    )
    parser.add_argument(
        '--query',
        help='查询关键字（如：A股开户入口）'
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

    args = parser.parse_args()

    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # 验证智能体类型
        agent_type_config = get_agent_type_config(args.agent_type)
        logger.info(f"智能体类型: {args.agent_type} - {agent_type_config['description']}")

        # 解析业务线过滤
        business_lines = None
        if args.business_lines:
            business_lines = [bl.strip() for bl in args.business_lines.split(',')]
            logger.info(f"业务线过滤: {business_lines}")

        # 初始化配置管理器
        config = ConfigManager()

        # 验证配置
        is_valid, error_msg = config.validate_config()
        if not is_valid:
            logger.error(f"配置验证失败: {error_msg}")
            sys.exit(1)

        # 初始化报表导出器
        exporter = ReportExporter(config, args.agent_type)

        # 执行导出
        success = await exporter.export(
            business_lines=business_lines,
            dry_run=args.dry_run,
            verbose=args.verbose,
            query=args.query
        )

        if success:
            logger.info("✅ 导出任务完成")
            sys.exit(0)
        else:
            logger.error("❌ 导出任务失败")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("用户中断导出")
        sys.exit(130)
    except Exception as e:
        logger.error(f"导出过程发生异常: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
