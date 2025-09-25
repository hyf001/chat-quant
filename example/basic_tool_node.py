


from email import message
import json
from typing import Any
from langchain_core.messages import ToolMessage


class BasicToolNode:
    def __init__(self,tools: list) -> None:
        self.tools_by_name = {tool.name : tool for tool in tools}

    def __call__(self, inputs: dict):
        message = inputs.get("messages",[])
        message = message[-1]
        outputs=[]
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call['name']].invoke(tool_call['args'])
            outputs.append(
                ToolMessage(content=json.dumps(tool_result),
                            name=tool_call['name'],
                            tool_call_id=tool_call['id'])
            )
        return {"messages":outputs}
