"""
Agent Execution Trace Generator

Generates comprehensive execution traces from database messages for evaluation purposes.
Supports both Markdown (for LLM evaluation) and JSON (for programmatic analysis) formats.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal, Union
from pathlib import Path
from dataclasses import dataclass, asdict
import re
from sqlalchemy.orm import Session


@dataclass
class TraceMetadata:
    """Trace metadata"""
    project_id: str
    start_time: str
    end_time: str
    duration_seconds: float
    model: Optional[str]
    cli_type: Optional[str]
    total_cost_usd: Optional[float] = None
    total_tokens: Optional[int] = None
    total_tokens_processed: Optional[int] = None


@dataclass
class TraceStatistics:
    """Trace statistics"""
    total_messages: int
    tool_calls: int
    errors: int
    retries: int
    message_breakdown: Dict[str, int]
    tool_breakdown: Dict[str, int]


@dataclass
class ToolCall:
    """Tool call information"""
    index: int
    timestamp: str
    tool_name: str
    tool_id: str
    tool_input: Dict[str, Any]
    tool_output: Optional[str]
    duration_ms: Optional[int]
    success: bool
    agent_thought: Optional[str]
    phase: Optional[str]


@dataclass
class Phase:
    """Execution phase"""
    name: str
    description: str
    start_index: int
    end_index: int
    duration_seconds: float
    tool_calls: int


class TraceGenerator:
    """Generate execution traces from database messages

    Supports both SQLAlchemy Session (recommended) and direct SQLite path (legacy).
    """

    def __init__(self, db: Union[Session, str]):
        """
        Initialize TraceGenerator

        Args:
            db: SQLAlchemy Session or SQLite database path string
        """
        if isinstance(db, Session):
            # SQLAlchemy Session (supports all databases)
            self.session = db
            self.conn = None
            self.cursor = None
            self.using_sqlalchemy = True
        else:
            # Legacy SQLite path support
            self.session = None
            self.conn = sqlite3.connect(db)
            self.cursor = self.conn.cursor()
            self.using_sqlalchemy = False

    def close(self):
        """Close database connection (only for SQLite mode)"""
        if self.conn:
            self.conn.close()

    def get_project_messages(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a project"""
        if self.using_sqlalchemy:
            # Use SQLAlchemy ORM
            from app.models.messages import Message

            db_messages = self.session.query(Message).filter(
                Message.project_id == project_id
            ).order_by(Message.created_at.asc()).all()

            messages = []
            for msg in db_messages:
                messages.append({
                    'id': msg.id,
                    'project_id': msg.project_id,
                    'role': msg.role,
                    'message_type': msg.message_type,
                    'content': msg.content,
                    'metadata': msg.metadata_json or {},
                    'parent_message_id': msg.parent_message_id,
                    'duration_ms': msg.duration_ms,
                    'token_count': msg.token_count,
                    'cost_usd': float(msg.cost_usd) if msg.cost_usd else None,
                    'commit_sha': msg.commit_sha,
                    'cli_source': msg.cli_source,
                    'created_at': msg.created_at.isoformat()
                })

            return messages
        else:
            # Legacy SQLite mode
            query = '''
                SELECT id, project_id, role, message_type, content,
                       metadata_json, parent_message_id,
                       duration_ms, token_count, cost_usd,
                       commit_sha, cli_source, created_at
                FROM messages
                WHERE project_id = ?
                ORDER BY created_at ASC
            '''
            self.cursor.execute(query, (project_id,))

            messages = []
            for row in self.cursor.fetchall():
                metadata = json.loads(row[5]) if row[5] else {}

                msg = {
                    'id': row[0],
                    'project_id': row[1],
                    'role': row[2],
                    'message_type': row[3],
                    'content': row[4],
                    'metadata': metadata,
                    'parent_message_id': row[6],
                    'duration_ms': row[7],
                    'token_count': row[8],
                    'cost_usd': row[9],
                    'commit_sha': row[10],
                    'cli_source': row[11],
                    'created_at': row[12]
                }
                messages.append(msg)

            return messages

    def extract_metadata(self, messages: List[Dict]) -> TraceMetadata:
        """Extract metadata from messages"""
        if not messages:
            raise ValueError("No messages found")

        first_msg = messages[0]
        last_msg = messages[-1]

        start_time = datetime.fromisoformat(first_msg['created_at'])
        end_time = datetime.fromisoformat(last_msg['created_at'])
        duration = (end_time - start_time).total_seconds()

        # Try to extract model info, cost and tokens from system messages
        model = None
        cli_type = None
        total_cost_usd = None
        total_tokens = None
        total_tokens_processed = None

        for msg in messages:
            if msg['role'] == 'system' and msg['metadata']:
                # Extract model and cli_type
                if not model:
                    model = msg['metadata'].get('model')
                if not cli_type:
                    cli_type = msg['metadata'].get('cli_type')

                # Extract cost and token info from result messages
                if msg['message_type'] == 'result':
                    # Extract total cost
                    cost = msg['metadata'].get('total_cost_usd')
                    if cost is not None:
                        total_cost_usd = float(cost) if total_cost_usd is None else total_cost_usd + float(cost)

                    # Extract tokens from usage string
                    usage_str = msg['metadata'].get('usage')
                    if usage_str and isinstance(usage_str, str):
                        try:
                            # Parse usage string like "{'input_tokens': 3, 'output_tokens': 624, ...}"
                            import ast
                            usage_dict = ast.literal_eval(usage_str)
                            if isinstance(usage_dict, dict):
                                input_tokens = usage_dict.get('input_tokens', 0)
                                output_tokens = usage_dict.get('output_tokens', 0)
                                cache_creation = usage_dict.get('cache_creation_input_tokens', 0)
                                cache_read = usage_dict.get('cache_read_input_tokens', 0)

                                # New tokens (input + output)
                                session_tokens = input_tokens + output_tokens
                                total_tokens = session_tokens if total_tokens is None else total_tokens + session_tokens

                                # Total processed tokens (including cache)
                                session_processed = input_tokens + output_tokens + cache_creation + cache_read
                                total_tokens_processed = session_processed if total_tokens_processed is None else total_tokens_processed + session_processed
                        except:
                            pass

        return TraceMetadata(
            project_id=first_msg['project_id'],
            start_time=first_msg['created_at'],
            end_time=last_msg['created_at'],
            duration_seconds=duration,
            model=model,
            cli_type=cli_type,
            total_cost_usd=total_cost_usd,
            total_tokens=total_tokens,
            total_tokens_processed=total_tokens_processed
        )

    def calculate_statistics(self, messages: List[Dict]) -> TraceStatistics:
        """Calculate statistics from messages"""
        msg_breakdown = {}
        tool_breakdown = {}
        tool_calls = 0
        errors = 0

        for msg in messages:
            # Message breakdown
            key = f"{msg['role']}_{msg['message_type']}"
            msg_breakdown[key] = msg_breakdown.get(key, 0) + 1

            # Tool breakdown
            if msg['message_type'] == 'tool_use':
                tool_calls += 1
                tool_name = msg['metadata'].get('tool_name', 'unknown')
                tool_breakdown[tool_name] = tool_breakdown.get(tool_name, 0) + 1

            # Error count
            if msg['message_type'] == 'error':
                errors += 1

        return TraceStatistics(
            total_messages=len(messages),
            tool_calls=tool_calls,
            errors=errors,
            retries=0,  # TODO: detect retries
            message_breakdown=msg_breakdown,
            tool_breakdown=tool_breakdown
        )

    def extract_tool_calls(self, messages: List[Dict]) -> List[ToolCall]:
        """Extract tool calls with their results"""
        tool_calls = []
        tool_outputs = {}  # Store outputs by tool_id

        # First pass: collect tool outputs
        for msg in messages:
            if msg['role'] == 'user' and msg['metadata'].get('tool_id'):
                tool_id = msg['metadata']['tool_id']
                tool_outputs[tool_id] = msg['content']

        # Second pass: build tool calls
        index = 0
        last_assistant_text = None

        for msg in messages:
            # Track assistant thoughts
            if msg['role'] == 'assistant' and msg['message_type'] == 'chat':
                last_assistant_text = msg['content']

            # Process tool calls
            if msg['message_type'] == 'tool_use':
                index += 1
                tool_id = msg['metadata'].get('tool_id', '')
                tool_name = msg['metadata'].get('tool_name', 'unknown')
                tool_input = msg['metadata'].get('tool_input', {})

                # Get output for this tool call
                output = tool_outputs.get(tool_id)

                tool_call = ToolCall(
                    index=index,
                    timestamp=msg['created_at'],
                    tool_name=tool_name,
                    tool_id=tool_id,
                    tool_input=tool_input,
                    tool_output=output,
                    duration_ms=msg.get('duration_ms'),
                    success=output is not None and 'error' not in output.lower()[:200],
                    agent_thought=last_assistant_text,
                    phase=None  # Will be assigned later
                )
                tool_calls.append(tool_call)

                # Reset thought after using it
                last_assistant_text = None

        return tool_calls

    def identify_phases(self, tool_calls: List[ToolCall], messages: List[Dict]) -> List[Phase]:
        """Identify execution phases based on tool usage patterns"""
        if not tool_calls:
            return []

        phases = []
        current_phase = None
        phase_patterns = {
            'exploration': ['Bash', 'Glob', 'Grep', 'Read'],
            'planning': ['TodoWrite'],
            'query': ['mcp__sql__preview_sql_result', 'mcp__sql__download_sql_result'],
            'processing': ['Write', 'Bash'],
            'reporting': ['Write']
        }

        for i, tool_call in enumerate(tool_calls):
            # Determine which phase this tool belongs to
            detected_phase = None
            for phase_name, tools in phase_patterns.items():
                if any(tool in tool_call.tool_name for tool in tools):
                    detected_phase = phase_name
                    break

            if detected_phase is None:
                detected_phase = 'other'

            # Assign phase to tool call
            tool_call.phase = detected_phase

            # Check if we need to start a new phase
            if current_phase is None or current_phase['name'] != detected_phase:
                # Close previous phase
                if current_phase:
                    phases.append(Phase(
                        name=current_phase['name'],
                        description=current_phase['description'],
                        start_index=current_phase['start_index'],
                        end_index=i - 1,
                        duration_seconds=current_phase['duration'],
                        tool_calls=current_phase['tool_count']
                    ))

                # Start new phase
                current_phase = {
                    'name': detected_phase,
                    'description': self._get_phase_description(detected_phase),
                    'start_index': i,
                    'duration': 0,
                    'tool_count': 0
                }

            current_phase['tool_count'] += 1

        # Close last phase
        if current_phase:
            phases.append(Phase(
                name=current_phase['name'],
                description=current_phase['description'],
                start_index=current_phase['start_index'],
                end_index=len(tool_calls) - 1,
                duration_seconds=0,  # TODO: calculate
                tool_calls=current_phase['tool_count']
            ))

        return phases

    def _get_phase_description(self, phase_name: str) -> str:
        """Get description for a phase"""
        descriptions = {
            'exploration': '需求理解与元数据探索',
            'planning': '任务规划',
            'query': 'SQL查询与数据获取',
            'processing': '数据处理与分析',
            'reporting': '报告生成',
            'other': '其他操作'
        }
        return descriptions.get(phase_name, phase_name)

    def extract_user_queries(self, messages: List[Dict]) -> List[str]:
        """Extract all user queries"""
        queries = []
        for msg in messages:
            if msg['role'] == 'user' and msg['message_type'] in ['chat', 'user']:
                queries.append(msg['content'])
        return queries

    def extract_final_response(self, messages: List[Dict]) -> Optional[str]:
        """Extract the final assistant response"""
        for msg in reversed(messages):
            if msg['role'] == 'assistant' and msg['message_type'] == 'chat':
                return msg['content']
        return None

    def generate_markdown(
        self,
        project_id: str,
        max_output_length: int = 1000
    ) -> str:
        """Generate Markdown format trace for a project"""
        messages = self.get_project_messages(project_id)
        if not messages:
            return "# No messages found\n"

        metadata = self.extract_metadata(messages)
        stats = self.calculate_statistics(messages)
        tool_calls = self.extract_tool_calls(messages)
        phases = self.identify_phases(tool_calls, messages)
        user_queries = self.extract_user_queries(messages)
        final_response = self.extract_final_response(messages)

        # Build markdown
        md = []

        # Header
        md.append("# Agent 执行轨迹")
        md.append("")

        # Metadata
        md.append("## 📋 任务概览")
        md.append("")
        md.append(f"- **Project ID**: {metadata.project_id}")
        md.append(f"- **执行时长**: {self._format_duration(metadata.duration_seconds)}")
        md.append(f"- **开始时间**: {self._format_datetime(metadata.start_time)}")
        md.append(f"- **结束时间**: {self._format_datetime(metadata.end_time)}")
        if metadata.model:
            md.append(f"- **模型**: {metadata.model}")
        md.append("")

        # User queries
        if user_queries:
            md.append("## 🎯 用户需求")
            md.append("")
            for i, query in enumerate(user_queries, 1):
                if len(user_queries) > 1:
                    md.append(f"### Query {i}")
                    md.append("")
                md.append(query)
                md.append("")

        # Statistics
        md.append("## 📊 执行统计")
        md.append("")
        md.append(f"- **总消息数**: {stats.total_messages}")
        md.append(f"- **工具调用次数**: {stats.tool_calls}")
        if stats.errors > 0:
            md.append(f"- **错误次数**: {stats.errors}")
        md.append("")

        md.append("### 工具使用分布")
        md.append("")
        for tool, count in sorted(stats.tool_breakdown.items(), key=lambda x: x[1], reverse=True):
            md.append(f"- {tool}: {count}次")
        md.append("")

        # Execution flow
        md.append("## 🔄 执行流程")
        md.append("")

        current_phase = None
        for tool_call in tool_calls:
            # Add phase header if needed
            if tool_call.phase != current_phase:
                current_phase = tool_call.phase
                phase_info = next((p for p in phases if p.name == current_phase), None)
                if phase_info:
                    md.append(f"### 阶段: {phase_info.description}")
                    md.append("")

            # Add tool call
            md.append(f"#### [Step {tool_call.index}] {self._get_tool_display_name(tool_call.tool_name)}")
            md.append(f"**Time**: {self._format_time(tool_call.timestamp)}")
            md.append(f"**Tool**: {tool_call.tool_name}")

            if tool_call.agent_thought:
                thought = tool_call.agent_thought[:200]
                md.append(f"**Agent思考**: {thought}...")
                md.append("")

            # Add tool input
            if tool_call.tool_input:
                md.append("**Input**:")
                md.append("```json")
                md.append(json.dumps(tool_call.tool_input, ensure_ascii=False, indent=2))
                md.append("```")
                md.append("")

            # Add tool output (truncated)
            if tool_call.tool_output:
                output = tool_call.tool_output
                if len(output) > max_output_length:
                    output = output[:max_output_length] + f"\n... (truncated, total {len(tool_call.tool_output)} chars)"

                md.append("**Output**:")
                md.append("```")
                md.append(output)
                md.append("```")
                md.append("")

        # Final result
        if final_response:
            md.append("## ✅ 最终结果")
            md.append("")
            md.append(final_response)
            md.append("")

        # Summary
        md.append("## 📈 性能指标")
        md.append("")
        md.append(f"- **任务完成**: {'✅ 成功' if stats.errors == 0 else '❌ 失败'}")
        md.append(f"- **执行时长**: {metadata.duration_seconds:.1f}秒")
        md.append(f"- **工具调用**: {stats.tool_calls}次")
        if stats.tool_calls > 0:
            md.append(f"- **平均每步耗时**: {metadata.duration_seconds / stats.tool_calls:.1f}秒")
        md.append("")

        return "\n".join(md)

    def generate_json(
        self,
        project_id: str,
        include_full_output: bool = False
    ) -> Dict[str, Any]:
        """Generate JSON format trace for a project"""
        messages = self.get_project_messages(project_id)
        if not messages:
            return {"error": "No messages found"}

        metadata = self.extract_metadata(messages)
        stats = self.calculate_statistics(messages)
        user_queries = self.extract_user_queries(messages)
        final_response = self.extract_final_response(messages)

        # Build timeline
        timeline = []
        for i, msg in enumerate(messages):
            timeline_entry = {
                'index': i + 1,
                'timestamp': msg['created_at'],
                'type': f"{msg['role']}_{msg['message_type']}",
                'role': msg['role'],
                'message_type': msg['message_type'],
                'content': msg['content'] if include_full_output else msg['content'][:500],
                'metadata': msg['metadata']
            }
            timeline.append(timeline_entry)

        # Build JSON structure
        trace = {
            'trace_version': '1.0',
            'generated_at': datetime.utcnow().isoformat(),

            'metadata': asdict(metadata),

            'task': {
                'user_queries': user_queries,
                'task_type': 'data_analysis',  # TODO: detect
                'success': stats.errors == 0
            },

            'statistics': asdict(stats),

            'timeline': timeline,

            'outcome': {
                'success': stats.errors == 0,
                'final_response': final_response,
                'errors': stats.errors
            }
        }

        return trace

    def generate_trace_files(
        self,
        project_id: str,
        output_dir: str,
        format: Literal['markdown', 'json', 'both'] = 'both'
    ) -> Dict[str, str]:
        """
        Generate trace files for a project

        Args:
            project_id: Project ID
            output_dir: Output directory
            format: Output format (markdown, json, or both)

        Returns:
            Dictionary of generated file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Check if project has messages
        messages = self.get_project_messages(project_id)
        if not messages:
            raise ValueError(f"No messages found for project {project_id}")

        generated_files = {}

        # Generate Markdown
        if format in ['markdown', 'both']:
            md_path = output_path / "trace.md"
            markdown = self.generate_markdown(project_id)
            md_path.write_text(markdown, encoding='utf-8')
            generated_files['markdown'] = str(md_path)

        # Generate JSON
        if format in ['json', 'both']:
            json_path = output_path / "trace.json"
            trace_json = self.generate_json(project_id, include_full_output=True)
            json_path.write_text(
                json.dumps(trace_json, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            generated_files['json'] = str(json_path)

        return generated_files

    # Utility methods
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = seconds % 60
            return f"{minutes}分{secs:.0f}秒"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}小时{minutes}分"

    def _format_datetime(self, dt_str: str) -> str:
        """Format datetime string"""
        try:
            dt = datetime.fromisoformat(dt_str)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return dt_str

    def _format_time(self, dt_str: str) -> str:
        """Format time only"""
        try:
            dt = datetime.fromisoformat(dt_str)
            return dt.strftime("%H:%M:%S")
        except:
            return dt_str

    def _get_tool_display_name(self, tool_name: str) -> str:
        """Get display name for tool"""
        display_names = {
            'Bash': 'Shell 命令',
            'Read': '读取文件',
            'Write': '写入文件',
            'Edit': '编辑文件',
            'Glob': '文件搜索',
            'Grep': '内容搜索',
            'TodoWrite': '任务规划',
            'mcp__sql__preview_sql_result': 'SQL 查询预览',
            'mcp__sql__download_sql_result': 'SQL 结果下载',
        }
        return display_names.get(tool_name, tool_name)
