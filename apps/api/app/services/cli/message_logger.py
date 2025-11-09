"""
Message Logger for Claude Agent Analysis
用于捕获和导出 Claude Agent SDK 的消息到 JSON 文件
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class MessageLogger:
    """记录和导出 Claude Agent SDK 消息"""

    def __init__(self, output_dir: str = "logs/messages"):
        # 如果是相对路径，转换为基于项目根目录的绝对路径
        if not os.path.isabs(output_dir):
            # 获取当前文件所在目录（adapters/）
            current_file_dir = Path(__file__).parent
            # 向上找到 api 目录（apps/api/）
            api_root = current_file_dir.parent.parent.parent
            # 构建完整路径
            self.output_dir = api_root / output_dir
        else:
            self.output_dir = Path(output_dir)

        # 确保目录存在
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # 如果失败，fallback 到临时目录
            import tempfile
            self.output_dir = Path(tempfile.gettempdir()) / "claude_messages"
            self.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Warning: Could not create {output_dir}, using {self.output_dir} instead. Error: {e}")

        self.messages: List[Dict[str, Any]] = []
        self.current_session_id: Optional[str] = None
        self.tool_use_map: Dict[str, Dict[str, Any]] = {}  # 映射 tool_id -> tool_call 信息
        self.user_instructions: List[Dict[str, str]] = []  # 存储用户指令
        self.session_start_time: Optional[str] = None  # 会话开始时间
        self.model_name: Optional[str] = None  # 使用的模型名称

    def log_message(self, message_obj: Any, message_type: str, extra_info: Optional[Dict] = None):
        """
        记录单个消息

        Args:
            message_obj: Claude SDK 消息对象
            message_type: 消息类型 (SystemMessage, AssistantMessage, UserMessage, ResultMessage)
            extra_info: 额外的信息字典
        """
        timestamp = datetime.utcnow().isoformat()

        # 基础消息信息（不包含 session_id，避免冗余）
        log_entry = {
            "timestamp": timestamp,
            "type": message_type,
        }

        # 提取消息对象的所有属性
        if hasattr(message_obj, '__dict__'):
            for key, value in message_obj.__dict__.items():
                if key.startswith('_') or key == 'session_id':  # 跳过内部属性和 session_id
                    continue

                # 提取 model 信息但不加入 log_entry
                if key == "model":
                    if not self.model_name and isinstance(value, str):
                        self.model_name = value
                    continue  # 跳过，不添加到消息中

                # 特殊处理复杂类型
                if isinstance(value, (str, int, float, bool, type(None))):
                    log_entry[key] = value
                elif isinstance(value, list):
                    # 处理 content blocks
                    if key == "content":
                        processed = self._process_content_blocks(value)
                        # 只添加非空字段
                        if processed.get("text"):
                            log_entry["text"] = processed["text"]
                        if processed.get("tools"):
                            log_entry["tools"] = processed["tools"]
                    else:
                        log_entry[key] = json.dumps(value, default=str)
                else:
                    log_entry[key] = str(value)

        # 提取 SystemMessage 中的真实 session_id
        if message_type == "SystemMessage":
            # 首先尝试从属性获取
            if hasattr(message_obj, 'session_id'):
                real_session_id = getattr(message_obj, 'session_id', None)
                if real_session_id and not self.current_session_id:
                    self.current_session_id = real_session_id

            # 如果属性中没有，尝试从 data 字符串中解析
            if not self.current_session_id and 'data' in log_entry:
                try:
                    import ast
                    data_str = log_entry['data']
                    if isinstance(data_str, str) and 'session_id' in data_str:
                        # 尝试解析为字典
                        data_dict = ast.literal_eval(data_str)
                        if isinstance(data_dict, dict) and 'session_id' in data_dict:
                            self.current_session_id = data_dict['session_id']
                except Exception:
                    pass  # 解析失败，忽略

        # 添加额外信息
        if extra_info:
            log_entry.update(extra_info)

        self.messages.append(log_entry)

    def _format_tool_data(self, data: Any) -> Any:
        """格式化工具数据，保持完整性用于评估"""
        # 保持所有数据完整，不做截断
        # 对于评估和分析，完整的数据更重要
        return data

    def _process_content_blocks(self, content_blocks: List[Any]) -> Dict[str, Any]:
        """处理 content blocks，提取文本和工具信息"""
        from claude_agent_sdk.types import TextBlock, ToolUseBlock, ToolResultBlock

        text_parts = []
        tool_uses = []
        tool_results = []

        for block in content_blocks:
            if isinstance(block, TextBlock):
                text_parts.append(block.text)

            elif isinstance(block, ToolUseBlock):
                tool_data = {
                    "name": block.name,
                    "id": block.id,
                }
                # 只在有 input 时添加
                if hasattr(block, 'input') and block.input:
                    tool_data["input"] = self._format_tool_data(block.input)
                tool_uses.append(tool_data)

            elif isinstance(block, ToolResultBlock):
                tool_id = getattr(block, 'tool_use_id', getattr(block, 'id', 'unknown'))
                content = getattr(block, 'content', None)
                is_error = getattr(block, 'is_error', False)

                tool_data = {
                    "tool_id": tool_id,
                }
                # 只在有错误时添加 is_error
                if is_error:
                    tool_data["is_error"] = is_error
                # 只在有输出时添加 output
                if content:
                    tool_data["output"] = self._format_tool_data(content)

                tool_results.append(tool_data)

        result = {}
        if text_parts:
            result["text"] = "\n".join(text_parts)
        if tool_uses:
            result["tools"] = tool_uses
        if tool_results:
            result["tools"] = tool_results  # UserMessage 用 tools 存储结果

        return result

    def set_session_id(self, session_id: str):
        """设置当前会话 ID"""
        if not self.current_session_id:
            self.current_session_id = session_id
            self.session_start_time = datetime.utcnow().isoformat()  # 使用 UTC 时间

    def log_user_instruction(self, instruction: str, images: Optional[List] = None):
        """记录用户指令（作为一条消息）"""
        user_msg = {
            "timestamp": datetime.utcnow().isoformat(),  # 使用 UTC 时间保持一致
            "type": "UserInstruction",
            "instruction": instruction,
        }

        # 只在有图片时添加 image_count
        if images and len(images) > 0:
            user_msg["image_count"] = len(images)

        self.messages.append(user_msg)

        # 同时保存到 user_instructions 用于快速访问
        self.user_instructions.append({
            "timestamp": user_msg["timestamp"],
            "instruction": instruction,
            "image_count": len(images) if images else 0
        })

    def export_to_json(self, filename: Optional[str] = None, append_mode: bool = True) -> str:
        """
        导出消息到 JSON 文件（支持追加模式）

        Args:
            filename: 输出文件名，如果为 None 则使用 session_id
            append_mode: 是否追加模式（同一 session 追加到同一文件）

        Returns:
            生成的文件路径
        """
        if not self.messages:
            raise ValueError("No messages to export")

        # 确保目录存在
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not ensure directory exists: {e}")

        # 生成文件名：使用 session_id 作为文件名（一个 session 一个文件）
        if filename is None:
            if self.current_session_id:
                filename = f"session_{self.current_session_id[:8]}.json"
            else:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                filename = f"messages_{timestamp}.json"

        output_path = self.output_dir / filename

        # 清理和重组消息，并按时间戳排序
        cleaned_messages = []
        for msg in self.messages:
            cleaned_msg = {}
            # 保留关键字段，去除冗余字段
            for key, value in msg.items():
                # 跳过 None、空字符串、parent_tool_use_id 等冗余字段
                if value is None or value == "" or key in ["parent_tool_use_id"]:
                    continue
                cleaned_msg[key] = value
            cleaned_messages.append(cleaned_msg)

        # 按时间戳排序所有消息（包括 UserInstruction）
        cleaned_messages.sort(key=lambda x: x.get("timestamp", ""))

        # 如果文件存在且是追加模式，读取现有数据
        existing_data = None
        if append_mode and output_path.exists():
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not read existing file: {e}")

        # 构建导出数据
        if existing_data and append_mode:
            # 追加模式：合并消息
            existing_data["messages"].extend(cleaned_messages)
            # 重新排序所有消息
            existing_data["messages"].sort(key=lambda x: x.get("timestamp", ""))
            existing_data["message_count"] = len(existing_data["messages"])
            existing_data["last_updated"] = datetime.utcnow().isoformat()  # 使用 UTC 时间

            # 更新统计信息
            instruction_count = sum(1 for msg in existing_data["messages"] if msg.get("type") == "UserInstruction")
            existing_data["user_instruction_count"] = instruction_count

            # 更新 model（如果有新的）
            if self.model_name:
                existing_data["model"] = self.model_name

            export_data = existing_data
        else:
            # 新建模式
            instruction_count = sum(1 for msg in cleaned_messages if msg.get("type") == "UserInstruction")

            export_data = {
                "session_id": self.current_session_id,
                "session_start": self.session_start_time or datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat(),  # 使用 UTC 时间
                "message_count": len(cleaned_messages),
                "user_instruction_count": instruction_count,
                "messages": cleaned_messages
            }

            # 添加 model 信息到最外层
            if self.model_name:
                export_data["model"] = self.model_name

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

        return str(output_path)

    def clear(self):
        """清空消息记录"""
        self.messages.clear()
        self.current_session_id = None

    def get_summary(self) -> Dict[str, Any]:
        """获取消息统计摘要"""
        if not self.messages:
            return {"total": 0}

        # 统计各类型消息数量
        type_counts = {}
        for msg in self.messages:
            msg_type = msg.get("type", "unknown")
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1

        return {
            "total": len(self.messages),
            "by_type": type_counts,
            "session_id": self.current_session_id,
            "first_timestamp": self.messages[0].get("timestamp") if self.messages else None,
            "last_timestamp": self.messages[-1].get("timestamp") if self.messages else None,
        }
