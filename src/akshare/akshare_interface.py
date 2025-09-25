"""
AKShare 接口详情类和加载器
用于解析 ak_share.md 文档并提供接口查询功能
"""

import re
import os
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
import pandas as pd
import jieba

from src.utils import logger

log = logger.get_logger("__name__")


@dataclass
class InterfaceParameter:
    """接口参数"""
    name: str
    type: str
    description: str
    required: bool = True  # 是否必需参数，默认为必需
    default_value: Optional[str] = None  # 默认值（如果有）

    def __post_init__(self):
        """初始化后处理，根据描述自动判断参数性质"""
        if not hasattr(self, '_processed'):
            self._determine_parameter_properties()
            self._processed = True

    def _determine_parameter_properties(self):
        """根据描述确定参数属性"""
        desc_lower = self.description.lower()

        # 判断是否为可选参数的关键词
        optional_keywords = [
            'optional', '可选', '默认', 'default', '不填', '空',
            '留空', '不传', '不指定', '非必需', '非必填'
        ]

        # 判断是否有默认值的模式
        default_patterns = [
            r'默认[：:]\s*(.+?)[\s；;，,。]',
            r'default[：:=]\s*(.+?)[\s；;，,。]',
            r'缺省[：:]\s*(.+?)[\s；;，,。]',
            r'不填.*?默认(.+?)[\s；;，,。]'
        ]

        # 检查是否为可选参数
        for keyword in optional_keywords:
            if keyword in desc_lower:
                self.required = False
                break

        # 检查是否包含等号或默认值语法，如 'date="20200619"'
        if '=' in self.description and '"' in self.description:
            self.required = False
            # 提取默认值
            import re
            match = re.search(r'=\s*["\']([^"\']+)["\']', self.description)
            if match:
                self.default_value = match.group(1)

        # 使用正则表达式查找默认值
        if not self.default_value:
            import re
            for pattern in default_patterns:
                match = re.search(pattern, self.description, re.IGNORECASE)
                if match:
                    self.required = False
                    self.default_value = match.group(1).strip()
                    break

        # 特殊处理：如果参数名是 '-'，则标记为占位符（不是真实参数）
        if self.name == '-':
            self.required = False

    def is_placeholder(self) -> bool:
        """判断是否为占位符参数"""
        return self.name == '-' or not self.name

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required,
            "default_value": self.default_value
        }


@dataclass
class InterfaceDetail:
    """AKShare 接口详情"""
    name: str
    target_url: str
    description: str
    limitation: str
    input_parameters: List[InterfaceParameter]
    output_parameters: List[InterfaceParameter]
    example_code: Optional[str] 
    example_data: Optional[str]
    category: str = ""
    subcategory: str = ""

    def __str__(self):
        return f"Interface: {self.name} - {self.description}"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "target_url": self.target_url,
            "description": self.description,
            "limitation": self.limitation,
            "input_parameters": [p.to_dict() for p in self.input_parameters],
            "output_parameters": [p.to_dict() for p in self.output_parameters],
            "example_code": self.example_code,
            "example_data": self.example_data,
            "category": self.category,
            "subcategory": self.subcategory
        }


