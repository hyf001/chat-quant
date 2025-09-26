
from langgraph.graph import MessagesState
from typing import Literal, Optional, Dict, Any, List, Self



class State(MessagesState):
    # 意图
    intention:Literal["-生成金融数据分析页面","生成量化交易策略","都不是"]
    current_plan:Optional[str]
