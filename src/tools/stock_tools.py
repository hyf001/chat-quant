import json
from datetime import date, datetime
import os
from langchain_core.tools import tool
import akshare as ak
from typing import Dict, Any, List
from langchain_core.messages import ToolMessage
import os.path
from src.akshare import get_akshare_invoker
from src.akshare.akshare_interface import AKShareInvoker


work_dir = "/Users/huyufei/Documents/hyf/code/github/chat-quant/workspace/"

class ToolCall():

    def __init__(self,tools: list):
        self.tools_by_name:dict = { tool.name:tool for tool in tools}

    def _json_serializer(self, obj):
        """自定义JSON序列化器，处理日期对象"""
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    def __call__(self, inputs: dict,config: dict):
            message = inputs.get("messages",[])
            message = message[-1]
            outputs=[]
            tool_result = {}
            for tool_call in message.tool_calls:
                tool_result = self.tools_by_name[tool_call['name']].invoke(tool_call['args'])
                outputs.append(
                    ToolMessage(content=json.dumps(tool_result, default=self._json_serializer, ensure_ascii=False),
                                name=tool_call['name'],
                                tool_call_id=tool_call['id'])
                )
            return {"messages":outputs}






@tool
def stock_zh_a_spot_em() -> Dict[str, Any]:
     """
     东方财富网-沪深京 A股-实时行情数据。
     限量: 单次返回所有沪深京 A 股上市公司的实时行情数据
     调用这个工具后,系统会自动生成一个数据文件。
     返回: 数据文件相关信息
     """
     try:
         df = ak.stock_zh_a_spot_em()
         now = datetime.now().strftime("%Y%m%d%H%M%S")
         file_path = os.path.join(work_dir,f"stock_zh_a_spot_em-{now}.csv") 
         df.to_csv(file_path)
         return {
             "file_path": file_path,
             "status": "ok",
             "count": len(df)
         }
     except Exception as e:
         return {
             "data": None,
             "status": "error",
             "error": str(e)
         }

@tool
def stock_individual_info_em(symbol: str) -> Dict[str, Any]:
    """获取个股实时行情数据
    Args:
        symbol: 股票代码，如 '000001'
    调用这个工具后,系统会自动生成一个数据文件。
    返回: 数据文件相关信息
    """
    try:
        df = ak.stock_individual_info_em(symbol=symbol)
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = file_path = os.path.join(work_dir,f"stock_zh_a_spot_em-{symbol}-{now}.csv") 
        df.to_csv(file_path)
        return {
            "file_path": file_path,
            "status": "ok",
            "symbol": symbol
        }
    except Exception as e:
        return {
            "data": None,
            "status": "error",
            "error": str(e),
            "symbol": symbol
        }

@tool
def stock_zh_a_hist(symbol: str,start_date:str, end_date: str, period: str = "daily") -> Dict[str, Any]:
    """获取股票历史行情数据

    Args:
        symbol: 股票代码，如 '000001'
        start_date: 开始日期，格式 '%Y%m%d'
        end_date: 结束日期，格式 '%Y%m%d'
        period: 周期，可选 'daily', 'weekly', 'monthly'
        
    调用这个工具后,系统会自动生成一个数据文件。
    返回: 数据文件相关信息
    """
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust="")
        file_path = os.path.join(work_dir,f"stock_zh_a_spot_em-{symbol}-{start_date}-{end_date}.csv") 
        df.to_csv(file_path)
        return {
            "file_path": file_path,
            "status": "ok",
            "symbol": symbol,
            "period": period
        }
    except Exception as e:
        return {
            "data": None,
            "status": "error",
            "error": str(e),
            "symbol": symbol
        }


@tool
def search_akshare_interfaces(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    根据自然语言描述搜索相关的 AKShare 接口

    Args:
        query: 自然语言查询，如 "股票实时行情"、"上市公司信息" 等
        limit: 返回结果的最大数量，默认为10

    Returns:
        包含匹配的接口详情列表
    """
    try:
        invoker = get_akshare_invoker()

        # 搜索相关接口
        interfaces = invoker.search_interfaces(query)

        # 限制返回数量
        if limit > 0:
            interfaces = interfaces[:limit]

        # 构建返回结果
        results = []
        for interface in interfaces:
            # 获取参数信息
            param_info = invoker.get_parameter_info(interface.name)

            interface_detail = {
                "name": interface.name,
                "description": interface.description,
                "category": interface.category,
                "subcategory": interface.subcategory,
                "target_url": interface.target_url,
                "limitation": interface.limitation,
                "required_parameters": param_info.get("required_parameters", []),
                "optional_parameters": param_info.get("optional_parameters", []),
                "example_code": interface.example_code
            }
            results.append(interface_detail)

        return {
            "status": "success",
            "query": query,
            "total_found": len(invoker.search_interfaces(query)),
            "returned_count": len(results),
            "interfaces": results
        }

    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e),
            "interfaces": []
        }


@tool
def invoke_akshare_interface(interface_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    调用指定的 AKShare 接口获取数据

    Args:
        interface_name: AKShare 接口名称，如 'stock_zh_a_spot_em'
        parameters: 接口参数字典，如 {"symbol": "000001", "period": "daily"}

    Returns:
        包含调用结果和数据文件信息
    """
    try:
        invoker = get_akshare_invoker()

        # 验证接口是否存在
        interface = invoker.get_interface(interface_name)
        if not interface:
            return {
                "status": "error",
                "interface_name": interface_name,
                "error": f"接口 '{interface_name}' 不存在",
                "suggestions": _get_similar_interfaces(invoker, interface_name)
            }

        # 处理参数
        if parameters is None:
            parameters = {}

        # 获取参数信息用于验证
        param_info = invoker.get_parameter_info(interface_name)

        # 调用接口
        result = invoker.invoke_with_validation(interface_name, **parameters)

        if result["success"]:
            # 保存数据到文件
            data = result["data"]
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{interface_name}_{now}.csv"
            file_path = os.path.join(work_dir, file_name)

            # 确保工作目录存在
            os.makedirs(work_dir, exist_ok=True)

            # 保存数据
            data.to_csv(file_path, index=False, encoding='utf-8-sig')

            return {
                "status": "success",
                "interface_name": interface_name,
                "interface_description": interface.description,
                "parameters_used": parameters,
                "data_shape": list(data.shape),
                "columns": list(data.columns),
                "file_path": file_path,
                "file_size_mb": round(os.path.getsize(file_path) / 1024 / 1024, 2),
                "sample_data": data.head().to_dict('records') if len(data) > 0 else []
            }
        else:
            return {
                "status": "error",
                "interface_name": interface_name,
                "parameters_used": parameters,
                "error": result["error"],
                "parameter_info": param_info
            }

    except Exception as e:
        return {
            "status": "error",
            "interface_name": interface_name,
            "parameters_used": parameters,
            "error": str(e)
        }


def _get_similar_interfaces(invoker, interface_name: str) -> List[str]:
    """获取相似的接口名称建议"""
    try:
        # 简单的相似度匹配，基于名称包含关系
        all_interfaces = invoker.list_interfaces()
        suggestions = []

        # 提取查询词的关键字
        query_parts = interface_name.lower().split('_')

        for name in all_interfaces:
            name_lower = name.lower()
            # 如果接口名包含查询词的任何部分，加入建议
            if any(part in name_lower for part in query_parts if len(part) > 2):
                suggestions.append(name)
                if len(suggestions) >= 5:  # 最多返回5个建议
                    break

        return suggestions
    except:
        return []


