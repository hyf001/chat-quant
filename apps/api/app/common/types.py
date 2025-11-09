from enum import Enum
from typing import Optional

class AgentType(str, Enum):

    """数据分析智能体"""
    ANALYIS = "analysis"

    """金融数据分析智能体"""
    FIN_ANALYSIS = "fin-analysis"

    """生成next.js代码智能体"""
    NEXT_JS = "next-js"

    @classmethod
    def from_value(cls,value : str):
        for item in cls:
            if item.value == value:
                return item
        return None
