
from langgraph.graph import MessagesState
from typing import Optional, Dict, Any, List, Self



class State(MessagesState):
    # 意图
    intention:Optional[str]
    current_plan:Optional[str]
