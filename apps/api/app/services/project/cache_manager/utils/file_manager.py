"""
File system operations and YAML file management
"""

import os
import stat
import yaml
import logging
import re
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class QuotedStringDumper(yaml.SafeDumper):
    """自定义YAML Dumper，强制字符串值使用引号"""

    def write_plain(self, text, split=True):
        """重写write_plain方法，但不影响键的输出"""
        # 对于键（keys），使用默认行为
        if self.simple_key_context:
            super().write_plain(text, split)
        else:
            # 对于值（values），使用父类的行为
            super().write_plain(text, split)


def str_representer(dumper, data):
    """字符串表示器 - 强制值使用双引号"""
    if '\n' in data:  # 多行字符串使用literal样式（保留所有换行）
        # 确保字符串末尾有换行符，这样YAML会生成 | 而不是 |-
        if not data.endswith('\n'):
            data = data + '\n'
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


def list_representer(dumper, data):
    """列表表示器 - 强制使用行内格式 []"""
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


# 注册字符串和列表表示器
QuotedStringDumper.add_representer(str, str_representer)
QuotedStringDumper.add_representer(list, list_representer)


def remove_key_quotes(yaml_content: str) -> str:
    """
    移除YAML顶层键上的引号（保留值的引号，不处理多行字符串内容）

    Args:
        yaml_content: 原始YAML内容

    Returns:
        str: 移除键引号后的YAML内容
    """
    lines = yaml_content.split('\n')
    result_lines = []
    in_multiline_string = False

    for line in lines:
        # 检查是否进入/退出多行字符串
        if re.match(r'^\w+:\s*[|>-]', line):
            # 这是多行字符串的开始
            in_multiline_string = True
            # 匹配被引号包裹的键
            match = re.match(r'^"(\w+)":\s*(.*)$', line)
            if match:
                key = match.group(1)
                rest = match.group(2)
                line = f"{key}: {rest}"
        elif in_multiline_string:
            # 检查是否是多行字符串的内容（有缩进）或结束
            if line and not line[0].isspace():
                # 没有缩进，说明多行字符串结束
                in_multiline_string = False
            else:
                # 在多行字符串内，不处理
                result_lines.append(line)
                continue

        # 只处理顶层的键（不在多行字符串内）
        if not in_multiline_string:
            match = re.match(r'^"(\w+)":\s*(.*)$', line)
            if match:
                key = match.group(1)
                rest = match.group(2)
                line = f"{key}: {rest}"

        result_lines.append(line)

    return '\n'.join(result_lines)


def add_yaml_comments(yaml_content: str, field_comments: Dict[str, str]) -> str:
    """
    在YAML内容中添加字段注释

    Args:
        yaml_content: 原始YAML内容
        field_comments: 字段名到注释的映射

    Returns:
        str: 添加注释后的YAML内容
    """
    lines = yaml_content.split('\n')
    result_lines = []

    for line in lines:
        # 匹配字段定义行（格式: field_name: value）
        match = re.match(r'^(\w+):\s*(.*)$', line)
        if match:
            field_name = match.group(1)
            if field_name in field_comments:
                comment = field_comments[field_name]
                # 添加行内注释（包括多行字符串的首行）
                line = f"{line}  # {comment}"

        result_lines.append(line)

    return '\n'.join(result_lines)


class FileManagerError(Exception):
    """文件管理异常"""
    pass