class AKShareInterfaceLoader:
    """AKShare 接口文档加载器"""

    def __init__(self, md_file_path: Optional[str] = None):
        if md_file_path is None:
            import os
            current_dir = os.path.dirname(__file__)
            md_file_path = os.path.join(current_dir, 'ak_share.md')

        self.md_file_path = md_file_path
        self.interfaces: Dict[str, InterfaceDetail] = {}
        self._load_interfaces()

    def _load_interfaces(self):
        """加载接口文档"""
        if not os.path.exists(self.md_file_path):
            raise FileNotFoundError(f"AKShare 文档文件不存在: {self.md_file_path}")

        with open(self.md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self._parse_content(content)

    def _parse_content(self, content: str):
        """解析文档内容"""
        # 按接口分割内容
        interface_pattern = r'接口:\s*(\w+)'
        sections = re.split(interface_pattern, content)

        current_category = ""
        current_subcategory = ""

        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                interface_name = sections[i].strip()
                interface_content = sections[i + 1]

                # 从前面的内容中提取类别信息
                prev_content = sections[i - 1] if i > 0 else ""
                category, subcategory = self._extract_category(prev_content)

                if category:
                    current_category = category
                if subcategory:
                    current_subcategory = subcategory

                interface = self._parse_interface(
                    interface_name,
                    interface_content,
                    current_category,
                    current_subcategory
                )

                if interface:
                    self.interfaces[interface_name] = interface

    def _extract_category(self, content: str) -> tuple[str, str]:
        """从内容中提取类别信息"""
        lines = content.split('\n')
        category = ""
        subcategory = ""

        for line in reversed(lines):
            line = line.strip()
            if line.startswith('####'):
                if not subcategory:
                    subcategory = line.replace('#', '').strip()
            elif line.startswith('###'):
                if not category:
                    category = line.replace('#', '').strip()
            elif line.startswith('##'):
                if not category:
                    category = line.replace('#', '').strip()
                break

        return category, subcategory

    def _parse_interface(self, name: str, content: str, category: str, subcategory: str) -> Optional[InterfaceDetail]:
        """解析单个接口"""
        try:
            # 提取目标地址
            target_url = self._extract_field(content, r'目标地址:\s*(.+)')

            # 提取描述
            description = self._extract_field(content, r'描述:\s*(.+)')

            # 提取限量说明
            limitation = self._extract_field(content, r'限量:\s*(.+)')

            # 提取参数表格
            input_params = self._parse_parameters(content, '输入参数')
            output_params = self._parse_parameters(content, '输出参数')

            # 提取示例代码
            example_code = self._extract_code_block(content, 'python')

            # 提取示例数据
            example_data = self._extract_code_block(content, '', after_example=True)

            return InterfaceDetail(
                name=name,
                target_url=target_url,
                description=description,
                limitation=limitation,
                input_parameters=input_params,
                output_parameters=output_params,
                example_code=example_code,
                example_data=example_data,
                category=category,
                subcategory=subcategory
            )

        except Exception as e:
            print(f"解析接口 {name} 时出错: {e}")
            return None

    def _extract_field(self, content: str, pattern: str) -> str:
        """提取单个字段"""
        match = re.search(pattern, content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    def _parse_parameters(self, content: str, section_name: str) -> List[InterfaceParameter]:
        """解析参数表格"""
        parameters = []

        # 查找参数表格
        pattern = rf'{section_name}.*?\n\n(.*?)\n\n'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return parameters

        table_content = match.group(1)
        lines = table_content.strip().split('\n')

        # 跳过表格头部和分隔符
        if len(lines) >= 3:
            for line in lines[2:]:
                if line.strip() and '|' in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 4:  # 至少有名称、类型、描述三列（加上前后空列）
                        name = parts[1]
                        param_type = parts[2]
                        desc = parts[3]

                        # 创建参数对象（包括占位符），让 InterfaceParameter 自动判断属性
                        parameters.append(InterfaceParameter(
                            name=name,
                            type=param_type,
                            description=desc
                        ))

        return parameters

    def _extract_code_block(self, content: str, language: str = '', after_example: bool = False) -> str:
        """提取代码块"""
        if after_example and not language:
            # 提取"数据示例"后的代码块
            pattern = r'数据示例\s*\n\n```[^`]*?\n(.*?)```'
        else:
            # 提取指定语言的代码块
            if language:
                pattern = rf'```{language}\n(.*?)```'
            else:
                pattern = r'```\n(.*?)```'

        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""

    def list_interfaces(self) -> List[str]:
        """列出所有接口名称"""
        return list(self.interfaces.keys())

    def get_interface(self, name: str) -> Optional[InterfaceDetail]:
        """根据接口名称获取接口详情"""
        return self.interfaces.get(name)

    def get_interfaces_by_category(self, category: str) -> List[InterfaceDetail]:
        """根据类别获取接口列表"""
        return [
            interface for interface in self.interfaces.values()
            if category.lower() in interface.category.lower()
        ]

    def search_interfaces(self, keyword: str) -> List[InterfaceDetail]:
        """搜索包含关键词的接口，使用分词提高搜索精度"""
        # 对查询关键词进行分词
        query_tokens = list(jieba.cut(keyword.lower()))
        query_tokens = [x for x in query_tokens if x != ' ' and x != '_' and x != '-']
        log.info(f"分词结果:{query_tokens}")
        results = []
        scored_results = []

        for interface in self.interfaces.values():
            # 创建搜索文本
            search_fields = [
                interface.name.lower(),
                interface.description.lower(),
                interface.category.lower(),
                interface.subcategory.lower()
            ]
            search_fields.extend([
                item.name.lower()+item.description.lower() for item in interface.output_parameters])

            search_text = " ".join(search_fields)

            # 对接口文本进行分词
            text_tokens = list(jieba.cut(search_text))

            # 计算匹配分数
            score = self._calculate_match_score(query_tokens, text_tokens, search_text)

            if score > 0:
                scored_results.append((interface, score))

        # 按分数降序排列
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = [item[0] for item in scored_results]

        return results

    def _calculate_match_score(self, query_tokens: List[str], text_tokens: List[str], search_text: str) -> float:
        """计算匹配分数"""
        score = 0.0

        # 完全匹配原始查询（最高权重）
        original_query = "".join(query_tokens)
        if original_query in search_text:
            score += 10.0

        # 计算词汇匹配
        for query_token in query_tokens:
            if len(query_token.strip()) < 2:  # 跳过单字符和空白
                continue

            # 精确匹配权重更高
            if query_token in text_tokens:
                score += 3.0
            # 部分匹配
            elif any(query_token in text_token for text_token in text_tokens):
                score += 1.0
            # 反向匹配（处理复合词）
            elif any(text_token in query_token for text_token in text_tokens if len(text_token) >= 2):
                score += 0.5

        return score

    def get_interface_count(self) -> int:
        """获取接口总数"""
        return len(self.interfaces)

    def get_categories(self) -> List[str]:
        """获取所有类别"""
        categories = set()
        for interface in self.interfaces.values():
            if interface.category:
                categories.add(interface.category)
        return sorted(list(categories))


class AKShareInvoker:
    """AKShare 接口调用器"""

    def __init__(self, loader: AKShareInterfaceLoader):
        self._loader = loader

    def invoke(self, interface_name: str, **kwargs) -> pd.DataFrame:
        """
        调用 AKShare 接口

        Args:
            interface_name: 接口名称
            **kwargs: 接口参数

        Returns:
            pd.DataFrame: 接口返回的数据

        Raises:
            ValueError: 接口不存在或参数错误
            ImportError: akshare 库未安装
            Exception: 接口调用失败
        """
        # 检查接口是否存在
        interface = self._loader.get_interface(interface_name)
        if not interface:
            raise ValueError(f"接口 '{interface_name}' 不存在")

        try:
            # 动态导入 akshare
            import akshare as ak
        except ImportError:
            raise ImportError("请先安装 akshare 库: pip install akshare")

        # 验证参数
        self._validate_parameters(interface, kwargs)

        try:
            # 动态调用接口
            interface_func = getattr(ak, interface_name)

            # 调用接口并返回结果
            result = interface_func(**kwargs)

            # 确保返回 DataFrame
            if not isinstance(result, pd.DataFrame):
                if hasattr(result, 'to_frame'):
                    result = result.to_frame()
                else:
                    # 尝试转换为 DataFrame
                    result = pd.DataFrame(result)

            return result

        except AttributeError:
            raise ValueError(f"AKShare 中不存在接口 '{interface_name}'")
        except Exception as e:
            raise Exception(f"调用接口 '{interface_name}' 失败: {str(e)}")

    def _validate_parameters(self, interface: InterfaceDetail, params: Dict[str, Any]) -> None:
        """
        验证接口参数

        Args:
            interface: 接口详情
            params: 传入的参数

        Raises:
            ValueError: 参数验证失败
        """
        # 获取所有有效参数（排除占位符）
        valid_params = [p for p in interface.input_parameters if not p.is_placeholder()]

        # 分类必需参数和可选参数
        required_params = [p.name for p in valid_params if p.required]
        optional_params = [p.name for p in valid_params if not p.required]
        all_valid_param_names = required_params + optional_params

        # 检查缺失的必需参数
        missing_params = [p for p in required_params if p not in params]
        if missing_params:
            raise ValueError(f"缺少必需参数: {missing_params}")

        # 检查多余的参数（警告而不是错误）
        if all_valid_param_names:  # 只有当有定义参数时才检查
            extra_params = [p for p in params.keys() if p not in all_valid_param_names]
            if extra_params:
                print(f"警告: 发现未定义的参数 {extra_params}，可能会被忽略")

    def get_required_parameters(self, interface_name: str) -> List[str]:
        """
        获取接口的必需参数列表

        Args:
            interface_name: 接口名称

        Returns:
            List[str]: 必需参数名称列表
        """
        interface = self._loader.get_interface(interface_name)
        if not interface:
            return []

        return [p.name for p in interface.input_parameters if p.required and not p.is_placeholder()]

    def get_optional_parameters(self, interface_name: str) -> List[str]:
        """
        获取接口的可选参数列表

        Args:
            interface_name: 接口名称

        Returns:
            List[str]: 可选参数名称列表
        """
        interface = self._loader.get_interface(interface_name)
        if not interface:
            return []

        return [p.name for p in interface.input_parameters if not p.required and not p.is_placeholder()]

    def get_parameter_info(self, interface_name: str) -> Dict[str, Any]:
        """
        获取接口的参数信息

        Args:
            interface_name: 接口名称

        Returns:
            Dict[str, Any]: 参数信息字典
        """
        interface = self._loader.get_interface(interface_name)
        if not interface:
            return {}

        return {
            "required_parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "default_value": p.default_value
                }
                for p in interface.input_parameters if p.required and not p.is_placeholder()
            ],
            "optional_parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "default_value": p.default_value
                }
                for p in interface.input_parameters if not p.required and not p.is_placeholder()
            ]
        }

    def invoke_with_validation(self, interface_name: str, **kwargs) -> Dict[str, Any]:
        """
        带验证的接口调用，返回详细信息

        Args:
            interface_name: 接口名称
            **kwargs: 接口参数

        Returns:
            Dict[str, Any]: 包含结果和元信息的字典
        """
        interface = self._loader.get_interface(interface_name)
        if not interface:
            return {
                "success": False,
                "error": f"接口 '{interface_name}' 不存在",
                "data": None,
                "interface_info": None
            }

        try:
            # 调用接口
            data = self.invoke(interface_name, **kwargs)

            return {
                "success": True,
                "error": None,
                "data": data,
                "interface_info": {
                    "name": interface.name,
                    "description": interface.description,
                    "category": interface.category,
                    "subcategory": interface.subcategory,
                    "rows": len(data) if isinstance(data, pd.DataFrame) else 0,
                    "columns": list(data.columns) if isinstance(data, pd.DataFrame) else []
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "interface_info": {
                    "name": interface.name,
                    "description": interface.description,
                    "category": interface.category,
                    "subcategory": interface.subcategory
                }
            }

    def batch_invoke(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量调用接口

        Args:
            requests: 请求列表，每个请求包含 interface_name 和参数

        Returns:
            List[Dict[str, Any]]: 结果列表
        """
        results = []

        for i, request in enumerate(requests):
            if 'interface_name' not in request:
                results.append({
                    "success": False,
                    "error": f"请求 {i} 缺少 interface_name",
                    "data": None,
                    "interface_info": None
                })
                continue

            interface_name = request['interface_name']
            params = {k: v for k, v in request.items() if k != 'interface_name'}

            result = self.invoke_with_validation(interface_name, **params)
            results.append(result)

        return results

    # 查询方法的代理 - 这些方法不涉及调用，可以直接代理给 loader
    def list_interfaces(self) -> List[str]:
        """列出所有接口名称"""
        return self._loader.list_interfaces()

    def get_interface(self, name: str) -> Optional[InterfaceDetail]:
        """根据接口名称获取接口详情"""
        return self._loader.get_interface(name)

    def get_interfaces_by_category(self, category: str) -> List[InterfaceDetail]:
        """根据类别获取接口列表"""
        return self._loader.get_interfaces_by_category(category)

    def search_interfaces(self, keyword: str) -> List[InterfaceDetail]:
        """搜索包含关键词的接口"""
        return self._loader.search_interfaces(keyword)

    def get_interface_count(self) -> int:
        """获取接口总数"""
        return self._loader.get_interface_count()

    def get_categories(self) -> List[str]:
        """获取所有类别"""
        return self._loader.get_categories()
    