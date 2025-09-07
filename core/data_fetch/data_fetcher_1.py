"""
统一数据查询接口
基于schemas/akshare目录下的元数据信息，提供统一的查询接口
"""

import json
import logging
import pandas as pd
import akshare as ak
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


class DataFetcher:
    """统一数据查询接口"""
    
    def __init__(self, schemas_path: Optional[str] = None):
        self.logger = logging.getLogger("unified_query")
        self.schemas_path = schemas_path or Path(__file__).parent / "schema" / "akshare"
        self.api_metadata = {}
        self._load_api_metadata()
        
    def _load_api_metadata(self):
        """加载API元数据"""
        try:
            schemas_dir = Path(self.schemas_path)
            if not schemas_dir.exists():
                self.logger.warning(f"Schema目录不存在: {schemas_dir}")
                return
                
            for schema_file in schemas_dir.glob("*.json"):
                try:
                    with open(schema_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        
                    api_name = metadata.get('name')
                    display_name = metadata.get('display_name', api_name)
                    
                    if api_name:
                        self.api_metadata[api_name] = metadata
                        self.logger.debug(f"加载API元数据: {api_name} ({display_name})")
                        
                except Exception as e:
                    self.logger.error(f"加载元数据文件失败 {schema_file}: {e}")
                    
        except Exception as e:
            self.logger.error(f"加载API元数据失败: {e}")
    
    def list_api(self) -> List[str]:
        """
        获取可用的API列表
        
        Returns:
            Dict[str, str]: {api_name: display_name} 字典
        """
        return [
            f'{name}({metadata.get('display_name')})' for name, metadata in self.api_metadata.items()
        ]
    
    def get_api_info(self, api_name: str) -> Optional[Dict]:
        """
        获取API详细信息
        
        Args:
            api_name: API名称
            
        Returns:
            Dict: API元数据信息
        """
        return self.api_metadata.get(api_name)
    
    def describe_api(self, api_name: str) -> str:
        """
        获取API描述信息
        
        Args:
            api_name: API名称
            
        Returns:
            str: 格式化的API描述信息
        """
        metadata = self.get_api_info(api_name)
        if not metadata:
            return f"API '{api_name}' 不存在"
        
        description = f"API: {api_name}\n"
        description += f"显示名称: {metadata.get('display_name', 'N/A')}\n"
        description += f"描述: {metadata.get('description', 'N/A')}\n"
        description += f"数据源: {metadata.get('datasource', 'N/A')}\n"
        description += f"目录: {metadata.get('dir', 'N/A')}\n\n"
        
        # 输入参数
        input_params = metadata.get('input', [])
        if input_params:
            description += "输入参数:\n"
            for param in input_params:
                required = "必需" if param.get('required', False) else "可选"
                description += f"  - {param['name']} ({param['type']}) [{required}]: {param.get('description', 'N/A')}\n"
            description += "\n"
        
        # 输出字段
        output_fields = metadata.get('output', [])
        if output_fields:
            description += "输出字段:\n"
            for field in output_fields:
                description += f"  - {field['name']} ({field['type']}): {field.get('description', 'N/A')}\n"
        
        return description
    
    def query(self, api_name: str, **kwargs) -> pd.DataFrame:
        """
        统一查询接口
        
        Args:
            api_name: API名称
            **kwargs: 查询参数
            
        Returns:
            pandas.DataFrame: 查询结果
            
        Example:
            # 查询股票历史数据
            result = interface.query(
                'stock_zh_a_hist',
                symbol='000001',
                start_date='20240901',
                end_date='20240910',
                period='daily',
                adjust='qfq'
            )
        """
        metadata = self.get_api_info(api_name)
        if not metadata:
            raise ValueError(f"不支持的API: {api_name}")
        
        try:
            self.logger.info(f"查询API: {api_name}, 参数: {kwargs}")
            
            # 验证和处理参数
            validated_params = self._validate_and_process_params(metadata, kwargs)
            
            # 调用akshare API
            result_df = self._call_akshare_api(api_name, validated_params)
            
            self.logger.info(f"查询完成，返回 {len(result_df)} 行数据")
            return result_df
            
        except Exception as e:
            self.logger.error(f"查询失败: {e}")
            raise
    
    def _validate_and_process_params(self, metadata: Dict, params: Dict[str, Any]) -> Dict[str, Any]:
        """验证和处理查询参数"""
        validated_params = {}
        input_params = metadata.get('input', [])
        
        for param_def in input_params:
            param_name = param_def['name']
            param_type = param_def['type']
            is_required = param_def.get('required', False)
            
            if param_name in params:
                # 参数存在，进行类型转换
                value = params[param_name]
                
                try:
                    if param_type == 'str':
                        validated_params[param_name] = str(value)
                    elif param_type == 'int':
                        validated_params[param_name] = int(value)
                    elif param_type == 'float':
                        validated_params[param_name] = float(value)
                    else:
                        validated_params[param_name] = value
                        
                except ValueError as e:
                    raise ValueError(f"参数 {param_name} 类型转换失败: {e}")
                    
            elif is_required:
                # 必需参数缺失，尝试设置默认值
                default_value = self._get_default_value(param_name, metadata)
                if default_value is not None:
                    validated_params[param_name] = default_value
                else:
                    raise ValueError(f"缺少必需参数: {param_name}")
        
        return validated_params
    
    def _get_default_value(self, param_name: str, metadata: Dict) -> Any:
        """获取参数默认值"""
        api_name = metadata.get('name', '')
        
        # 根据不同API设置默认值
        if api_name == 'stock_zh_a_hist':
            if param_name == 'period':
                return 'daily'
            elif param_name == 'adjust':
                return 'qfq'
            elif param_name == 'start_date':
                return (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            elif param_name == 'end_date':
                return datetime.now().strftime('%Y%m%d')
        
        return None
    
    def _call_akshare_api(self, api_name: str, params: Dict[str, Any]) -> pd.DataFrame:
        """调用akshare API"""
        try:
            # 检查akshare中是否存在该函数
            if not hasattr(ak, api_name):
                raise ValueError(f"akshare中不存在函数: {api_name}")
            
            api_func = getattr(ak, api_name)
            
            # 调用API
            result = api_func(**params)
            
            if isinstance(result, pd.DataFrame):
                return result
            else:
                # 如果返回的不是DataFrame，尝试转换
                return pd.DataFrame(result) if result is not None else pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"调用akshare API失败: {e}")
            raise


data_fetcher = DataFetcher()