class FileManager:
    """文件管理器"""

    def __init__(self, output_dir: str = "cbas_dw"):
        """
        初始化文件管理器

        Args:
            output_dir: 输出根目录
        """
        self.output_dir = Path(output_dir)
        self.ensure_output_dir()

    def ensure_output_dir(self):
        """确保输出目录存在"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            # 设置目录权限
            os.chmod(self.output_dir, 0o750)
            logger.debug(f"输出目录已准备: {self.output_dir}")
        except Exception as e:
            raise FileManagerError(f"创建输出目录失败: {str(e)}")

    def generate_file_path(self, filename: str, business_line: str, category: str = None) -> Path:
        """
        生成文件路径

        Args:
            filename: 文件名
            business_line: 业务线
            category: 类别 (data_source, transmission_task等)，如果为None或空字符串则不添加category层级

        Returns:
            Path: 完整文件路径
        """
        # 构建目录路径: output_dir/business_line/category/filename
        # 如果category为空，则路径为: output_dir/business_line/filename
        if category:
            file_path = self.output_dir / business_line / category / filename
        else:
            file_path = self.output_dir / business_line / filename
        return file_path

    def save_yaml_file(self, yaml_data: Dict[str, Any], file_path: Path) -> bool:
        """
        保存YAML文件

        Args:
            yaml_data: YAML数据
            file_path: 文件路径

        Returns:
            bool: 是否保存成功
        """
        try:
            # 创建目录结构
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 移除内部文件信息和字段注释
            clean_data = yaml_data.copy()
            field_comments = clean_data.pop("_field_comments", {})
            clean_data.pop("_file_info", None)

            # 生成YAML内容
            from io import StringIO
            stream = StringIO()
            yaml.dump(clean_data, stream,
                     Dumper=QuotedStringDumper,
                     default_flow_style=False,
                     allow_unicode=True,
                     indent=2,
                     sort_keys=False)
            yaml_content = stream.getvalue()

            # 移除键上的引号
            yaml_content = remove_key_quotes(yaml_content)

            # 处理特殊标记，移除标记行但保留内容（用于columns和extra_info的literal block格式）
            lines = yaml_content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 跳过包含标记的行
                if '__LITERAL_BLOCK_START__' in line or '__LITERAL_BLOCK_END__' in line:
                    continue
                cleaned_lines.append(line)
            yaml_content = '\n'.join(cleaned_lines)

            # 添加字段注释
            if field_comments:
                yaml_content = add_yaml_comments(yaml_content, field_comments)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)

            # 设置文件权限
            os.chmod(file_path, 0o640)

            logger.debug(f"YAML文件已保存: {file_path}")
            return True

        except Exception as e:
            logger.error(f"保存YAML文件失败 {file_path}: {str(e)}")
            return False

    def save_report(self, report_data: Dict[str, Any], report_type: str = "export") -> Optional[Path]:
        """
        保存导出报告

        Args:
            report_data: 报告数据
            report_type: 报告类型

        Returns:
            Optional[Path]: 报告文件路径，失败时返回None
        """
        try:
            # 生成报告文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"{report_type}_report_{timestamp}.yaml"

            # 报告保存在output_dir的父目录下的export_reports目录
            # 例如：dw-project-manager/export_reports/
            project_root = self.output_dir.parent
            reports_dir = project_root / "export_reports"
            reports_dir.mkdir(parents=True, exist_ok=True)

            report_path = reports_dir / report_filename

            # 保存报告 - 使用自定义Dumper确保字符串使用引号
            with open(report_path, 'w', encoding='utf-8') as f:
                yaml.dump(report_data, f,
                         Dumper=QuotedStringDumper,
                         default_flow_style=False,
                         allow_unicode=True,
                         indent=2,
                         sort_keys=False)

            # 设置文件权限
            os.chmod(report_path, 0o644)

            logger.info(f"导出报告已保存: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"保存导出报告失败: {str(e)}")
            return None

    def batch_save_files(self, data_list: List[Dict[str, Any]]) -> List[str]:
        """
        批量保存文件

        Args:
            data_list: 数据列表，每个元素包含_file_info

        Returns:
            List[str]: 成功保存的文件路径列表
        """
        saved_files = []

        for data in data_list:
            try:
                file_info = data.get("_file_info")
                if not file_info:
                    logger.warning("数据缺少_file_info，跳过保存")
                    continue

                filename = file_info["filename"]
                business_line = file_info["business_line"]
                category = file_info["category"]

                file_path = self.generate_file_path(filename, business_line, category)

                if self.save_yaml_file(data, file_path):
                    saved_files.append(str(file_path))

            except Exception as e:
                logger.error(f"批量保存文件失败: {str(e)}")
                continue

        logger.info(f"批量保存完成: 成功 {len(saved_files)}, 失败 {len(data_list) - len(saved_files)}")
        return saved_files

    def get_file_stats(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        获取文件统计信息

        Args:
            file_paths: 文件路径列表

        Returns:
            Dict[str, Any]: 统计信息
        """
        stats = {
            "total_files": len(file_paths),
            "total_size_bytes": 0,
            "by_business_line": {},
            "by_category": {}
        }

        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists():
                    file_size = path.stat().st_size
                    stats["total_size_bytes"] += file_size

                    # 按业务线统计
                    parts = path.parts
                    if len(parts) >= 3:  # output_dir/business_line/category/file
                        business_line = parts[-3]
                        category = parts[-2]

                        if business_line not in stats["by_business_line"]:
                            stats["by_business_line"][business_line] = {
                                "files": 0,
                                "size_bytes": 0
                            }
                        stats["by_business_line"][business_line]["files"] += 1
                        stats["by_business_line"][business_line]["size_bytes"] += file_size

                        # 按类别统计
                        if category not in stats["by_category"]:
                            stats["by_category"][category] = {
                                "files": 0,
                                "size_bytes": 0
                            }
                        stats["by_category"][category]["files"] += 1
                        stats["by_category"][category]["size_bytes"] += file_size

            except Exception as e:
                logger.warning(f"获取文件统计失败 {file_path}: {str(e)}")
                continue

        # 转换字节为可读格式
        stats["total_size_readable"] = self._format_file_size(stats["total_size_bytes"])
        for bl_stats in stats["by_business_line"].values():
            bl_stats["size_readable"] = self._format_file_size(bl_stats["size_bytes"])
        for cat_stats in stats["by_category"].values():
            cat_stats["size_readable"] = self._format_file_size(cat_stats["size_bytes"])

        return stats

    def validate_yaml_file(self, file_path: Path) -> bool:
        """
        验证YAML文件格式

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否有效
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            return True
        except Exception as e:
            logger.error(f"YAML文件验证失败 {file_path}: {str(e)}")
            return False

    def cleanup_by_tools(self, tools: List[str]) -> int:
        """
        按工具名称清理文件

        Args:
            tools: 工具名称列表 (如: ['datasource_list', 'transmission_task_list'])

        Returns:
            int: 清理的文件数量
        """
        # 工具名称到类别目录的映射
        tool_category_map = {
            'datasource_list': 'data_source',
            'transmission_task_list': 'transmission_task',
        }

        cleaned_count = 0

        try:
            for tool in tools:
                # 获取对应的类别目录
                category = tool_category_map.get(tool)
                if not category:
                    logger.warning(f"未知工具类型: {tool}，跳过清理")
                    continue

                # 遍历所有业务线目录
                for business_line_dir in self.output_dir.iterdir():
                    if not business_line_dir.is_dir():
                        continue

                    # 构建类别目录路径
                    category_dir = business_line_dir / category
                    if not category_dir.exists():
                        continue

                    # 删除该类别目录下的所有文件
                    for file_path in category_dir.glob('*.yaml'):
                        try:
                            file_path.unlink()
                            cleaned_count += 1
                            logger.debug(f"清理文件: {file_path}")
                        except Exception as e:
                            logger.warning(f"清理文件失败 {file_path}: {str(e)}")
                            continue

                    # 如果类别目录为空，删除该目录
                    try:
                        if not any(category_dir.iterdir()):
                            category_dir.rmdir()
                            logger.debug(f"清理空目录: {category_dir}")
                    except Exception as e:
                        logger.warning(f"清理目录失败 {category_dir}: {str(e)}")

            logger.info(f"清理完成: 删除 {cleaned_count} 个文件")
            return cleaned_count

        except Exception as e:
            logger.error(f"清理操作失败: {str(e)}")
            return 0

    def cleanup_old_files(self, days: int = 30) -> int:
        """
        清理指定天数前的文件（已弃用，项目不支持按时间清理）

        Args:
            days: 天数

        Returns:
            int: 清理的文件数量
        """
        import time

        cutoff_time = time.time() - (days * 24 * 60 * 60)
        cleaned_count = 0

        try:
            for root, dirs, files in os.walk(self.output_dir):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        if file_path.stat().st_mtime < cutoff_time:
                            file_path.unlink()
                            cleaned_count += 1
                            logger.debug(f"清理旧文件: {file_path}")
                    except Exception as e:
                        logger.warning(f"清理文件失败 {file_path}: {str(e)}")
                        continue

            logger.info(f"清理完成: 删除 {cleaned_count} 个文件")
            return cleaned_count

        except Exception as e:
            logger.error(f"清理操作失败: {str(e)}")
            return 0

    def _format_file_size(self, size_bytes: int) -> str:
        """
        格式化文件大小

        Args:
            size_bytes: 字节数

        Returns:
            str: 可读的文件大小
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"

    def list_exported_files(self, business_line: Optional[str] = None,
                           category: Optional[str] = None) -> List[Path]:
        """
        列出导出的文件

        Args:
            business_line: 业务线过滤
            category: 类别过滤

        Returns:
            List[Path]: 文件路径列表
        """
        files = []

        try:
            search_path = self.output_dir
            if business_line:
                search_path = search_path / business_line
                if category:
                    search_path = search_path / category

            if search_path.exists():
                pattern = "**/*.yaml" if not category else "*.yaml"
                files = list(search_path.glob(pattern))

            return sorted(files)

        except Exception as e:
            logger.error(f"列出文件失败: {str(e)}")
            return []

    def get_temp_category_path(self, business_line: str, category: str) -> Path:
        """
        获取临时分类目录路径（用于原子性替换）

        Args:
            business_line: 业务线
            category: 数据类型（如 data_table、bi_report）

        Returns:
            Path: 临时目录路径（category_temp）
        """
        return self.output_dir / business_line / f"{category}_temp"

    def atomic_replace_category_dir(self, business_line: str, category: str = None) -> bool:
        """
        原子性替换分类目录

        将 category_temp 目录原子性地替换 category 目录，确保数据一致性。

        操作流程：
        1. 检查 category_temp 目录是否存在
        2. 如果 category 目录存在，删除它
        3. 将 category_temp 重命名为 category

        Args:
            business_line: 业务线（如 iwc、cbas）
            category: 数据类型（如 data_table、bi_report），如果为None或空则直接替换business_line目录

        Returns:
            bool: 是否替换成功

        示例：
            将 /cache/data_analysis/cot/data_table_temp 原子性替换为
            /cache/data_analysis/cot/data_table
        """
        try:
            # 获取目录路径
            if category:
                temp_dir = self.get_temp_category_path(business_line, category)
                target_dir = self.output_dir / business_line / category
            else:
                # category为空时，直接替换business_line目录
                temp_dir = self.output_dir / business_line / "_temp"
                target_dir = self.output_dir / business_line

            # 检查临时目录是否存在
            if not temp_dir.exists():
                logger.warning(f"临时目录不存在，无法执行替换: {temp_dir}")
                return False

            # 检查临时目录是否为空
            if not any(temp_dir.iterdir()):
                logger.warning(f"临时目录为空，跳过替换: {temp_dir}")
                # 清理空的临时目录
                temp_dir.rmdir()
                return False

            if category:
                # 有category：可以直接重命名整个目录
                # 如果目标目录存在，先删除
                if target_dir.exists():
                    logger.debug(f"删除旧目录: {target_dir}")
                    shutil.rmtree(target_dir)

                # 原子性重命名：temp_dir -> target_dir
                logger.debug(f"原子性重命名: {temp_dir} -> {target_dir}")
                temp_dir.rename(target_dir)
            else:
                # 无category：需要移动_temp目录下的所有文件到父目录
                # 先删除target_dir下除了_temp之外的所有内容
                if target_dir.exists():
                    for item in target_dir.iterdir():
                        if item.name != "_temp":
                            if item.is_dir():
                                shutil.rmtree(item)
                            else:
                                item.unlink()

                # 移动_temp目录下的所有文件到父目录
                logger.debug(f"移动临时目录内容: {temp_dir} -> {target_dir}")
                for item in temp_dir.iterdir():
                    dest = target_dir / item.name
                    item.rename(dest)

                # 删除空的临时目录
                temp_dir.rmdir()
                logger.debug(f"已清理临时目录: {temp_dir}")

            # 根据是否有category显示不同的日志
            display_path = f"{business_line}/{category}" if category else business_line
            logger.info(f"✅ 原子性替换完成: {display_path}")
            return True

        except Exception as e:
            display_path = f"{business_line}/{category}" if category else business_line
            logger.error(f"原子性替换失败 {display_path}: {str(e)}")
            # 尝试清理临时目录
            try:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                    logger.info(f"已清理临时目录: {temp_dir}")
            except Exception as cleanup_error:
                logger.error(f"清理临时目录失败: {cleanup_error}")
            return False

    def generate_file_path_in_temp(self, filename: str, business_line: str, category: str = None) -> Path:
        """
        在临时目录中生成文件路径（用于原子性替换）

        Args:
            filename: 文件名
            business_line: 业务线
            category: 类别，如果为None或空字符串则不添加category层级

        Returns:
            Path: 临时目录中的完整文件路径
        """
        if category:
            temp_dir = self.get_temp_category_path(business_line, category)
        else:
            # category为空时，临时目录直接在business_line下
            temp_dir = self.output_dir / business_line / "_temp"
        return temp_dir / filename